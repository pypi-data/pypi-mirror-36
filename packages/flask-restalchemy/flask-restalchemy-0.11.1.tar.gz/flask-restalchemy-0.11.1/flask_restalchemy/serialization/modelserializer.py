from typing import Union

from sqlalchemy.orm.dynamic import AppenderMixin
from sqlalchemy.sql import sqltypes

from flask_restalchemy.serialization.serializer import Serializer, DateTimeSerializer, is_datetime_field, is_enum_field, \
    EnumSerializer


class ModelSerializer(Serializer):
    """
    Serializer for SQLAlchemy Declarative classes
    """

    DEFAULT_SERIALIZERS = [
        (is_datetime_field, DateTimeSerializer),
        (is_enum_field, EnumSerializer)
    ]

    def __init__(self, model_class):
        """
        :param Type[DeclarativeMeta] model_class: the SQLAlchemy mapping class to be serialized
        """
        self._mapper_class = model_class
        self._fields = self._get_declared_fields()
        # Collect columns not declared in the serializer
        for column in self.model_columns.keys():
            field = self._fields.setdefault(column, Field())
            # Set a serializer for fields that can not be serialized by default
            if field.serializer is None:
                serializer = self._get_default_serializer(self.model_columns.get(column))
                if serializer:
                    field._serializer = serializer

    def get_model_name(self) -> str:
        return self._mapper_class.__name__

    @property
    def model_columns(self) -> dict:
        return self._mapper_class.__mapper__.c

    def dump(self, model):
        serial = {}
        for attr, field in self._fields.items():
            if field is None:
                serial[attr] = getattr(model, attr)
                continue
            if field.load_only:
                continue
            value = getattr(model, attr) if hasattr(model, attr) else None
            if value is None:
                serialized = None
            elif field.serializer:
                serialized = field.serializer.dump(value)
            else:
                serialized = value
            serial[attr] = serialized
        return serial

    def load(self, serialized, existing_model=None):
        """
        Instancialize a Declarative model from a serialized dict

        :param dict serialized: the serialized object.

        :param None|DeclarativeMeta existing_model: If given, the model will be updated with the serialized data.

        :rtype: DeclarativeMeta
        """
        if existing_model:
            model = existing_model
            # If deserialization must update an existing model, check if primary key is the same
            pk_name = self._get_pk_name(existing_model)
            assert getattr(existing_model, pk_name) == serialized[pk_name], \
                "Primary key value of serialized nested object is inconsistent"
        else:
            model = self._mapper_class()
        for field_name, value in serialized.items():
            field = self._fields[field_name]
            if field.dump_only:
                continue
            if value is None:
                deserial_value = value
            elif field.serializer:
                if isinstance(field.serializer, ModelSerializer):
                    if existing_model:
                        existing_nested = getattr(existing_model, field_name)
                    else:
                        existing_nested = self._find_existing_model(field, value)
                    deserial_value = field.serializer.load(value, existing_nested)
                else:
                    deserial_value = field.serializer.load(value)
            else:
                deserial_value = value
            setattr(model, field_name, deserial_value)
        return model

    def before_put_commit(self, model, session):
        pass

    def after_put_commit(self, model, session):
        pass

    def before_post_commit(self, model, session):
        pass

    def after_post_commit(self, model, session):
        pass

    def _get_default_serializer(self, column):
        for check_type, serializer_class in self.DEFAULT_SERIALIZERS:
            if check_type(column):
                return serializer_class(column)

    @classmethod
    def _get_declared_fields(cls) -> dict:
        fields = {}
        # Fields should be only defined ModelSerializer subclasses,
        if cls is ModelSerializer:
            return fields
        for attr_name in dir(cls):
            if attr_name.startswith('_'):
                continue
            value = getattr(cls, attr_name)
            if isinstance(value, Field):
                fields[attr_name] = value
        return fields

    def _find_existing_model(self, field, value):
        class_mapper = field.serializer._mapper_class
        pk_name = self._get_pk_name(class_mapper)
        pk = value.get(pk_name)
        if pk:
            return class_mapper.query.get(pk)
        else:
            return None

    def _get_pk_name(self, existing_model):
        primary_keys = existing_model.__mapper__.primary_key
        assert len(primary_keys) == 1, "Nested object must have exactly one primary key"
        pk_name = primary_keys[0].key
        return pk_name


class Field(object):
    """
    Configure a ModelSerializer field
    """

    def __init__(self, dump_only=False, load_only=False, serializer=None):
        self.dump_only = dump_only
        self.load_only = load_only
        self._serializer = serializer

    @property
    def serializer(self):
        return self._serializer


class NestedModelField(Field):
    """
    A field to Dump and Update nested models.
    """

    def __init__(self, declarative_class, **kw):
        super().__init__(**kw)
        if self._serializer is None:
            self._serializer = ModelSerializer(declarative_class)


class NestedAttributesField(Field):
    """
    A read-only field that dump nested object attributes.
    """

    class NestedAttributesSerializer(Serializer):

        def __init__(self, attributes, many):
            self.attributes = attributes
            self.many = many

        def dump(self, value):
            if self.many:
                serialized = [self._dump_item(item) for item in value]
            else:
                return self._dump_item(value)
            return serialized

        def _dump_item(self, item):
            serialized = {}
            for attr_name in self.attributes:
                serialized[attr_name] = getattr(item, attr_name)
            return serialized

        def load(self, serialized):
            raise NotImplementedError()


    def __init__(self, attributes: Union[tuple, dict], many=False, **kw):
        super().__init__(serializer=self.NestedAttributesSerializer(attributes, many), **kw)
        assert 'serializer' not in kw, "NestedAttributesField does not support custom Serializer"


class PrimaryKeyField(Field):
    """
    Convert relationships in a list of primary keys (for serialization and deserialization).
    """

    class PrimaryKeySerializer(Serializer):

        def __init__(self, declarative_class):
            self.declarative_class = declarative_class
            self._pk_column = get_model_pk(self.declarative_class)

        def load(self, serialized):
            pk_column = self._pk_column
            return self.declarative_class.query.filter(pk_column.in_(serialized)).all()

        def dump(self, value):
            pk_column = self._pk_column
            if is_tomany_attribute(value):
                serialized = [getattr(item, pk_column.key) for item in value]
            else:
                return getattr(value, pk_column.key)
            return serialized

    def __init__(self, declarative_class, **kw):
        super().__init__(serializer=self.PrimaryKeySerializer(declarative_class), **kw)


def get_model_pk(declarative_class):
    """
    Get the primary key Column object from a Declarative model class

    :param Type[DeclarativeMeta] declarative_class: a Declarative class

    :rtype: Column
    """
    primary_keys = declarative_class.__mapper__.primary_key
    assert len(primary_keys) == 1, "Nested object must have exactly one primary key"
    return primary_keys[0]


def is_tomany_attribute(value):
    """
    Check if the Declarative relationship attribute represents a to-many relationship.

    :param value: a SQLAlchemy Declarative class relationship attribute

    :rtype: bool
    """
    return isinstance(value, (list, AppenderMixin))

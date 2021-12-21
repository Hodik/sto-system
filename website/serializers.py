from django.db.models import fields
from website.models import *
from typing import Union
import json
from rest_framework import serializers

"""class Serializer:

    def __init__(self, obj, many: bool = False) -> Union[list, dict]:

        __meta = self.Meta()
        self._model = __meta.model
        self._fields = __meta.fields
        self._many = many

        self.serialized = self.serialize(obj)

    
    def __get_fields(self) -> tuple:
        if type(self._fields) == tuple:
            return self._fields
        else:
            return (f.name for f in self._model._meta.get_fields())

    def __get_attr_by_name(self, obj, attr: str):
        return getattr(obj, attr)

    def __get_attr_by_source(seld, obj, source: str):
        return getattr(obj, source)()

    def __serialize_entry(self, entry):
        rv: dict = {}

        for field in self.__get_fields():
            rv[field] = str(self.__get_attr_by_name(entry, field))

        if hasattr(self, "custom_fields"):
            for field in self.custom_fields:
                if hasattr(entry, field['name']):
                    if 'serializer' in field:
                        attr_value = self.__get_attr_by_name(entry, field['name'])
                        if attr_value.exists():
                            nested_obj = field['serializer'](attr_value.all(), many=field['many']).serialized
                            rv[field['name']] = nested_obj
                        else:
                            rv[field['name']] = ""

                elif 'source' in field:
                    attr_value = self.__get_attr_by_source(entry, field['source'])
                    rv[field['name']] = str(attr_value)
        return rv

    def serialize(self, obj) -> Union[list, dict]:
        if self._many: 
            rv = []
            for el in obj:
                rv.append(self.__serialize_entry(el))
        else: rv = self.__serialize_entry(obj)

        return rv

    def get_json(self) -> str:
        return json.dumps(self.serialized)

class ReviewsSerializer(Serializer):

    class Meta:
        model = Review
        fields = '__all__'

class StoSerializer(Serializer):

    custom_fields = ({'name': 'sto_reviews', 'serializer': ReviewsSerializer, 'many': True}, 
        {'name': 'average_rating', 'source': 'get_average_rating'})

    class Meta:
        model = Sto
        fields = '__all__'"""

class StoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sto
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

from abc import ABC, abstractmethod
from dict2xml import dict2xml
import yaml


class FormatSerializer(ABC):

    @abstractmethod
    def set_object(self, obj): ...

    @abstractmethod
    def to_str(self): ...

class JsonSerializer(FormatSerializer):
    def __init__(self):
        self._current_object = None

    def set_object(self, obj):
        self._current_object = obj

    def to_str(self):
        return json.dumps(self._current_object)

class XMLSerializer(FormatSerializer):
    def __init__(self):
        self._current_object = None

    def set_object(self, obj):
        self._current_object = obj

    def to_str(self):
        print(self._current_object)
        return dict2xml(self._current_object)

class YamlSerializer(XMLSerializer):
    def to_str(self):
        return yaml.dump(self._current_object)

class FormatFactory:
    def __init__(self):
        self._creators = {}

    def register_creator(self, name, creator):
        self._creators[name] = creator

    def get_serializer(self, name):
        creator = self._creators.get(name)
        if not creator:
            raise ValueError(name)
        return creator()

format_factory = FormatFactory()
format_factory.register_creator('Json', JsonSerializer)
format_factory.register_creator('XML', XMLSerializer)
format_factory.register_creator('YAML', YamlSerializer)

class ObjectSerializer:
    def serialize(self, serializable, format: str):
        serializer = format_factory.get_serializer(format)
        serializer.set_object(serializable)
        return serializer.to_str()

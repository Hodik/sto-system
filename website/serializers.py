from django.db.models import fields
from website.models import *
from typing import Union
import json

class Serializer:

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
        fields = '__all__'



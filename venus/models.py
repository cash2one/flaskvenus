from . import db as mongodb

from mongoengine import (Document, DynamicDocument, EmbeddedDocument,LongField, SequenceField,
                        IntField, StringField, ListField, ReferenceField, EmbeddedDocumentField, 
                        DateTimeField, GeoPointField , connect)
from mongoengine.fields import FloatField
from bson import json_util

class ApiDocument(Document):
    meta = {'allow_inheritance':True, 'abstract': True}
    
    def to_api(self, hide_id = True):
        son = self.to_mongo();
        oid = son.pop('_id')
        if not hide_id:
            son['_id'] = str(oid)
        return son.to_dict()
        
#uid maybe uin , phoneNO
class User(Document):
    uin = LongField(unique=True, required=True)
    name = StringField(max_length=50)
    phoneNO = StringField(max_length=50, unique=True)
    password = StringField(max_length=200)
    sexType = IntField(default=1)
    meta = {'abstract': False, 'indexes': ['uin']}
    
    def to_api(self, hide_id = True):
        son = self.to_mongo();
        son.pop('password')
        if(hide_id):
            son.pop('_id')
            
        return son.to_dict()
    
    
class Profile(ApiDocument):
    uin = LongField(unique=True, required=True)
    avatar_id = StringField(max_length=50)
        
class Presence(Document):
    uin = LongField(unique=True, required=True)
    updated_at =  DateTimeField()
    auth_token = StringField(max_length=50)
    
class Relation(Document):
    owner = LongField(required=True)
    target = LongField(required=True)
    type = IntField()
                   
class DAType(Document):
    _typeId = IntField(db_field='typeId',unique=True, required=True)
    _typeName = StringField(db_field='typeName', max_length=50, unique=True, required=True)
    createUIN = LongField(required = True)
    scope = IntField(default=1)
    meta = {'collection': 'datype'}
    
    def gettype(self):
        """
        Returns (typename, maintype, subtype)
        """
        return (self._typeName, self._typeId>>16, self._typeId & 0xffff)
    
    def settype(self, type_name, sub_type, main_type=0):
        self._typeId = ((main_type & 0xffff) << 16)|(sub_type & 0xffff)
        self._typeName = type_name
        
    def to_api(self, hide_id = True):
        output = {}
        output['typeId'] = self['_typeId']
        output['mainTypeName'] = 'main'
        output['subTypeName'] = self['_typeName']
        if not hide_id:
            output['_id'] = str(self['_id'])
        return output
        
    

class Location(EmbeddedDocument):
    address = StringField()
    location = ListField()
    confidence = IntField(default=100)
    #position  = GeoPointField()
    #longitude = FloatField()
    #latitude = FloatField()
    
    
class Distraction(ApiDocument):
    title = StringField(max_length=120)
    create_time = LongField(required=True)
    start_time = LongField(required=True)
    #creatUser = ReferenceField(User)
    create_user_id = LongField(db_field='createuserid', required=True)
    description = StringField(max_length=500, required=True)
    origin_loc = EmbeddedDocumentField(Location)
    dst_loc = EmbeddedDocumentField(Location)
    group_id = StringField()
    tag_list = ListField(StringField(max_length=30))
    pay_type = IntField()
    max_member_count = IntField()
    min_member_count = IntField() 
    meta = {
    'indexes': ['*dst_loc.location',],
    'ordering': ['create_time']} 


class IDCounter(DynamicDocument):
    key = StringField(max_length=20, db_field='idName', required=True)
    value = IntField(db_field='idValue', required=True)
    id = SequenceField(db_field='_id')
    meta = {'collection': 'ID'}
    
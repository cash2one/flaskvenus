import datetime
from mongoengine import (Document, DynamicDocument, EmbeddedDocument,LongField, SequenceField, DictField,
                        IntField, StringField, ListField, ReferenceField, EmbeddedDocumentField, 
                        DateTimeField, GeoPointField , connect)
from mongoengine.fields import FloatField
from bson import json_util
from . import db as mongodb
from . import utils

class ApiDocument(Document):
    meta = {'allow_inheritance':True, 'abstract': True}
    
    def to_api(self, hide_id = True):
        son = self.to_mongo();
        son.pop('_cls')
        oid = son.pop('_id')
        if not hide_id:
            son['_id'] = str(oid)
        return son.to_dict()
        
#uid maybe uin , phoneNO
class User(Document):
    
    MEMBER = 100
    MODERATOR = 200
    ADMIN = 300
    
    uin = LongField(unique=True, required=True)
    name = StringField(max_length=50)
    phoneNO = StringField(max_length=50, unique=True)
    _password = StringField(db_field='password', max_length=200)
    role = IntField(default=MEMBER)
    avatarId = StringField(max_length=256)
    sexType = IntField(default=1)
    meta = {'abstract': False, 'indexes': ['uin']}
    
    def to_api(self, hide_id = True):
        son = self.to_mongo();
        son.pop('password')
        if(hide_id):
            son.pop('_id')
            
        return son.to_dict()
    
    def is_admin(self):
        return self.role == ADMIN
    
class Profile(ApiDocument):
    uin = LongField(unique=True, required=True)
    avatar_id = StringField(max_length=50)
    like_das = ListField(StringField(max_length=32))
    collect_das = ListField(StringField(max_length=32))
    like_scs = ListField(StringField(max_length=32))
    collect_scs = ListField(StringField(max_length=32))
        
class Presence(Document):
    uin = LongField(unique=True, required=True)
    updated_at =  DateTimeField(default=utils.timestamp_ms)
    auth_token = StringField(max_length=50)
    
#用户和用户之间的关系
class UURelation(Document):
    owner = LongField(required=True)
    target = LongField(required=True)
    type = IntField()

#用户和场所或活动之间的关系    
class USDRelation(Document):
    owner = LongField(required=True)
    target = StringField(required=True)
    type = IntField()
    
#tag和Scenic, distraction的关系
class TSDRelation(Document):
    owner = LongField(required=True)
    target = StringField(required=True)
    type = IntField()
    
#场所和活动之间的关系    
class SDRelation(Document):
    owner = LongField(required=True)
    target = StringField(required=True)
    type = IntField()

    
 
class DATag(ApiDocument):
    #_id = StringField(unique=True,required=True)
    name = StringField(max_length=20, unique=True,required=True) 
    createUIN = LongField(required = True)
    parent = StringField(required=True, default='root')
    scope = StringField(default = 'pu') #"choice (public,private, friend)
    pic_url  = StringField(max_length=256)
    meta = {'collection': 'datag'}
        
                       
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
    city = StringField(max_length=10)
    address = StringField()
    location = ListField()
    confidence = IntField(default=100)
    #position  = GeoPointField()
    #longitude = FloatField()
    #latitude = FloatField()

class Comment(EmbeddedDocument):
    create_user_id = LongField(db_field='createUserId', required=True)
    create_time = LongField(db_field='createTime', default=utils.timestamp_ms)
    content = StringField(max_length=140)

class Scenic(ApiDocument):
    theme = StringField(max_length=20)
    summary = StringField(max_length=50)
    create_user_id = LongField(db_field='createUserId', required=True)
    create_time = LongField(db_field='createTime', default=utils.timestamp_ms)
    location = EmbeddedDocumentField(Location, db_field='originLoc')
    description = StringField(max_length=500, required=True)
    tag_list = ListField(StringField(max_length=30))
    expired_da = ListField(StringField(max_length=32))
    pending_da = ListField(StringField(max_length=32))
    like_num = IntField(db_field='likeNum')
    #TODO comment num is limit , becaus document is limit 
    comment_list = ListField(EmbeddedDocumentField(Comment))
    pic_main  = StringField(max_length=256)
    pic_others  = ListField(StringField(max_length=256))
    prop_ex = DictField()
    
    
        
class Distraction(ApiDocument):
    title = StringField(max_length=20)
    summary = StringField(max_length=50)
    create_time = LongField(db_field='createTime', default=utils.timestamp_ms)
    start_time = LongField(db_field='startTime', required=True)
    #creatUser = ReferenceField(User)
    create_user_id = LongField(db_field='createUserId', required=True)
    description = StringField(max_length=500, required=True)
    origin_loc = EmbeddedDocumentField(Location, db_field='originLoc')
    dst_loc = EmbeddedDocumentField(Location, db_field='dstLoc')
    group_id = StringField()
    tag_list = ListField(StringField(max_length=30))
    img_url_list = ListField(StringField(max_length = 256))
    like_num = IntField(db_field='likeNum')
    pay_type = IntField()
    max_member_count = IntField()
    min_member_count = IntField() 
    #TODO comment num is limit , becaus document is limit 
    comment_list = ListField(EmbeddedDocumentField(Comment))
    pic_main  = StringField(max_length=256)
    pic_others  = ListField(StringField(max_length=256))
    prop_ex = DictField()
    
    meta = {
    'indexes': ['*dst_loc.location',],
    'ordering': ['create_time']} 

        
class Topic(ApiDocument):
    title = StringField(max_length=20)
    summary = StringField(max_length=50)
    create_time = LongField(db_field='createTime', default=utils.timestamp_ms)
    
    
class IDCounter(DynamicDocument):
    key = StringField(max_length=20, db_field='idName', required=True)
    value = IntField(db_field='idValue', required=True)
    id = SequenceField(db_field='_id')
    meta = {'collection': 'ID'}
    
import datetime
from mongoengine import (Document, DynamicDocument, EmbeddedDocument,LongField, SequenceField, DictField,
                        BooleanField, IntField, StringField, ListField, ReferenceField,GenericReferenceField, 
                        EmbeddedDocumentField, DateTimeField, GeoPointField , connect)
from mongoengine.fields import FloatField
from bson import json_util
from . import db as mongodb
from random import choice
from pip._vendor.pkg_resources import require

        
class ApiDocument(Document):
    meta = {'allow_inheritance':True, 'abstract': True}
    
    def to_clean_son(self, hide_id = True):
        son = self.to_mongo();
        son.pop('_cls')
        oid = son.pop('_id')
        if not hide_id:
            son['_id'] = str(oid)
        return son
            
    def to_api(self, hide_id = True):
        return self.to_clean_son(hide_id).to_dict()
        
#uid maybe uin , phoneNO
class User(ApiDocument):
    
    MEMBER = 100
    MODERATOR = 200
    ADMIN = 300
    
    uin = LongField(primary_key=True, unique=True,  required=True)
    phone = StringField(max_length=50, unique=True)
    name  = StringField(max_length=50) 
    _password = StringField(db_field='password', max_length=200)
    role = IntField(choices=(MEMBER, MODERATOR, ADMIN), default=MEMBER)
    avatar_id = StringField(max_length=256)
    sex_type = IntField(default=1)
    meta = {'abstract': False, 'indexes': ['uin']}
    
    def to_api(self, hide_id = True):
        son = self.to_clean_son(True);
        son['uin'] = self.uin
        son.pop('password')
        return son.to_dict()
    
    def is_admin(self):
        return self.role == User.ADMIN
    
class Profile(ApiDocument):
    uin = LongField(unique=True, required=True)
    avatar_id = StringField(max_length=50)
    last_login_at = DateTimeField()
    current_login_at = DateTimeField()
    follower_num = IntField()
    like_das = IntField()
    favorite_das = IntField()
    like_scs = IntField()
    favorite_scs = IntField()
        
class Presence(Document):
    uin = LongField(unique=True, required=True)
    updated_at =  DateTimeField(default=datetime.datetime.now)
    city = StringField(max_length=10)
    auth_token = StringField(max_length=50)

def Relation(type1, type2):
    class RelationCls(ApiDocument):
        _type1=type1
        _type2=type2
    
    return RelationCls


class Focus(object):
    name  = StringField(max_length=50, unique=True, required=True) 
    created_by = ReferenceField(User,  required=True)
    create_time = DateTimeField(default=datetime.datetime.now)
    follower_num = IntField()
    subject =  StringField(default = 'scenic', max_length=20, choices =('album', 'scenic','distraction', 'user')) 
    
    def follow(self):
        pass

#当 Tag.scope为public时,即变成type
class Tag(Focus, ApiDocument):
    #_id = StringField(unique=True,required=True)
    parent = ReferenceField('self', required=False, default=None, reverse_delete_rule=mongodb.DENY)
    #offical指经公司编辑认同后由public提升而来的
    scope = StringField(default = 'pu', max_length=2) #"choices (offical, public,private, friend)
    feed_num = IntField()
    
    def get_children(self, **kwargs):
        """return direct children 1 level depth"""
        return self.__class__.objects(parent=self, **kwargs)
    
    meta = {'collection': 'tag'}

class Topic(Focus, ApiDocument):
    #_id = StringField(unique=True,required=True)
    feed_num = IntField()     
                
class Feedable(object):
    title = StringField(max_length=20)
    summary = StringField(max_length=50)
    topic = ReferenceField(Topic)
    tag_list = ListField(ReferenceField(Tag))
    imgurl  = StringField(max_length=256)
    like_num = IntField()
    created_by = ReferenceField(User)
    create_time = DateTimeField(default=datetime.datetime.now)

    def to_api(self, hide_id = True):
        if isinstance(self, ApiDocument):
            values = ApiDocument.to_api(self, hide_id)
            values['created_by'] = self.created_by.to_api()
            if self.topic:
                values['topic'] = self.topic.name
            values['tag_list'] = [tag.name for tag in self.tag_list]
            return values
        
        return self.__dict__    
    
class Followship(Relation(User, Focus)):
    target_type = StringField(required=True)

class Notification(ApiDocument):
    LIKED = 'L'
    COMMENTED = 'C'
    FOLLOWED = 'F'

    NOTIFICATION_TYPES = (
        (LIKED, 'Liked'),
        (COMMENTED, 'Commented'),
        (FOLLOWED, 'Follewed'),
    )
    
    from_user = ReferenceField(User)
    to_user = ReferenceField(User)
    date = DateTimeField(default=datetime.datetime.now)
    summary = StringField(max_length=50)
    detail_url =  StringField(max_length=256)
    notify_type = StringField(max_length=1, choices=NOTIFICATION_TYPES)
    is_read = BooleanField(default=False)
    
class FeedAction(Relation(User, Feedable)):  
    FAVORITE = 'F'
    LIKE = 'L'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTION_TYPES = (
        (FAVORITE, 'Favorite'),
        (LIKE, 'Like'),
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
    )
    
    user = ReferenceField(User)
    action_type = StringField(max_length=1, choices=ACTION_TYPES)
    date = DateTimeField(default=datetime.datetime.now)
    feed = StringField(max_length=50)
     
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
    tag = StringField(required=True)
    target = StringField(required=True)
    type = IntField()
    
#场所和活动之间的关系    
class SDRelation(Document):
    scenic_id = StringField(required=True)
    da_id = StringField(required=True)
    type = IntField()


class HotFocus(ApiDocument):
    focus = GenericReferenceField()  
    create_time = DateTimeField(default=datetime.datetime.now)
    _ttl_day =IntField(db_field = 'ttl_day', default=5)
    
                         
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
        
    @property
    def type(self):
        return self.gettype()
    
    @type.setter
    def type(self, **kargs):
        self.settype(type_name=kargs['type_name'], 
                     sub_type=kargs['type_name'], 
                     main_type=kargs.get('main_type', 0))
        
    def to_api(self, hide_id = True):
        output = {}
        output['type_id'] = self['_typeId']
        output['main_type_name'] = 'main'
        output['sub_type_name'] = self['_typeName']
        if not hide_id:
            output['_id'] = str(self['_id'])
        return output
        


class Poi(EmbeddedDocument):
    city = StringField(max_length=10)
    name = StringField(max_length=10)
    address = StringField(max_length=100)
    location = ListField()
    confidence = IntField(default=100)
    #position  = GeoPointField()
    #longitude = FloatField()
    #latitude = FloatField()

class Comment(EmbeddedDocument):
    created_by = ReferenceField(User,required=True)
    create_time = DateTimeField(default=datetime.datetime.now)
    content = StringField(max_length=140)
    deleted = BooleanField()
    
    
class Scenic(Feedable, ApiDocument):
    location = EmbeddedDocumentField(Poi)
    description = StringField(max_length=500, required=True)
    da_list = ListField(StringField(max_length=30))
    like_num = IntField()
    #TODO comment num is limit , becaus document is limit 
    comment_list = ListField(EmbeddedDocumentField(Comment))
    others_imgurl  = ListField(StringField(max_length=256))
    prop_ex = DictField()
    meta = {
    'indexes': ['*location.location',],
    'ordering': ['create_time']} 
    
    @property
    def creater(self):
        return User.objects.get(uin=create_user_id).to_api()
    
    
        
class Distraction(Feedable, ApiDocument):
    start_time = DateTimeField(default=datetime.datetime.now, required=True)
    origin_loc = EmbeddedDocumentField(Poi)
    dst_loc = EmbeddedDocumentField(Poi)
    group_id = StringField()
    img_url_list = ListField(StringField(max_length = 256))
    pay_type = IntField()
    max_member_count = IntField()
    min_member_count = IntField() 
    #TODO comment num is limit , becaus document is limit 
    comment_list = ListField(EmbeddedDocumentField(Comment))
    prop_ex = DictField()
    
    meta = {
    'indexes': ['*dst_loc.location',],
    'ordering': ['create_time']} 

        
class Album(Feedable, ApiDocument):
    pass

class RecommendFeed(ApiDocument):
    feedid=StringField(max_length=32)
    _ttl_day =IntField(db_field = 'ttl_day', default=5)
    subject =  StringField(default = 'scenic', max_length=20) #choice('album', 'scenic','distraction')
    create_time = DateTimeField(default=datetime.datetime.now, required=True)
        
    
class IDCounter(DynamicDocument):
    key = StringField(max_length=20, db_field='idName', required=True)
    value = IntField(db_field='idValue', required=True)
    id = SequenceField(db_field='_id')
    meta = {'collection': 'ID'}
    
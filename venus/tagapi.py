# -*- coding: utf-8 -*-

from flask import request
from mongoengine.errors import DoesNotExist
from .models import IDCounter, Tag
from . import app, db, idmanager,utils, userapi
from .apis import api, APIError, APIValueError
from bson import ObjectId

ALLOW_TAG_TYPE =  set(['topic', 'scenic', 'distraction', 'user'])
@app.route('/api/v1/sec/tags/<type>',  methods=['POST'])
@api
def add_tag(type):
    if type not in ALLOW_TAG_TYPE:
        return  'not found', 404

    form = request.form
    name = form['tagname']
    createuin = form['createuin']
    parent = form.get('parent', 'root')

    if  userapi.is_admin(createuin):
        scope = form.get('scope', 'of')
    else:
        scope = form.get('scope', 'pr') 
    
    tag = Tag(name=name, parent=parent,createUIN=createuin, scope=scope, target_type = type)
    #tag['_id'] = ObjectId()
    tag.save()
    return tag.to_api(hide_id=False),0
    
@app.route('/api/v1/sec/tags/<type>',  methods=['GET'])
@api
def list_all_tag(type):
    if type not in ALLOW_TAG_TYPE:
        return  'not found', 404
    
    try:
        list = Tag.objects(scope='pu', target_type = type)
    except DoesNotExist as e:
        list = []
        
    tags=[tag.to_api(hide_id=False) for tag in list]
    return {'total':len(tags), 'list': tags}, 0
 
 
@app.route('/api/v1/feedgroup',  methods=['GET'])
@api
def list_all_feedgroup():
    scenic_group = dict(name='推荐地点')     
    tags = Tag.objects(scope='of', target_type = 'scenic')
    scenic_group['value'] = [tag.to_api() for tag in tags]
    
    da_group = dict(name='活动') 
    tags = Tag.objects(scope='of', target_type = 'distraction')
    da_group['value'] = [tag.to_api() for tag in tags]
    
    topic_group = dict(name='专题')
    tags = Tag.objects(scope='of',  target_type = 'topic')
    topic_group['value'] = [tag.to_api() for tag in tags]
    
    feedgroup=[scenic_group, da_group, topic_group]
    return {'total':len(feedgroup), 'list': feedgroup}, 0
    
    
# -*- coding: utf-8 -*-

from flask import request, abort
from mongoengine.errors import DoesNotExist
from flask_mongoengine.wtf import model_form
from .models import IDCounter, Tag
from . import app, db, idmanager,utils, userapi
from .apis import api, APIError, APIValueError
from bson import ObjectId
from flask.helpers import url_for

ALLOW_TAG_SUBJECT =  set(['album', 'scenic', 'distraction', 'user'])
        
        
@app.route('/api/v1/sec/tags/<subject>',  methods=['POST'])                          
@api
def add_tag(subject):
    if subject not in ALLOW_TAG_SUBJECT:
        return  'not found', 404

    form = request.form
    name = form['name']
    createuin = form['createuin']
    parent = form.get('parent', 'root')

    if  userapi.is_admin(createuin):
        scope = form.get('scope', 'of')
    else:
        scope = form.get('scope', 'pr') 
    
    tag = Tag(name=name, parent=parent,createuin=createuin, scope=scope, subject = subject)
    #tag['_id'] = ObjectId()
    tag.save()
    return tag.to_api(hide_id=False),0
    
@app.route('/api/v1/sec/tags/<subject>',  methods=['GET'])
@api
def list_all_tag(subject):
    if subject not in ALLOW_TAG_SUBJECT:
        return  'not found', 404
    
    try:
        list = Tag.objects(scope='pu', subject = subject)
    except DoesNotExist as e:
        list = []
        
    tags=[tag.to_api(hide_id=False) for tag in list]
    return {'total':len(tags), 'list': tags}, 0
 
 
@app.route('/api/v1/feedgroup',  methods=['GET'])
@api
def list_all_feedgroup():
    scenic_group = dict(name='推荐地点', moreurl=url_for('add_tag', subject='scenic'))     
    tags = Tag.objects(scope='of', subject = 'scenic')
    scenic_group['value'] = [tag.to_api(False) for tag in tags]
    
    da_group = dict(name='活动', moreurl=url_for('add_tag', subject='distraction')) 
    tags = Tag.objects(scope='of', subject = 'distraction')
    da_group['value'] = [tag.to_api(False) for tag in tags]
    
    topic_group = dict(name='专题', moreurl=url_for('add_tag', subject='album'))
    tags = Tag.objects(scope='of',  subject = 'album')
    topic_group['value'] = [tag.to_api(False) for tag in tags]
    
    feedgroup=[scenic_group, da_group, topic_group]
    return {'total':len(feedgroup), 'list': feedgroup}, 0
    
    
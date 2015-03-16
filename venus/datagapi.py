# -*- coding: utf-8 -*-

from flask import request
from mongoengine.errors import DoesNotExist
from .models import IDCounter, Tag
from . import app, db, idmanager,utils
from .apis import api, APIError, APIValueError
from bson import ObjectId


@app.route('/api/v1/sec/datags',  methods=['POST'])
@api
def add_tag():
    form = request.form
    parent = form.get('parent', None)
    name = form['tagname']
    createuin = form['createuin']
    scope = form.get('scope', 'pu')
    tag = Tag(name=name, parent=parent,createUIN=createuin, scope=scope, target_type = 'da')
    #tag['_id'] = ObjectId()
    tag.save()
    return tag.to_api(hide_id=False),0
    
@app.route('/api/v1/sec/datags',  methods=['GET'])
@api
def list_all_tag():
    try:
        list = Tag.objects(scope='pu', target_type = 'da')
    except DoesNotExist as e:
        list = []
        
    tags=[tag.to_api(hide_id=False) for tag in list]
    return {'total':len(tags), 'list': tags}, 0
        
    
    
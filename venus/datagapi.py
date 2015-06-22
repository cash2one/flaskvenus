# -*- coding: utf-8 -*-

from flask import request
from mongoengine.errors import DoesNotExist
from .models import IDCounter, Tag
from . import db, idmanager,utils
from .apis import api, APIError, APIValueError
from .apiv1 import apiv1
from bson import ObjectId


@apiv1.route('/sec/datags',  methods=['POST'])
@api
def add_datag():
    form = request.form
    parent = form.get('parent', None)
    name = form['tagname']
    createuin = form['createuin']
    scope = form.get('scope', 'pu')
    tag = Tag(name=name, parent=parent,createUIN=createuin, scope=scope, subject = 'distraction')
    #tag['_id'] = ObjectId()
    tag.save()
    return tag.to_api(hide_id=False),0
    
@apiv1.route('/sec/datags',  methods=['GET'])
@api
def list_all_datag():
    try:
        list = Tag.objects(scope='pu', subject = 'distaction')
    except DoesNotExist as e:
        list = []
        
    tags=[tag.to_api(hide_id=False) for tag in list]
    return {'total':len(tags), 'list': tags}, 0
        
    
    
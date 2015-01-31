# -*- coding: utf-8 -*-

from flask import request
from .models import IDCounter, DAType
from . import app, db, idmanager,utils
from .apis import api, APIError, APIValueError


@app.route('/api/v1/sec/datypes',  methods=['POST'])
@api
def add_type():
    main_type = request.form.get('maintypeid', '0')
    main_type = int(main_type)
    type_name = request.form['subtypename']
    createuin = request.form['createuin']
    sub_type = idmanager.generateDASubType(int(main_type))
    datype = DAType(createUIN=createuin, scope=0)
    datype.settype(type_name,sub_type, main_type)
    datype.save()
    return datype.to_api(),0
    
@app.route('/api/v1/sec/datypes',  methods=['GET'])
@api
def list_all_type():
    list = DAType.objects.all()
    types=[type.to_api() for type in list]
    return {'mainTypeCount':len(types), 'list': types}, 0
        
    
    
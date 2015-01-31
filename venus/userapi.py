# -*- coding: utf-8 -*-

from flask import request
from .models import User
from . import app, db, idmanager,utils
from .apis import api, APIError, APIValueError

@app.route('/api/v1/rest/users',  methods=['POST'])
@api
def register_user():
    name = request.form['name'].strip()
    phone = request.form['phoneNo'].strip().lower()
    password = request.form['password']
    if not name:
        raise APIValueError('name')
    if not phone:
        raise APIValueError('phone')
    if not password:
        raise APIValueError('password')
    
    try:
        user = User.objects.get(phoneNO=phone)
    except DoesNotExist as e:
        user = None
    
    if  user:
        raise APIError(-1, 'phone', 'phone is already in use.')
    
    uin = idmanager.generateUIN()
    user = User(uin=uin, name=name, phoneNO=phone, password=password)
    user.save()
    return user.to_api(), 201

def ensure_admin(request):
    return True

@app.route('/api/v1/rest/users',  methods=['GET'])
@api
def list_users():
    form = request.args
    per_num = int(form.get("maxItemPerPage", "10"))
    from_index = int(form.get("fromIndex", "0"))
    ensure_admin(request)
    users = User.objects.all()
    list = [user.to_api() for user in users]
    page = utils.paginate_list(list, from_index, per_num)
    return page, 0

@app.route('/api/v1/users/<int:uin>',  methods=['DELETE'])
@api
def delete_user():
    ensure_admin(request)
    User.objects.delete(uin=uin)
    return {}, 0
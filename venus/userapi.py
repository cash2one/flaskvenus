# -*- coding: utf-8 -*-

from flask import request
from werkzeug.security import generate_password_hash,check_password_hash
from mongoengine.errors import DoesNotExist
from venus.models import User
from venus import app, db, idmanager,utils, settings
from venus.apis import api, APIError, APIValueError

@app.route('/api/v1/rest/users',  methods=['POST'])
@api
def register_user():
    name = request.form['name'].strip()
    phone = request.form['phone'].strip().lower()
    password = request.form['password']
    avatarurl = request.form.get('avatarurl');
    if not name:
        raise APIValueError('name')
    if not phone:
        raise APIValueError('phone')
    if not password:
        raise APIValueError('password')
    
    try:
        user = User.objects.get(phone=phone)
    except DoesNotExist as e:
        user = None
    
    if  user:
        raise APIError(-1, 'phone', 'phone is already in use.')
    
    uin = idmanager.generateUIN()
    user = User(uin=uin, name=name, phone=phone, _password=generate_password_hash(password), avatar_id = avatarurl)
    user.save()
    return user.to_api(), 201

def get_current_user(request):
    uin = request.cookies.get('uin')
    if uin :
        return User.objects.get(uin=uin)
    
    return None    
        
    
def is_admin(uin):
    user = User.objects.get(uin=uin)
    if user and user.is_admin():
        return True
    return False

def ensure_admin(request):
    uin = request.cookies.get('uin')
    return is_admin(uin)

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

@app.route('/api/v1/rest/users/<int:uin>',  methods=['GET'])
@api
def get_user(uin):
    ensure_admin(request)
    usr = User.objects.get(uin=uin)
    if usr:
        return usr.to_api(), 0
    return 'not found', 404
    

@app.route('/api/v1/rest/users/<int:uin>',  methods=['DELETE'])
@api
def delete_user(uin):
    ensure_admin(request)
    User.objects.delete(uin=uin)
    return {}, 0

@app.route('/api/v1/rest/users/<uin>/avatar',  methods=['POST'])
@api
def set_avatar(uin):
    uin = request.form['uin']
    usr = User.objects.get(uin=uin)
    if(usr):
        usr.avatarId = request.form['avatarurl']
        usr.save()
        return 'ok', 0
    else:
        return 'fail', 404
    
    
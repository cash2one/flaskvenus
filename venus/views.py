
import re, os, base64, hashlib, logging, time, base64,json
from flask import request,g, render_template, make_response, redirect, jsonify, session, Blueprint
from flask.helpers import url_for
import flask_wtf
from werkzeug.security import generate_password_hash,check_password_hash

from bson import json_util
from mongoengine.errors import DoesNotExist
#from flask.ext.httpauth import HTTPBasicAuth

from . import  db
from . import idmanager

from .models import User
from .apiv1 import apiv1
from .apis import api, APIError, APIValueError
from flask.globals import current_app


_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')
_COOKIE_NAME = 'venus'
_COOKIE_KEY = 'venus'

web= Blueprint('web', __name__)

@web.route('/', methods=['GET'])
def index():
    login = request.args.get('logged_in', False)
    return render_template('index.html', title=__name__, content='hello, flask!!', logged_in = login)

@web.route('/register', methods=['GET'])    
def register():            
    upload_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
    files = os.listdir(upload_path)
    return render_template('register.html', filenames = [filename.rsplit('.', 1)[0] for filename in files] )
    
@web.route('/login', methods=['GET'])
def login():
    return render_template('login.html');

@web.route('/logout', methods=['GET'])
def logout():
    response = make_response(render_template('index.html', logged_in = False))
    response.delete_cookie(_COOKIE_NAME)
    session.pop('uin', None)
    return redirect(url_for('apiv1.index'))    

    

@apiv1.route('/login', methods=['POST'])
@api
def authenticate():
    name = request.form['uid'].strip().lower()
    password = request.form['password']
    #bytesString = password.encode(encoding="utf-8")
    #password = base64.encodebytes(bytesString).decode()
    try:
        user = User.objects.get(uin=int(name))
    except DoesNotExist as e:
        raise APIError(-1, 'uid', 'Invalid username.')
        
    if not check_password_hash(user._password, password):
        raise APIError(-1, 'password', 'Invalid password.')

    max_age = 604800
    auth_token = make_signed_cookie(user.id, user._password, max_age)
    #response = make_response(render_template('index.html', logged_in = True, username=user.name))
    #response.set_cookie(_COOKIE_NAME, cookie, max_age=max_age)

    logging.debug(user.name + 'login success!!')
    session['uin']=user.uin
    return user.to_api(), 0


def authenticate_user_token(nick, token):
    pass

@apiv1.before_request
def before_request():
    g.user = None
    if 'uin' in session:
        g.usr= User.objects.with_id(session['uin'])
    
    
@apiv1.errorhandler(404)
@api
def not_found(error):
    return 'not found', 404


# 计算加密cookie:
def make_signed_cookie(id, password, max_age):
    expires = str(int(time.time() + max_age))
    md5Str = '%s-%s-%s-%s' % (id, password, expires, _COOKIE_KEY)
    L = [str(id), str(expires), hashlib.md5(md5Str.encode(encoding="utf-8")).hexdigest()]
    return '-'.join(L)

def user_interceptor(next):
    user = None
    cookie = request.cookies.get(_COOKIE_NAME)
    if cookie:
        user = parse_signed_cookie(cookie)
    request.user = user
    return next()

# 解密cookie:
def parse_signed_cookie(cookie_str):
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        id, expires, md5 = L
        if int(expires) < time.time():
            return None
        user = User.objects.with_id(id)
        if user is None:
            return None
        md5Str = '%s-%s-%s-%s' % (id, user._password, expires, _COOKIE_KEY)
        if md5 != hashlib.md5(md5Str.encode(encoding="utf-8")).hexdigest():
            return None
        return user
    except:
        return None

'''
Created on Dec 30, 2014

@author: lenovo
'''

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_wtf import CsrfProtect
from flask.ext.restful import Api

class MyRestApi(Api):
    def make_response(self, data, *args, **kwargs):
        resp = super(MyRestApi, self).make_response(data, *args, **kwargs)
        content_type = resp.headers['Content-Type']
        if not 'charset' in content_type:
            resp.headers['Content-Type']=content_type+';charset=utf-8'
        return resp

DEFAULT_APP_NAME = 'venus'

db = MongoEngine()
app = Flask(DEFAULT_APP_NAME)
csrf_protect = CsrfProtect(app)
restapi=MyRestApi(app, decorators=[csrf_protect.exempt])
app.config.from_object('venus.settings')


from . import views
from . import userapi
from . import distractiontypeapi
from . import distractionapi
from . import datagapi
from . import tagapi
from . import imageapi
from . import scenicapi
from . import recommendfeedapi
from .resource import FeedTag
from .resource import FocusTimeline
from .resource import Hotspot



    

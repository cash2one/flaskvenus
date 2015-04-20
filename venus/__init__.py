'''
Created on Dec 30, 2014

@author: lenovo
'''

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_wtf import CsrfProtect
from flask.ext.restful import Api


DEFAULT_APP_NAME = 'venus'

db = MongoEngine()
app = Flask(DEFAULT_APP_NAME)
csrf_protect = CsrfProtect(app)
restapi=Api(app, decorators=[csrf_protect.exempt])
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



    

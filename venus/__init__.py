'''
Created on Dec 30, 2014

@author: lenovo
'''

from flask import Flask
from flask.ext.mongoengine import MongoEngine


DEFAULT_APP_NAME = 'venus'

db = MongoEngine()
app = Flask(DEFAULT_APP_NAME)
app.config.from_object('venus.settings')

from . import views
from . import userapi
from . import distractiontypeapi
from . import distractionapi
from . import datagapi
from . import imageapi


    

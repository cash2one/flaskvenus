'''
Created on Dec 30, 2014

@author: lenovo
'''

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_wtf import CsrfProtect
from celery import Celery

DEFAULT_APP_NAME = 'venuscms'

dbs = MongoEngine()
app = Flask(DEFAULT_APP_NAME)
#celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
#celery.conf.update(app.config)
csrf_protect = CsrfProtect(app)
app.config.from_object('cms.settings')

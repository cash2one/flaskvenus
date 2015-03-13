'''
Created on Dec 30, 2014

@author: lenovo
'''

from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object('venus.settings')

def init_app():
    db = MongoEngine(app)
    from . import views
    from . import userapi
    from . import distractiontypeapi
    from . import distractionapi
    from . import datagapi
    from . import imageapi
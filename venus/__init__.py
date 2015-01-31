'''
Created on Dec 30, 2014

@author: lenovo
'''

from flask import Flask, request, render_template,url_for
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object('venus.settings')
db = MongoEngine(app)

from . import views
from . import userapi
from . import distractiontypeapi
from . import distractionapi
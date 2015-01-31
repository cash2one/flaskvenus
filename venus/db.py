# -*- coding: utf-8 -*-

from flask import g
from flask_mongoengine import MongoEngine

def get_db(app):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = MongoEngine(app)
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



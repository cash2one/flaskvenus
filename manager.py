#!/usr/bin/python

import os
from flask_script import Server, Shell, Manager, Command, prompt_bool
from venus import db, create_app
import dbcreate
from flask_mongoengine import Document


app_dir = os.path.join(os.path.dirname(__file__), "venus")

app = create_app('settings_dev.py')
manager = Manager(app)

def _make_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=_make_context))

@manager.command
def createall():
    "Creates database tables"
    dbcreate.create_all()

@manager.command
def dropall():
    "Drops all database tables"
    
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.connection.drop_database(Document._get_db())
        
@manager.command
def migrate():
    "migrate database tables"
    dbcreate.migrate_db()
    
        
if __name__ == "__main__":
    manager.run()
import os, json
import unittest
from venus import app, db, tagapi

class VenusTestCase(unittest.TestCase):

    def setUp(self):
        if not app.config['TESTING']:
            app.config['TESTING'] = True
            app.config.from_pyfile('settings_dev.py')
            db.init_app(app)
            
        self.app = app.test_client()
        
    def tearDown(self):
        pass    
        
    def login(self, username, password):
        return self.app.post('/api/v1/rest/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)
        
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

            



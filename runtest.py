import os, json
import unittest
from venus import app, db, tagapi

class FlaskTestCase(unittest.TestCase):

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

        
        
class TagApiTest(FlaskTestCase):
    
    def test_list_all_feedgroup(self):
        recieve_data = self.app.get('/api/v1/feedgroup')
        json_data = json.loads(recieve_data.data.decode('utf-8'))
        assert json_data['body']['total'] == 3
        
def test_list_all_feedgroup():
    with app.test_request_context('/api/v1/feedgroup', method='GET'):
        recieve_data = tagapi.list_all_feedgroup()
        json_data = json.loads(recieve_data.data.decode('utf-8'))
        assert json_data['body']['total'] == 3
            
if __name__ == '__main__':
    app.config['TESTING'] = True
    app.config.from_pyfile('settings_dev.py')
    db.init_app(app)
    #unittest.main()
    test_list_all_feedgroup()
    db.connection.disconnect()


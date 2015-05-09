import os, json
import unittest
from venus import app, db, tagapi
from venus.test import apitest
import dbcreate

        
def test_list_all_feedgroup():
    with app.test_request_context('/api/v1/feedgroup', method='GET'):
        recieve_data = tagapi.list_all_feedgroup()
        json_data = json.loads(recieve_data.data.decode('utf-8'))
        assert json_data['body']['total'] == 3
            
if __name__ == '__main__':
    app.config['TESTING'] = True
    app.config.from_pyfile('settings_dev.py')
    db.init_app(app)
    dbcreate.init_scenic_feed()
    dbcreate.init_distraction_feed()
    #suite = unittest.TestSuite()  
    #suite.addTest(apitest.TagApiTest('test_list_all_feedgroup'))  
    suite =  unittest.TestLoader().loadTestsFromTestCase(apitest.HotspotResApiTest)  
    unittest.TextTestRunner(verbosity=2).run(suite) 
    #unittest.main(module='venus.test')
    #test_list_all_feedgroup()
    db.connection.disconnect()


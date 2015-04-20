import json
from .venustest import VenusTestCase
from venus import utils

class TagApiTest(VenusTestCase):
    
    def test_list_all_feedgroup(self):
        recieve_data = self.app.get('/api/v1/feedtags')
        json_data = json.loads(recieve_data.data.decode('utf-8'))
        assert json_data['body']['total'] == 3
        
    def test_post(self):
        recieve_data = self.app.post('/api/v1/feedtags', data=dict(name='测试TAG1', createuin=102, scope='pr', subject='scenic', parent='root'))
        json_data = json.loads(recieve_data.data.decode('utf-8'))
        assert json_data['body']['_id'] is not None
        
            
class ScenicApiTest(VenusTestCase):
    def test_add_scenic(self):
        file = open('venus/test/scenic.json', encoding='utf-8')
        post_data= json.load(file)
        file.close()
        recieve_data = self.app.post('/api/v1/sec/scenics', data=dict(post_data))
        json_data = json.loads(recieve_data.data.decode('utf-8'))
        assert json_data['body']['_id'] is not None
        
        recieve_data = self.app.get('/api/v1/sec/scenics?location=102.1, 80.1')
        json_data = json.loads(recieve_data.data.decode('utf-8'))
        assert json_data['body']['totalCount'] > 0


class DAApiTest(VenusTestCase):
    def test_add_da(self):
        file = open('venus/test/distraction.json', encoding='utf-8')
        post_data= json.load(file)
        file.close()
        recieve_data = self.app.post('/api/v1/sec/distractions', data=dict(post_data))
        json_data = json.loads(recieve_data.data.decode('utf-8'))
        assert json_data['body']['_id'] is not None
        
        recieve_data = self.app.get('/api/v1/sec/distractions?location=102.1, 80.1')
        json_data = json.loads(recieve_data.data.decode('utf-8'))
        assert json_data['body']['totalCount'] > 0
     
class RecommendFeddApiTest(VenusTestCase):
    def test_add_feed(self):
        file = open('venus/test/distraction.json', encoding='utf-8')
        post_data= json.load(file)
        file.close()
        recieve_data = self.app.post('/api/v1/sec/distractions', data=dict(post_data))
        json_data = json.loads(recieve_data.data.decode('utf-8')) 
        daid = json_data['body']['_id']
        recieve_data = self.app.post('/api/v1/sec/recommend', data=dict(
                                                 feedid=daid,
                                                 ttlday='10',
                                                 subject='distraction'                       
                                                ))
        json_data = json.loads(recieve_data.data.decode('utf-8'))
        assert json_data['body']['_id'] is not None
        
        file = open('venus/test/scenic.json', encoding='utf-8')
        post_data= json.load(file)
        file.close()
        recieve_data = self.app.post('/api/v1/sec/scenics', data=dict(post_data))
        json_data = json.loads(recieve_data.data.decode('utf-8')) 
        scenicid = json_data['body']['_id'] 
        recieve_data = self.app.post('/api/v1/sec/recommend', data=dict(
                                                 feedid=scenicid,
                                                 ttlday='15',
                                                 subject='scenic'                       
                                                ))
        json_data = json.loads(recieve_data.data.decode('utf-8'))
        assert json_data['body']['_id'] is not None 
        
        recieve_data = self.app.get('/api/v1/sec/recommend')
        json_data = json.loads(recieve_data.data.decode('utf-8'))
        assert json_data['body']['totalCount'] > 0
        
        
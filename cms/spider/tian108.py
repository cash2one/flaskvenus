'''
Created on May 11, 2015

@author: tangwh
'''
import json

from cms import dbs
from cms.model.tian108 import City
from spider.api_web import ApiWeb
from spider.api_task import ApiTask, Crawler

DOMAIN='http://api.108tian.com'
HOME_API = '/mobile/v2/Home?lnglat=113.977334,22.565122&uuid=00000000-794b-eb69-ffff-ffff98cab9f1&channel=baidu'
RecommendDetailList_API='/mobile/v2/RecommendDetailList?cityId=6281&page=0&step=10'
THEMEITEMS_API='/mobile/v2/ThemeItems?type=Event'
THEMEITEMS1_API='/mobile/v2/ThemeItems?type=Pick'
WEEKLYDETAIL_API = '/mobile/v2/WeeklyDetail?id=554c6aee0cf2d45cfc3c4030&channel=baidu'
SCENELIST_API = '/mobile/v2/SceneList?channel=baidu&cityId=6281&page=0&step=20&theme=13'
SCENEDETAIL_API = '/mobile/v2/SceneDetail?id=53b6addee4b01917be0a5f60&channel=baidu'
FARMLIST_API = '/mobile/v2/FarmList?lnglat=112.795604,23.621863&sort=distance&minDistance=0&channel=baidu&step=3'
PICKLIST_API='/mobile/v2/PickList?channel=baidu&cityId=6281&page=0&step=20'

class HomeCrawler(Crawler):
    def save(self, content):
        data = json.loads(content)
        if data['status'] != 0:
            return -1
        
        open_city = data['data']['openCity']
        for province, citydata in open_city.items:
            if  not City.objects.with_id(citydata['id'] ):
                city = City(province=province, id=citydata['id'], name=citydata['name'], city=citydata['city'])
                city.save()

class Tian108(ApiWeb):
    def __init__(self):
        apitask = []
        apitask.append(ApiTask(HOME_API, HomeCrawler, dict(lnglat='113.977334,22.565122')))
        super(Tian108, self).__init__('api.108tian.com', dbs.connection.get('108tian'), apitask)
        
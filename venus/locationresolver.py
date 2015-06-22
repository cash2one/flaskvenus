# -*- coding:utf-8 -*-
from venus.models import Poi
import hashlib, httplib2, json
from urllib.parse import urlencode,quote_plus

BAIDU_VENUS_SK = "LzvELOKlwM66OGZpdApUYtrTA7FopDgj"
BAIDU_VENUS_AK = "4c5OS5cGGjmPr4ERO1gcByk8"
BAIDU_MAP_BASE_URL = "http://api.map.baidu.com/geocoder/v2/?"
BAIDU_GEPCPDER_PATH_TMPL = "/geocoder/v2/?%s" 
MAX_RETRY_NUM = 3


def caculate_baiduSN(query):
    encodeQuery = query + BAIDU_VENUS_SK
    path = quote_plus(BAIDU_GEPCPDER_PATH_TMPL % encodeQuery)
    sn = hashlib.md5(path.encode(encoding="utf-8")).hexdigest()
    return sn
    
def buildQueryUrl(address):
    #TODO: ak param mustbe the end
    query = 'address=%s&output=json&ak=%s'% (quote_plus(address), BAIDU_VENUS_AK)
    query = query + '&sn=' + caculate_baiduSN(query)
    return BAIDU_MAP_BASE_URL + query
        
def parseLocation(content):
    content = json.loads(content)
    if content['status'] == 0 :
        result = content.get('result', None)
        if result and result['location']:
            location = result['location']
            return (location['lng'], location['lat'], content.get('confidence', 0))
        
    raise ValueError        

def _resolve(address):
    #example url:http://api.map.baidu.com/geocoder/v2/?address=%E6%B7%B1%E5%9C%B3%E5%B8%82%E5%8D%97%E5%B1%B1%E5%8C%BA%E6%AC%A7%E9%99%86%E7%BB%8F%E5%85%B8%E5%B0%8F%E5%8C%BA&output=json&ak=4c5OS5cGGjmPr4ERO1gcByk8&sn=eb8dbd5bb1aa227fcf04a338c8cf711f
    qury_url = buildQueryUrl(address)
    for num in range(MAX_RETRY_NUM):
        try:
            response, content = httplib2.Http().request(qury_url)
            if response.status == 200 and content:
                longitude, latitude, confidence = parseLocation(content.decode('utf-8'))
                break
        except :
            raise
    
    return  Poi(address=address, location=[longitude, latitude], confidence=confidence)
                    
def resolve(address, longitude, latitude):
    if  address:
        if  longitude and latitude: 
            return Poi(address=address, location=[longitude, latitude])
        else:
            return _resolve(address)
        
    elif longitude and latitude:
        return Poi(address='unknow', location=[longitude, latitude])
    
    else:
        raise ValueError 
    

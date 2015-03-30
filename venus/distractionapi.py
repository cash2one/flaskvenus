import time, datetime,json
from flask import request
from .models import Distraction, Poi, User, RecommendFeed, Tag
from . import app, db, locationresolver,utils, userapi
from .apis import api, APIError, APIValueError
from bson.son import SON
from django.contrib.gis.measure import Distance
from werkzeug.exceptions import NotFound

EARTH_RADIUS_METERS = 6378137;

@app.route('/api/v1/sec/distractions',  methods=['POST'])
@api
def add_distraction():
    form = request.form
    da = Distraction()
    da.title = form.get('title', None)
    da.description = form.get('description', None)
    da.pay_type = int(form.get('paytype', '0'))
    da.create_user_id = int(form['createuser'])
    da.start_time = utils.timestamp_ms(form['starttime'])
    da.create_time = int(utils.timestamp_ms())
    url_list = form.get('imgurllist', None);
    if url_list :
        da.img_url_list = url_list.split(',')
        
    tag_list_str = form.get('tagIdList', None)
    if tag_list_str :
        da.tag_list = tag_list_str.split(',')
        
    address = form['address'];
    longitude, lantitude = form['location'].split(',')
    da.dst_loc = locationresolver.resolve(address, float(longitude), float(lantitude))
    da.save()
    
    recommend = int(form.get('recommend', '0'))
    if recommend == 1 and userapi.is_admin(da.create_user_id):
        feed = RecommendFeed(feedid=str(da['id']),subject='distraction')
        feed.save()
    return da.to_api(False), 0

def append_distance(da, distance):
    da['_id'] = str(da['_id'])
    da['farawayMeters'] = round(distance)
 
    fill_user_info(da)
    img_url_list = da.get('img_url_list')
    if img_url_list :
        da['imageurl'] = img_url_list[0]
        del da['img_url_list']
    return da

def fill_user_info(da):
    uin = da['createUserId']
    del da['createUserId']
    user = User.objects.get(uin=uin)
    da['createUserInfo'] = {'uin' : uin,
                        'name' : user.name,
                        'headerImgUrl' : user.avatarId,
                        'sexType': user.sexType}
            
@app.route('/api/v1/sec/distractions',  methods=['get'])
@api
def get_nearby_distraction():
    args = request.args
    location_str = args['location']
    location_list = location_str.split(',')
    location = [float(loc) for loc in location_list]
    distance = float(args.get('distanceMeters', '50000.0'))
    per_num = int(args.get("maxItemPerPage", "10"))
    from_index = int(args.get("fromIndex", "0"))
    cmd = SON()
    cmd['geoNear'] = Distraction._get_collection_name()
    cmd['near'] = location
    cmd['maxDistance'] = distance/EARTH_RADIUS_METERS
    cmd['distanceMultiplier'] =EARTH_RADIUS_METERS 
    cmd['spherical'] = True
    dacol = Distraction.objects._collection
    cmd_rs = dacol.database.command(cmd)
    results = cmd_rs['results']
    if(from_index > len(results)):
        raise APIError(-1, from_index, 'start index is great than total')
    
    results = results[from_index:from_index+per_num]
    dalist = [append_distance(result['obj'], result['dis']) for result in results]
    page = utils.paginate_list(dalist, from_index, per_num)
    return page, 0
 
@app.route('/api/v1/sec/distractions/<feedid>',  methods=['get'])
@api
def get_distraction(feedid):   
    distraction = Distraction.objects.with_id(feedid)
    if distraction is None:
        raise NotFound
    
    result = distraction.to_api()
    fill_user_info(result)
    
    result['tag_list'] = []
    for tagid in distraction.tag_list:
        tag = Tag.objects.with_id(tagid)
        if tag: 
            result['tag_list'].append(tag.to_api())
    
    return result, 0   
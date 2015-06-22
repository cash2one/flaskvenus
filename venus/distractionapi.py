import time, datetime,json
from flask import request
from bson.son import SON
from werkzeug.exceptions import NotFound

from .models import Distraction, User, RecommendFeed, Tag, Topic
from . import apiv1, locationresolver,utils, userapi
from .apis import api, APIError
from .apiv1 import apiv1


EARTH_RADIUS_METERS = 6378137;

@apiv1.route('/sec/distractions',  methods=['POST'])
@api
def add_distraction():
    form = request.form
    da = Distraction()
    da.title = form.get('title', None)
    da.description = form.get('description', None)
    da.pay_type = int(form.get('paytype', '0'))
    da.created_by = User.objects.get(uin= int(form['createuser']))
    ts_ms = form.get('starttime', None)
    if ts_ms: 
        da.start_time = datetime.datetime.fromtimestamp(int(ts_ms)/1000)
    url_list = form.get('img_url_list', None);
    if url_list :
        da.img_url_list = url_list.split(',')
        
    tag_list_str = form.get('tag_list', None)
    if tag_list_str :
        tag_list = tag_list_str.split(',')
        da.tag_list = [Tag.objects.with_id(tag_id) for tag_id in tag_list]
        
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
    da['faraway_meters'] = round(distance)
    da['created_by'] = User.objects.with_id(int(da['created_by'])).to_api()  
    if 'topic' in da:
        da['topic'] = Topic.objcets.with_id(da['topic']).name
    
    if'tag_list' in da:
        da['tag_list'] = [Tag.objects.with_id(tag_id).name for tag_id in da['tag_list']]
    img_url_list = da.get('img_url_list')
    if img_url_list :
        da['imgurl'] = img_url_list[0]
        del da['img_url_list']
    return da

            
@apiv1.route('/sec/distractions',  methods=['get'])
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
    #cmd_rs = Distraction.objects(__raw__=cmd.to_dict())
    dacol = Distraction.objects._collection
    cmd_rs = dacol.database.command(cmd)
    results = cmd_rs['results']
    if(from_index > len(results)):
        raise APIError(-1, from_index, 'start index is great than total')
    
    results = results[from_index:from_index+per_num]
    dalist = [append_distance(result['obj'], result['dis']) for result in results]
    page = utils.paginate_list(dalist, from_index, per_num)
    return page, 0
 
@apiv1.route('/sec/distractions/<feedid>',  methods=['get'])
@api
def get_distraction(feedid):   
    distraction = Distraction.objects.with_id(feedid)
    if distraction is None:
        raise NotFound
    
    result = distraction.to_api()
    return result, 0   
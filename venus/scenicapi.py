import time, datetime,json
from flask import request
from werkzeug.exceptions import NotFound
from .models import Poi, Scenic, RecommendFeed, Tag, Distraction
from . import app, db, locationresolver,utils, userapi
from .apis import api, APIError, APIValueError
from bson.son import SON

EARTH_RADIUS_METERS = 6378137;

@app.route('/api/v1/sec/scenics',  methods=['POST'])
@api
def add_scenic():
    form = request.form
    scenic = Scenic()
    scenic.title = form.get('title', None)
    scenic.summary = form.get('summary', None)
    scenic.description = form.get('description', None)
    scenic.create_user_id = int(form['createuser'])
    scenic.create_time = int(utils.timestamp_ms())
    url_str = form.get('imgurllist', None)
    if url_str:
        urllist = url_str.split(',')
        scenic.main_imgurl = urllist[0]
        scenic.others_imgurl = urllist[1:]
        
    address = form['address'];
    location = form['location']
    longitude, lantitude = location.split(',')
    scenic.location = locationresolver.resolve(address, float(longitude), float(lantitude))
    scenic.save()
    
    recommend = int(form.get('recommend', '0'))
    if recommend == 1 and userapi.is_admin(scenic.create_user_id):
        feed = RecommendFeed(feedid=str(scenic['id']),subject='scenic')
        feed.save()
    return scenic.to_api(False), 0

def append_distance(scenic, distance):
    scenic['_id'] = str(scenic['_id'])
    scenic['farawayMeters'] = round(distance)
    return scenic 
            
@app.route('/api/v1/sec/scenics',  methods=['get'])
@api
def get_nearby_scenics():
    args = request.args
    location_str = args['location']
    location_list = location_str.split(',')
    location = [float(loc) for loc in location_list]
    distance = float(args.get('distanceMeters', '50000.0'))
    per_num = int(args.get("maxItemPerPage", "10"))
    from_index = int(args.get("fromIndex", "0"))
    cmd = SON()
    cmd['geoNear'] = Scenic._get_collection_name()
    cmd['near'] = location
    cmd['maxDistance'] = distance/EARTH_RADIUS_METERS
    cmd['distanceMultiplier'] = EARTH_RADIUS_METERS 
    cmd['spherical'] = True
    scenic_coll = Scenic.objects._collection
    cmd_rs = scenic_coll.database.command(cmd)
    results = cmd_rs['results']
    scenics = [append_distance(result['obj'], result['dis']) for result in results]
    page = utils.paginate_list(scenics, from_index, per_num)
    return page, 0
    
@app.route('/api/v1/sec/scenics/<feedid>',  methods=['get'])
@api
def get_scenic(feedid):
    scenic = Scenic.objects.with_id(feedid)
    if scenic is None:
        raise NotFound()
    
    result=scenic.to_api()
    result['tag_list'] = []
    for tagid in scenic.tag_list:
        tag = Tag.objects.get(id=tagid)
        if tag: 
            result['tag_list'].append(tag.to_api())
    
    result['da_list'] =[]
    for daid in scenic.da_list:
        da = Distraction.objects.get(id=daid)
        if da :
            result['da_list'].append(da.to_api())
            
    return result, 0
    
        
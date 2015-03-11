import time, datetime,json
from flask import request
from .models import Distraction, Location
from . import app, db, locationresolver,utils
from .apis import api, APIError, APIValueError
from bson.son import SON
from django.contrib.gis.measure import Distance

EARTH_RADIUS_METERS = 6378137;

@app.route('/api/v1/sec/scenics',  methods=['POST'])
@api
def add_scenic():
    form = request.form
    scenic = Scenic()
    scenic.theme = form.get('theme', None)
    scenic.description = form.get('description', None)
    scenic.create_user_id = int(form['createuser'])
    scenic.create_time = int(utils.timestamp_ms())
    address = form['address'];
    longitude = int(form.get('longitude', 0.0))
    lantitude = int(form.get('lantitude', 0.0))
    scenic.location = locationresolver.resolve(address, longitude, lantitude)
    scenic.save()
    return scenic.to_api(False), 0

def append_distance(scenic, distance):
    scenic['_id'] = str(scenic['_id'])
    scenic['farawayMeters'] = round(distance)
    return scenic
            
@app.route('/api/v1/sec/scenics',  methods=['get'])
@api
def get_scenics():
    args = request.args
    address = args.get('address', None);
    longitude = float(args.get('longitude', 0.0))
    latitude = float(args.get('latitude', 0.0))
    location = locationresolver.resolve(address, longitude, latitude)
    distance = float(args.get('distanceMeters', '50000.0'))
    per_num = int(args.get("maxItemPerPage", "10"))
    from_index = int(args.get("fromIndex", "0"))
    cmd = SON()
    cmd['geoNear'] = Scenic._get_collection_name()
    cmd['near'] = location.location
    cmd['maxDistance'] = distance/EARTH_RADIUS_METERS
    cmd['distanceMultiplier'] = EARTH_RADIUS_METERS 
    cmd['spherical'] = True
    scenic_coll = Scenic.objects._collection
    cmd_rs = scenic_coll.database.command(cmd)
    results = cmd_rs['results']
    scenics = [append_distance(result['obj'], result['dis']) for result in results]
    page = utils.paginate_list(scenics, from_index, per_num)
    return page, 0
    
    
        
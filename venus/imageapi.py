import time, datetime,json
from os import path
from flask import request,url_for, make_response, send_file
from werkzeug import secure_filename
from bson.objectid import ObjectId

from . import app
from .apis import api, APIError, APIValueError

UPLOAD_FOLDER='venus/static/upload'
ALLOW_IMG_IMEI =  set(['image/png', 'image/jpeg'])

def is_image(content_type):
    return content_type in ALLOW_IMG_IMEI

@app.route('/api/v1/image',  methods=['POST'])
@api
def upload_image():
    files = request.files
    image = files['image']

    if is_image(image.content_type):
        ext='png'
        filename = '%s.%s'%(str(ObjectId()), ext) 
        image.save(path.join(UPLOAD_FOLDER, filename))
        return {'url':app.config.get('HOST_BASE') + url_for('get_image', imageid=filename)},0
    else:
        return 'bad request', 400
            
@app.route('/api/v1/image/<imageid>',  methods=['get'])
def get_image(imageid):
        filename = '%s/%s/%s.png'%(path.abspath('.'), UPLOAD_FOLDER, imageid)
        return send_file(filename, mimetype='image/png')

    
    
    
    
        

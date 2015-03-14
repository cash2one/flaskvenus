import time, datetime,json
from os import path
from flask import request,url_for, make_response, send_file
from werkzeug import secure_filename
from bson.objectid import ObjectId

from . import app
from .apis import api, APIError, APIValueError
from flask.helpers import send_from_directory

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
        upload_path = path.join(app.root_path, app.config['UPLOAD_FOLDER'])
        image.save(path.join(upload_path, filename))
        return {'url':app.config.get('VENUS_DOMAIN') + url_for('get_image', imageid=filename)}, 0
    else:
        return 'bad request', 400
            
@app.route('/api/v1/image/<imageid>',  methods=['get'])
def get_image(imageid):
        upload_path = path.join(app.root_path, app.config['UPLOAD_FOLDER'])
        return send_from_directory(upload_path, imageid + '.png')

    
    
    
    
        

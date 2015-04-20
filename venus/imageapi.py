from os import path
from flask import request,url_for, make_response, send_file
from bson.objectid import ObjectId

from venus import app
from .apis import api, APIError, APIValueError
from flask.helpers import send_from_directory

ALLOW_IMG_IMEI =  set(['image/png', 'image/jpeg'])

def is_image(content_type):
    return content_type in ALLOW_IMG_IMEI

@app.route('/api/v1/image',  methods=['POST'])
@api
def upload_image():
    files = request.files
    if files : 
        image = files['image']
        if is_image(image.content_type):
            ext='png'
            filename = '%s.%s'%(str(ObjectId()), ext) 
            upload_path = path.join(app.root_path, app.config['UPLOAD_FOLDER'])
            image.save(path.join(upload_path, filename))
            return {'url':app.config.get('VENUS_DOMAIN') + url_for('get_image', imageid=filename.split('.')[0])}, 0
        else:
            return 'bad request', 400
    else:
        content_type = request.content_type
        ext='png'
        filename = '%s.%s'%(str(ObjectId()), ext) 
        upload_path = path.join(app.root_path, app.config['UPLOAD_FOLDER'])
        savefile = open(path.join(upload_path, filename), 'wb')
        with savefile :
            from shutil import copyfileobj
            copyfileobj(request.stream, savefile, request.content_length)
        return {'url':app.config.get('VENUS_DOMAIN') + url_for('get_image', imageid=filename.split('.')[0])}, 0
        


    
            
@app.route('/api/v1/image/<imageid>',  methods=['get'])
def get_image(imageid):
        upload_path = path.join(app.root_path, app.config['UPLOAD_FOLDER'])
        #利用nginx来读取文件,减小app压力
        #resp = make_response()
        #resp.headers['Content-Type']= 'image/png'
        #resp.headers['X-Accel-Redirect']= path.join(app.root_path, imageid + '.png')
        
        return send_from_directory(upload_path, imageid + '.png')

    
    
    
    
        

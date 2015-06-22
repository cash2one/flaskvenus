# -*- coding: utf-8 -*-

from flask import request, abort
from flask.helpers import url_for
from flask_restful import Resource, reqparse
from flask_mongoengine.wtf.orm import model_form, ModelConverter, converts
from mongoengine.errors import DoesNotExist, InvalidQueryError

from venus.models import Tag, User
from venus import restapi
from venus.resource.ApiResource import ApiResource

ALLOW_TAG_SUBJECT =  set(['album', 'scenic', 'distraction', 'user'])

class MyModelConverter(ModelConverter):
    @converts('LongField')
    def conv_Long(self, model, field, kwargs):
        return self.conv_Int(model, field, kwargs)

class FeedTagListRes(ApiResource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('subject', type = str, required = True,choices=ALLOW_TAG_SUBJECT, 
            help = 'No subject provided', location = 'form')
        
        self.reqparse.add_argument('name', type = str, location = 'form')
        self.reqparse.add_argument('createuin', type = int, location = 'form')
        self.reqparse.add_argument('scope', type = str, choices=('pr', 'pb', 'fr','of'), location = 'form')
        super(FeedTagListRes, self).__init__()
        
    def list_all_taggroup(self):
        scenic_group = dict(name='推荐地点', moreurl=url_for('tags'))     
        tags = Tag.objects(scope='of', subject = 'scenic')
        scenic_group['value'] = [tag.to_api(False) for tag in tags]
        
        da_group = dict(name='活动', moreurl=url_for('tags')) 
        tags = Tag.objects(scope='of', subject = 'distraction')
        da_group['value'] = [tag.to_api(False) for tag in tags]
        
        album_group = dict(name='专题', moreurl=url_for('tags'))
        tags = Tag.objects(scope='of',  subject = 'album')
        album_group['value'] = [tag.to_api(False) for tag in tags]
        feedgroup=[scenic_group, da_group, album_group] 
        return {'total':len(feedgroup), 'list': feedgroup}       
        
    def get(self):
        subject = request.args.get('subject', None)
        if subject is None:
            return self.list_all_taggroup()
        
        if subject not in ALLOW_TAG_SUBJECT:
            abort(404)
            
        try:
            list = Tag.objects(scope='pu', subject = subject)
        except DoesNotExist as e:
            list = []
        
        tags=[tag.to_api(hide_id=False) for tag in list]
        return tags
    
    def post(self):
        args = self.reqparse.parse_args()  
        #field_args={'name':'tagname', 'createUIN':'createuin'}
        tag_form_class = model_form(Tag, 
                                    only=['created_by', 'name', 'parent', 'scope',  'subject'], 
                                    converter=MyModelConverter())
        tag_form = tag_form_class(request.form, **dict( scope='pr'))
        if tag_form.validate():
            tag = Tag()
            tag_form.populate_obj(tag)
            tag.save()
            return tag.to_api(hide_id=False)
        else:
            print(tag_form.errors)
            abort(400, 'Bad request')    

class FeedTagRes(Resource):
    def get(self, id):
        try:
            tag = Tag.objects.with_id(id)
        except InvalidQueryError as e:
            abort(404)
            
        return tag
    

 
    
    
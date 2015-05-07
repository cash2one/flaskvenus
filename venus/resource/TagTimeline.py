# -*- coding: utf-8 -*-

from flask import request, abort
from flask.helpers import url_for
from flask.ext.restful import Resource, reqparse
from mongoengine.errors import DoesNotExist, InvalidQueryError

from venus.models import Tag, Scenic
from venus import app, restapi, utils
from venus.resource.ApiResource import ApiResource

class TagScenicTimelineRes(ApiResource):

    def get(self, tag):
        args = request.args
        per_num = int(args.get("maxItemPerPage", "10"))
        from_index = int(args.get("fromIndex", "0"))
        
        tag_doc = Tag.objects.get(name=tag)
        scenic_list = []
        if tag_doc:
            try:
                scenic_list = Scenic.objects(tag_list__in=[tag_doc])
            except DoesNotExist as e:
                pass
            
        page = utils.paginate_list(scenic_list, from_index, per_num)
        return page


    
restapi.add_resource(TagScenicTimelineRes, '/api/v1/scenic/timeline/tag/<tag>' , endpoint='tag_scenic_timeline')


 
    
    
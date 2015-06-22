# -*- coding: utf-8 -*-

from flask import request, abort
from flask.helpers import url_for
from flask_restful import Resource, reqparse
from mongoengine.errors import DoesNotExist, InvalidQueryError

from venus.models import Tag, Scenic, Topic
from venus import restapi, utils
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
        return dict(page_feed = page, focus_name=tag, followed=0)


    
restapi.add_resource(TagScenicTimelineRes, '/api/v1/scenic/timeline/tags/<tag>' , endpoint='tag_scenic_timeline')

class TopicScenicTimelineRes(ApiResource):

    def get(self, topic):
        args = request.args
        per_num = int(args.get("maxItemPerPage", "10"))
        from_index = int(args.get("fromIndex", "0"))
        
        topic_doc = Topic.objects.get(name=topic)
        scenic_list = []
        if topic_doc:
            try:
                scenic_list = Scenic.objects(topic=topic_doc)
            except DoesNotExist as e:
                pass
            
        page = utils.paginate_list(scenic_list, from_index, per_num)
        return dict(page_feed = page, focus_name=topic, followed=0)
    
restapi.add_resource(TopicScenicTimelineRes, '/api/v1/scenic/timeline/topics/<topic>' , endpoint='topic_scenic_timeline')
 
    
    
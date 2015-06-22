# -*- coding: utf-8 -*-
import datetime
from flask import  abort
from flask.helpers import url_for
from flask.ext.restful import Resource
from mongoengine.errors import DoesNotExist, InvalidQueryError

from venus.models import Tag, Topic, HotFocus
from venus import  restapi, utils
from venus.resource.ApiResource import ApiResource


class HotspotRes(ApiResource):

    def get(self):
        hotfocus_list = HotFocus.objects.all()
        tag_list = []
        topic_list = []
        for hot in hotfocus_list:
            if datetime.datetime.now().date()  > hot.create_time.date() + datetime.timedelta(days=hot._ttl_day):
                hot.delete()
            elif isinstance(hot.focus, Topic):
                topic_list.append(hot.focus.to_api())
            elif  isinstance(hot.focus, Tag):
                tag_list.append(hot.focus.to_api())

        return dict(topics=topic_list, tags=tag_list)


    
restapi.add_resource(HotspotRes, '/api/v1/hotspot' , endpoint='hotspot')


 
    
    
import time, datetime,json
from flask import request
from mongoengine.errors import DoesNotExist
from .models import Distraction, User, RecommendFeed, Scenic, Distraction, Topic
from . import app, db,utils
from .apis import api, APIError, APIValueError


@app.route('/api/v1/sec/recommend',  methods=['POST'])
@api
def add_recommend_feed():
    form = request.form
    feed = RecommendFeed()
    feed.feedid=form['feedid']
    feed.subject=form['subject']
    feed._ttl_day = int(form.get('ttlday', '5'))
    feed.create_time = int(utils.timestamp_ms())
    feed.save()
    return feed.to_api(False), 0


class Feed(object):
    def __init__(self,id, title, summary, imgurl, subject):
        self.id=str(id)
        self.title = title
        self.summary = summary
        self.imgurl=imgurl
        self.subject=subject
        
    def to_api(self):
        return self.__dict__
            
@app.route('/api/v1/sec/recommend',  methods=['get'])
@api
def get_all_recommend_feed():
    args = request.args
    city = args.get('city', "深圳")
    per_num = int(args.get("maxItemPerPage", "10"))
    from_index = int(args.get("fromIndex", "0"))
    
    feedlist=[]
    try:
        list = RecommendFeed.objects.all()
        
        for recommend in list :
            if 'distraction' == recommend.subject:
                da = Distraction.objects.with_id(recommend.feedid)
                if da is None:
                    continue
                if da.img_url_list :
                    imgurl=da.img_url_list[0] 
                else:
                    imgurl=None 
                feedlist.append( Feed(da.id, da.title, da.description, imgurl, 'distraction').to_api())
            elif 'scenic' == recommend.subject:
                scenic = Scenic.objects.get(id=recommend.feedid)
                if scenic is None:
                    continue
                feedlist.append(Feed(scenic.id, scenic.title, scenic.summary, scenic.main_imgurl, 'scenic').to_api())
            elif 'topic' == recommend.subject:
                topic = Topic.objects.with_id(recommend.feedid)
                if topic is None:
                    continue
                feedlist.append(Feed(topic.id, topic.title, topic.summary, topic.imgurl, 'topic').to_api())
                
    except DoesNotExist as e:
        pass
    
    page = utils.paginate_list(feedlist, from_index, per_num)
    return page, 0
    
    
        
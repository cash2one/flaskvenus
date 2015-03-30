from venus import app,  db
import os,json
from venus.models import IDCounter, User, Tag, Scenic, RecommendFeed, Distraction

    

#迁移老数据库
def migrate_db():
    pass

def init_user():
    uinCounter = IDCounter(key='uin', value='10000')
    uinCounter.save();
    
    user = User(uin=101, name='admin101', phoneNO='13760480101', _password='123456', role=User.ADMIN, avatarId='http://120.24.208.105/venus/api/v1/image/header1')
    user.save()
    user = User(uin=102, name='admin102', phoneNO='13760480102', _password='123456', role=User.ADMIN, avatarId='http://120.24.208.105/venus/api/v1/image/header2')
    user.save()
    user = User(uin=103, name='admin103', phoneNO='13760480103', _password='123456', role=User.ADMIN, avatarId='http://120.24.208.105/venus/api/v1/image/header3')
    user.save()
    
def init_tag():
    tag = Tag(name='排行榜', createUIN=101, scope='of', subject = 'topic')
    tag.save()
    tag = Tag(name='推荐', createUIN=101, scope='of', subject = 'topic')
    tag.save()
    
    tag = Tag(name='自然风景', createUIN=101, scope='of', subject = 'scenic')
    tag.save()
    tag = Tag(name='人文古迹', createUIN=101, scope='of', subject = 'scenic')
    tag.save()
    tag = Tag(name='商家', createUIN=101, scope='of', subject = 'scenic')
    tag.save()
    
    tag = Tag(name='发呆', createUIN=101, scope='pu', subject = 'scenic')
    tag.save()  
    tag = Tag(name='情侣约会', createUIN=101, scope='pu', subject = 'scenic')
    tag.save()
    tag = Tag(name='拍照',createUIN=101, scope='pu', subject = 'scenic')
    tag.save()
    tag = Tag(name='遛娃', createUIN=101, scope='pu', subject = 'scenic')
    tag = Tag(name='高颜值', createUIN=101, scope='pu', subject = 'scenic')
    tag.save()

    tag = Tag(name='户外活动', createUIN=101, scope='of', subject = 'distraction')
    tag.save() 
    tag = Tag(name='朋友聚会', createUIN=101, scope='of', subject = 'distraction')
    tag.save()
    tag = Tag(name='优惠券', createUIN=101, scope='of', subject = 'distraction')
    tag.save()
    
    tag = Tag(name='徒步穿越', createUIN=101, scope='pu', subject = 'distraction')
    tag.save() 
    tag = Tag(name='爬山', createUIN=101, scope='pu', subject = 'distraction')
    tag.save() 
    tag = Tag(name='钓鱼', createUIN=101, scope='pu', subject = 'distraction')
    tag.save()  
    tag = Tag(name='暖男', createUIN=101, scope='pu', subject = 'distraction')
    tag.save()
    tag = Tag(name='累觉不爱', createUIN=101, scope='pu', subject = 'distraction')
    tag.save()

def init_scenic_feed():
    scenic_data_base = 'venus/static/data/scenic'
    scenic_list = os.listdir(path=scenic_data_base)
    for name in scenic_list:
        file = open(os.path.join(scenic_data_base, name), encoding='utf-8')
        scenic = Scenic.from_json(file.read())
        file.close()
        scenic.tag_list=[str(tag.id) for tag in Tag.objects(scope='pu', subject='scenic')]
        scenic.save()
        recommend = RecommendFeed(feedid=str(scenic.id), subject='scenic')
        recommend.save()
        
def init_distraction_feed():
    da_data_base = 'venus/static/data/distraction'
    da_list = os.listdir(path=da_data_base)
    for name in da_list:
        file = open(os.path.join(da_data_base, name), encoding='utf-8')
        distraction = Distraction.from_json(file.read())
        file.close()
        distraction.tag_list=[str(tag.id) for tag in Tag.objects(scope='pu', subject='distraction')]
        distraction.save()
        recommend = RecommendFeed(feedid=str(distraction.id), subject='distraction')
        recommend.save()
    
def create_all():
    version = IDCounter(key='db_version', value=1)
    version.save()
    init_user()
    init_tag()
    init_scenic_feed()
    init_distraction_feed()

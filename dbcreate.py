from venus import app,  db
from venus.settings import MONGODB_SETTINGS
import os.path
from venus.models import IDCounter, User, Tag

    

#迁移老数据库
def migrate_db():
    pass

def init_user():
    uinCounter = IDCounter(key='uin', value='10000')
    uinCounter.save();
    
    user = User(uin=101, name='admin101', phoneNO='13760480101', _password='123456', role=User.ADMIN)
    user.save()
    user = User(uin=102, name='admin102', phoneNO='13760480102', _password='123456', role=User.ADMIN)
    user.save()
    user = User(uin=103, name='admin103', phoneNO='13760480103', _password='123456', role=User.ADMIN)
    user.save()
    
def init_tag():
    tag = Tag(name='排行榜', parent='root',createUIN=101, scope='pu', target_type = 'topic')
    tag.save()
    tag = Tag(name='推荐', parent='root',createUIN=101, scope='pu', target_type = 'topic')
    tag.save()
    
    tag = Tag(name='自然风景', parent='root',createUIN=101, scope='pu', target_type = 'scenic')
    tag.save()
    tag = Tag(name='人文古迹', parent='root',createUIN=101, scope='pu', target_type = 'scenic')
    tag.save()
    tag = Tag(name='商家', parent='root',createUIN=101, scope='pu', target_type = 'scenic')
    tag.save()
    
    tag = Tag(name='遛娃', parent='root',createUIN=101, scope='pu', target_type = 'distraction')
    tag.save()
    tag = Tag(name='摄影', parent='root',createUIN=101, scope='pu', target_type = 'distraction')
    tag.save()
    tag = Tag(name='钓鱼', parent='root',createUIN=101, scope='pu', target_type = 'distraction')
    tag.save()  
    tag = Tag(name='发呆', parent='root',createUIN=101, scope='pu', target_type = 'distraction')
    tag.save()  
    tag = Tag(name='情侣约会', parent='root',createUIN=101, scope='pu', target_type = 'distraction')
    tag.save()
    tag = Tag(name='朋友聚会', parent='root',createUIN=101, scope='pu', target_type = 'distraction')
    tag.save()


def create_all():
    version = IDCounter(key='db_version', value=1)
    version.save()
    init_user()
    init_tag()

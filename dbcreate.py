from venus import db
from venus.settings import MONGODB_SETTINGS
import os.path

if(os.path.exists(MONGODB_SETTINGS['DB'])):
    migrate_db()
else :
    pass

#迁移老数据库
def migrate_db():
    pass

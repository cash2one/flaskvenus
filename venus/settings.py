DEBUG = True

#这是一个危险的操作!!!!!!!!
WTF_CSRF_ENABLED = False
#JSON_AS_ASCII=False能输出中文字串,不然中文字串件会以"\u535a\u5ba2\u56ed"形式输出
JSON_AS_ASCII = False 

SECRET_KEY = 'sdfsdf82347$$%$%$%$&fsdfs!!ASx+__WEBB$'

ADMIN=[101, 102,103]
VENUS_DOMAIN='www.funnycity.cn'

UPLOAD_FOLDER='/alidata/www/upload'

"""
DB in remote host
- register for free in venus
"""
MONGODB_SETTINGS = {'DB': "wlkqnuQHpoaIYnLikclm",
                     'USERNAME': '4c5OS5cGGjmPr4ERO1gcByk8',
                     'PASSWORD': 'LzvELOKlwM66OGZpdApUYtrTA7FopDgj',
                     'HOST': '10.170.1.11',
                     'PORT': 27017}

QQ_APP_ID = '101187283'
QQ_APP_KEY = '993983549da49e384d03adfead8b2489'

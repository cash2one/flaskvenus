

DEBUG = True

#这是一个危险的操作!!!!!!!!
WTF_CSRF_ENABLED = False
#JSON_AS_ASCII=False能输出中文字串,不然中文字串件会以"\u535a\u5ba2\u56ed"形式输出
JSON_AS_ASCII = False 

SECRET_KEY = 'sdfsdf82347$$%$%$%$&fsdfs!!ASx+__WEBB$'

ADMIN=[101, 102,103]
VENUS_DOMAIN='www.funnycity.cn'

UPLOAD_FOLDER='/alidata/www/cms/upload'

"""
DB in remote host
- register for free in venus
"""
TIAN108_DB_SETTING = {'alias': '108tian', 
                    'DB': '108tian',
                    'USERNAME': 'funnycity',
                    'PASSWORD': 'junjiyule',
                    'HOST': '127.0.0.1',
                    'PORT': 27017}

XIANV_DB_SETTING = {'alias': 'xianv',
                    'DB': "xianv",
                    'USERNAME': 'funnycity',
                    'PASSWORD': 'junjiyule',
                    'HOST': '127.0.0.1',
                    'PORT': 27017}

MONGODB_SETTINGS = [TIAN108_DB_SETTING, XIANV_DB_SETTING]

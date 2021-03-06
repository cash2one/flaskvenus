# -*- coding:utf-8 -*-
"""
    author sarike@timefly.cn
"""
import string
import random
import hashlib, time
from flask_mongoengine import Pagination
from venus.models import ApiDocument, User

def random_key():
    return ''.join([random.choice(string.letters) for i in xrange(48)])

def hashPassword(password):
    """Hash the user password.

    Args:
        password : the user input password.
    Returns:
        the password with md5 hashable

    """
    not_empty(password)
    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()



def paginate_list(content_list, from_index=0, per_page=10):
    paginator = Pagination(content_list, int(from_index/per_page + 1), per_page)
    content_list =[item.to_api() if  isinstance(item,(ApiDocument, User))  else item for item in paginator.items]
    return {'total': paginator.total, 'from': (paginator.page - 1) * paginator.per_page,
             'list': [item for item in content_list]}
    
def timestamp_ms(time_str=None):
    if time_str:
        time_array = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        #转换为时间戳:
        time_second = time.mktime(time_array)
    else:
        time_second = time.time()
    return round(time_second*1000)


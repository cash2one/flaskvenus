# -*- coding: utf-8 -*-

import logging
from venus.models import IDCounter


def generateUIN() -> int:
    #这样做有问题,不是原子操作,可能需要直接用mongopy原collection函数findAndModify来实现
    result = IDCounter.objects.filter(idName='uin').update_one(inc__idValue=1, upsert=True)
    if result > 0 :
        uin = IDCounter.objects.get(idName='uin').value
    logging.debug('generateUIN:' + uin)
    return uin

def generateDASubType(mainType:int) -> int:
    result = IDCounter.objects.filter(idName='datype', main=mainType).update_one(set__main=mainType,inc__idValue=1, upsert=True)
    if result > 0:
        sub = IDCounter.objects.get(idName='datype', main=mainType).value
     
    logging.debug('generateDASubType:%d'%sub)
    return sub
    
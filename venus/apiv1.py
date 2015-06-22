# -*- coding:utf-8 -*-

from flask import jsonify, Blueprint
from .apis import api, APIError

apiv1= Blueprint('apiv1', __name__)

@apiv1.errorhandler(400)
@api
def invalidate_param(error):
    return 'invalidate paramters', 400

@apiv1.errorhandler(APIError)
def handle_invalid_usage(error):
    return jsonify(error.to_dict())

#关联路由与Blueprint
from . import views
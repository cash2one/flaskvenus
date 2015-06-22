# -*- coding: utf-8 -*-

from flask import request, abort
from flask_restful import Resource
from venus import restapi
from venus.apis import jsonify

@restapi.representation('application/json')
def output_json(data, code, headers=None):
    resp = jsonify(data)
    if headers:
        resp.headers.extend(headers)
        
    return resp

    
class ApiResource(Resource):
    def dispatch_request(self, *args, **kwargs):
        data = super(ApiResource, self).dispatch_request(*args, **kwargs)
        return dict(statecode=0, stateDescription='success', body=data)


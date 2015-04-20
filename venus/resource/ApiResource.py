# -*- coding: utf-8 -*-

from flask import request, abort
from flask.ext.restful import Resource

class ApiResource(Resource):
    def dispatch_request(self, *args, **kwargs):
        data = super(ApiResource, self).dispatch_request(*args, **kwargs)
        return dict(statecode=0, stateDescription='success', body=data)


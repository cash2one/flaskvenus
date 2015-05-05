#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'tangwh'

import re,logging, functools
from flask import make_response, json
from flask.globals import current_app, request

#仿照josn.jsonity,只是在content_type 加入了charset=utf8
def jsonify(*args, **kwargs):
    indent = None
    if current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] \
        and not request.is_xhr:
        indent = 2
    return current_app.response_class(json.dumps(dict(*args, **kwargs),
        indent=indent),
        mimetype='application/json', content_type='application/json; charset=utf8')
    
class APIError(Exception):
    '''
    the base APIError which contains error(required), data(optional) and message(optional).
    '''
    def __init__(self, error= 400,  message='', payload=None):
        super(APIError, self).__init__(message)
        self.error = error
        self.message = message
        self.payload = payload


class APIValueError(APIError):
    def __init__(self, message='invalid value', payload=None):
        super(APIValueError, self).__init__(401, message, payload)

class APIResourceNotFoundError(APIError):
    def __init__(self, message='not found'):
        super(APIResourceNotFoundError, self).__init__(404, message)

class APIPermissionError(APIError):
    def __init__(self, message='permission forbidden'):
        super(APIPermissionError, self).__init__(402, message)


def api(func):
    '''
    A decorator that makes a function to json api, makes the return value as json.

    @app.route('/api/test')
    @api
    def api_test():
        return dict(result='123', items=[])
    '''
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        try:
            data, code = func(*args, **kw);
            body= dict(statecode=code, stateDescription='success', body=data)
        except APIError as e:
            body = dict(statecode=e.error, stateDescription=e.message, body=e.payload)
        except ValueError as e:
            body = dict(statecode=403, stateDescription='program error!')
        except Exception as e:
            logging.exception(e)
            body = dict(statecode=403, stateDescription='internalerror')
            
        response = jsonify(body)
        return response
    
    return _wrapper


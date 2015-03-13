#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'tangwh'

import re, json, logging, functools
from flask import make_response

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
            r = json.dumps(dict(statecode=code, stateDescription='success', body=data))
        except APIError as e:
            r = json.dumps(dict(statecode=e.error, stateDescription=e.message, body=e.payload))
        except Exception as e:
            logging.exception(e)
            r = json.dumps(dict(statecode=403, stateDescription='internalerror'))
        response = make_response(r) 
        response.headers.extend({'Content-Type': 'application/json'})  
        return response
    
    return _wrapper


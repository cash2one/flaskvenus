import os
import json
from flask import Flask, redirect, url_for, session, request, jsonify, Markup
from flask_oauthlib.client import OAuth
from .models import User
from . import  db
from .apiv1 import apiv1


def configure(apiv1):
    qq = oauth.remote_apiv1(
        'qq',
        consumer_key=apiv1.config['QQ_APP_ID'],
        consumer_secret=apiv1.config['QQ_APP_KEY'],
        base_url='https://graph.qq.com',
        request_token_url=None,
        request_token_params={'scope': 'get_user_info'},
        access_token_url='/oauth2.0/token',
        authorize_url='/oauth2.0/authorize',
        )
    setattr(apiv1, 'oauth_qq', qq)
    
def get_oauth_apiv1(provider):
    provider_name = "oauth_" + provider
    return getattr(current_apiv1, provider_name, None)

#qq=functools.partial(get_oauth_apiv1, 'qq')
qq=lambda:get_oauth_apiv1('qq')

def json_to_dict(x):
    '''OAuthResponse class can't not parse the JSON data with content-type
    text/html, so we need reload the JSON data manually'''
    if x.find('callback') > -1:
        pos_lb = x.find('{')
        pos_rb = x.find('}')
        x = x[pos_lb:pos_rb + 1]
    try:
        return json.loads(x, encoding='utf-8')
    except:
        return x


def update_qq_api_request_data(data={}):
    '''Update some required parameters for OAuth2.0 API calls'''
    defaults = {
        'openid': session.get('qq_openid'),
        'access_token': session.get('qq_token')[0],
        'oauth_consumer_key': QQ_APP_ID,
    }
    defaults.update(data)
    return defaults


@apiv1.route('/')
def index():
    '''just for verify website owner here.'''
    return Markup('''<meta property="qc:admins" '''
                  '''content="226526754150631611006375" />''')


@apiv1.route('/user_info')
def get_user_info():
    if 'qq_token' in session:
        data = update_qq_api_request_data()
        resp = qq.get('/user/get_user_info', data=data)
        return jsonify(status=resp.status, data=resp.data)
    return redirect(url_for('login'))


@apiv1.route('/login')
def login():
    return qq.authorize(callback=url_for('authorized', _external=True))


@apiv1.route('/logout')
def logout():
    session.pop('qq_token', None)
    return redirect(url_for('get_user_info'))


@apiv1.route('/login/authorized')
def authorized():
    resp = qq.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['qq_token'] = (resp['access_token'], '')

    # Get openid via access_token, openid and access_token are needed for API calls
    resp = qq.get('/oauth2.0/me', {'access_token': session['qq_token'][0]})
    resp = json_to_dict(resp.data)
    if isinstance(resp, dict):
        session['qq_openid'] = resp.get('openid')

    return redirect(url_for('get_user_info'))


@qq.tokengetter
def get_qq_oauth_token():
    return session.get('qq_token')

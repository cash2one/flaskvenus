from threading import Lock
from werkzeug.wsgi import pop_path_info, peek_path_info
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
import logging
from logging.handlers import RotatingFileHandler
from venus import create_app
from venus import db as venusdb
from cms import app as cmsapp
from cms import dbs as cmsdb

class SubdomainDispatcher(object):

    def __init__(self, domain, create_app):
        self.domain = domain
        self.create_app = create_app
        self.lock = Lock()
        self.instances = {}

    def get_application(self, host):
        host = host.split(':')[0]
        assert host.endswith(self.domain), 'Configuration error'
        subdomain = host[:-len(self.domain)].rstrip('.')
        with self.lock:
            app = self.instances.get(subdomain)
            if app is None:
                app = self.create_app(subdomain)
                self.instances[subdomain] = app
            return app

    def __call__(self, environ, start_response):
        app = self.get_application(environ['HTTP_HOST'])
        return app(environ, start_response)
    
class PathDispatcher(object):

    def __init__(self, default_app, create_app):
        self.default_app = default_app
        self.create_app = create_app
        self.lock = Lock()
        self.instances = {}

    def get_application(self, prefix):
        with self.lock:
            app = self.instances.get(prefix)
            if app is None:
                app = self.create_app(prefix)
                if app is not None:
                    self.instances[prefix] = app
            return app

    def __call__(self, environ, start_response):
        app = self.get_application(peek_path_info(environ))
        if app is not None:
            pop_path_info(environ)
        else:
            app = self.default_app
        return app(environ, start_response)

def make_app(prefix):
    if prefix == 'venus':
        return venusapp
    elif prefix == 'cms':
        return cmsapp  #cms_app还不存在,暂时用app来替代
    return None

def init_logger(app, filename):
        file_handler = RotatingFileHandler(filename, 'a', 1 * 1024 * 1024, 10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
    
    
if __name__ == '__main__':
    venusapp = create_app('settings_dev.py')
    #venusapp.run(debug=venusapp.config['DEBUG'], host='0.0.0.0',port=80)
    
    application = PathDispatcher(venusapp, make_app)
    #application = DispatcherMiddleware(app, {'/venus': venusapp, '/cms' : cmsapp});
    run_simple('0.0.0.0', 80, application, use_reloader=True, use_debugger=venusapp.config['DEBUG'])
else :
    venusapp = create_app()
    init_logger(venusapp, '/var/log/venus.log')
    app = DispatcherMiddleware(venusapp, {'/venus': venusapp, '/cms' : cmsapp})

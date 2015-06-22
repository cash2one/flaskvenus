'''
Created on Dec 30, 2015

@author: tangwh
'''

import logging
import urllib
from werkzeug.urls import url_decode, url_encode

class Crawler():
    
    def build_url(self, url_temple, **kwargs):
        base, query = url_temple.split('?', 1)
        query = url_decode(query, cls=dict)
        query.update(kwargs)
        return base + '?' + url_encode(query)

    def fetch_content(self,url):
        logging.debug('fetch url:' + url)
        try:
            urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            logging.error(e)
            
    def save(self, url, content):
        pass
    
class ApiTask():
    abstract = True
    
    def __init__(self, path_temple, crawler,  **kwargs):
        self.url_temple = path_temple
        self.crawler = crawler
        
    def excute(self, domain):
        
        pass
    
    def next(self):
        pass







    

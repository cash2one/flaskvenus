'''
Created on Dec 30, 2015

@author: tangwh
'''

from .api_task import ApiTask

class ApiWeb():
    def __init__(self, name, db, tasks):
        self.name = name
        self.db = db
        self.tasks = tasks
        
    def login(self):
        self.access_token=None
            
    def crawl(self):
        for task in self.tasks:
            if isinstance(task, ApiTask):
                task.excute();
                
    

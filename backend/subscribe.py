from req import RequestHandler
from req import reqenv
from req import Service

class SubscribeHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render('subscribe.html')
        return
    @reqenv 
    def post(self):
        return

class SubscribeService:
    def __init__(self, db):
        self.db = db
        SubscribeService.inst = self



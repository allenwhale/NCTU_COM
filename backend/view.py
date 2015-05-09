from req import RequestHandler
from req import reqenv
from req import Service

class ViewHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render('view.html')
        return
    @reqenv 
    def post(self):
        return

class ViewService:
    def __init__(self, db):
        self.db = db
        ViewService.inst = self

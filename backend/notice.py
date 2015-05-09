from req import RequestHandler
from req import reqenv
from req import Service

class NoticeHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render('notice.html')
        return
    @reqenv 
    def post(self):
        return

class NoticeService:
    def __init__(self, db):
        self.db = db
        NoticeService.inst = self

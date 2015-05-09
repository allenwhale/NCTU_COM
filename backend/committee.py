from req import RequestHandler
from req import reqenv
from req import Service

class CommitteeHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render('committee.html')
        return
    @reqenv 
    def post(self):
        return

class CommitteeService:
    def __init__(self, db):
        self.db = db
        CommitteeService.inst = self

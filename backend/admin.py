from req import RequestHandler
from req import reqenv

class AdminService:
    def __init__(self, db):
        self.db = db
        AdminService.inst = self


class AdminRequestHandler(RequestHandler):
    @reqenv
    def get(self):
        return
    @reqenv
    def post(self):
        return

from req import RequestHandler
from req import reqenv

class AdminService:
    def __init__(self, db):
        self.db = db
        AdminService.inst = self


class AdminHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render("admin.html")
        return
    @reqenv
    def post(self):
        return

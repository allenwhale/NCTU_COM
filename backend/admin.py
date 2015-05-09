from req import RequestHandler
from req import reqenv
import config

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
        req = self.get_argument('req', None)
        if req == 'isadmin':
            res = 1 if self.acct['uid'] in config.ADMIN_RANGE else 0
            self.finish(str(res))
        return

from req import RequestHandler
from req import reqenv
class LoginService:
    def __init__(self, db):
        self.db = db
        LoginService.inst = self


class LoginHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render('login.html')
        return

    @reqenv
    def post(self):
        pass


from req import RequestHandler
from req import reqenv
from req import Service

class ContactHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render('contact.html')
        return
    @reqenv 
    def post(self):
        return

class ContactService:
    def __init__(self, db):
        self.db = db
        ContactService.inst = self

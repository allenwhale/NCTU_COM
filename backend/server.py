import tornado.ioloop
import tornado.web
import pg
import config
from req import RequestHandler
from req import reqenv
from req import Service
from login import LoginHandler
from login import LoginService
from register import RegisterHandler
from register import RegisterService
from login import ModifyuserHandler
from paperupload import PaperuploadHandler
from paperupload import PaperuploadService
from showpaper import ShowpaperHandler
from showpaper import ShowpaperService
from admin import AdminService
from admin import AdminHandler
from committee import CommitteeHandler
from committee import CommitteeService
from notice import NoticeHandler
from notice import NoticeService
from subscribe import SubscribeHandler
from subscribe import SubscribeService
from contact import ContactHandler
from contact import ContactService
from view import ViewHandler
from view import ViewService

class IndexHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render('index.html')
        return

if __name__ == '__main__':
    db = pg.AsyncPG(config.DBNAME, config.DBUSER, config.DBPASSWORD, host=config.DBHOST, dbtz='+8')
    app = tornado.web.Application([
        ('/', IndexHandler),
        ('/login', LoginHandler),
        ('/register', RegisterHandler),
        ('/modifyuser', ModifyuserHandler),
        ('/paperupload', PaperuploadHandler),
        ('/showpaper', ShowpaperHandler),
        ('/admin', AdminHandler),
        ('/committee', CommitteeHandler),
        ('/notice', NoticeHandler),
        ('/subscribe', SubscribeHandler),
        ('/contact', ContactHandler),
        ('/view', ViewHandler),
        ('/(.*)', tornado.web.StaticFileHandler, {'path': '../html'}),
        ], cookie_secret=config.COOKIE_SECRET, autoescape='xhtml_escape')
    app.listen(config.PORT)
    Service.Login = LoginService(db)
    Service.Register = RegisterService(db)
    Service.Paperupload = PaperuploadService(db)
    Service.Showpaper = ShowpaperService(db)
    Service.Admin = AdminService(db)
    tornado.ioloop.IOLoop().instance().start()

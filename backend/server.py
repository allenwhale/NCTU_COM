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

class IndexHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render('index.html')
        return

if __name__ == '__main__':
    db = pg.AsyncPG(config.DBNAME, config.DBUSER, config.DBPASSWORD, dbtz='+8')
    app = tornado.web.Application([
        ('/', IndexHandler),
        ('/login', LoginHandler),
        ('/register', RegisterHandler),
        ('/modify_user', ModifyuserHandler),
        ('/(.*)', tornado.web.StaticFileHandler, {'path': '../html'}),
        ], cookie_secret=config.COOKIE_SECRET, autoescape='xhtml_escape')
    app.listen(config.PORT)
    Service.Login = LoginService(db)
    Service.Register = RegisterService(db)
    tornado.ioloop.IOLoop().instance().start()

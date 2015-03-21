from req import RequestHandler
from req import reqenv
class LoginService:
    def __init__(self, db):
        self.db = db
        LoginService.inst = self

    def signin(self, email, password):
        def _hash(p):
            ret = 1048576
            MOD = 10000000007
            C = 213
            for i in p:
                ret = (ret * C + ord(i)) % MOD
            return ret
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "account"."password" "account"."uid" FROM "account" '
                'WHERE "account"."email" = %s;', (email,))
        if cur.rowcount != 1:
            return ('Enoexist', None)
        meta = cur.fetchone()
        if _hash(password) != meta[0]:
            return ('Epassword', None)
        return (None, meta[1])

    def changepassword(self, email, password, newpassword, repassword):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "account"."password" "account"."uid" FROM "account" '
                'WHERE "account"."email" = %s;', (email,))
        if cur.rowcount != 1:
            return ('Enoexist', None)
        meta = cur.fetchone()
        if _hash(password) != meta[0]:
            return ('Epassword', None)
        if newpassword != repassword:
            return ('Enewpassword')
        yield cur.execute('UPDATE "account" SET "account"."password" = %s ')

class LoginHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render('login.html')
        return

    @reqenv
    def post(self):
        req = str(self.get_argument('req'))
        if req == 'signin':
            try:
                email = str(self.get_argument('email'))
                password = str(self.get_argument('password'))
            except:
                self.finish('E')
                return
            err, uid = yield from LoginService.inst.signin(email, password)
            if err:
                self.finish(err)
                return
            self.finish('S')
            return
        elif req == 'changepassword':
            try: 
                email = str(self.get_argument('email'))
                password = str(self.get_argument('password'))
                newpassword = str(self.get_argument('newpassword'))
                repassword = sstr(self.get_argument('repassword'))
            except:
                 self.finish('E')
                 return




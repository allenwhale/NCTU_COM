from req import RequestHandler
from req import reqenv
class RegisterService:
    def __init__(self, db):
        self.db = db
        RegisterService.inst = self

    def signup(self, email, password, repassword):
        if password != repassword:
            return ('Epassword', None)
        def _hash(p):
            ret = 1048576
            MOD = 10000000007
            C = 213
            for i in p:
                ret = (ret * C + ord(i)) % MOD
            return ret

        cur = yield self.db.cursor()
        yield cur.execute('SELECT 1 FROM "account" '
                'WHERE "account"."email" = %s;', (email, ))
        if cur.rowcount != 0:
            return ('Eexist', None)
        yield cur.execute('INSERT INTO "sccount" '
                '( "email", "password") '
                'VALUES ( %s ,%s) '
                'RETURNING "account"."uid";', (email, _hash(password)))
        if cur.rowcount != 1:
            return ('Edb', None)
        uid = str(cur.fetchone()[0])
        return (None, str(uid))


class RegisterHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render('register.html')
        return

    @reqenv
    def post(self):
        try:
            email = str(self.get_argument('email'))
            password = str(self.get_argument('password'))
            repassword = str(self.get_argument('repassword'))
        except:
            self.finish('E')
            return
        err, uid = yield from RegisterService.inst.sigup(email, password, repassword)
        if err:
            self.finish(err)
            return
        self.finish('S')
        return


from req import RequestHandler
from req import reqenv
import smtplib
from email.mime.text import MIMEText
def SendMail(From, To, Subject, Msg):
    content = MIMEText(msg)
    content['Suject'] = Subject
    content['From'] = From
    content['To'] = To
    s = smtplib.SMTP('localhost')
    s.sendmail(From, [To], content.as_string())
    s.quit()
    

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
        yield cur.execute('UPDATE "account" SET "account"."password" = %s '
                'WHERE "account"."email" = %s;', (email, _hash(newpassword)))
        if cur.rowcount != 1:
            return ('Edb', None)
        return (None, meta[1])

    def forgetpassword(self, email):
        def rand_password():
            return 'qwertyuiop'
        newpassword = rand_password()
        yield cur.execute('UPDATE "account" SET "account"."password" = %s '
                'WHERE "account"."email" = %s;', (email, _hash(newpassword)))
        if cur.rowcount != 1:
            return ('Edb', None)
        return (None, email)

    def edit(self, name, first_name, last_name, gender, degree, country, affiliation, department, position, affiliation_postcode, affiliation_address, contact_postcode, contact_address, email, ability):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "account"."password" "account"."uid" FROM "account" '
                'WHERE "account"."email" = %s;', (email,))
        if cur.rowcount != 1:
            return ('Enoexist', None)
        meta = cur.fetchone()
        if _hash(password) != meta[0]:
            return ('Epassword', None)
        uid = meta['uid']
        yield cur.execute('UPDATE table "account" SET '
                '("name", "first_name", "last_name", "gender", "degree", "country", "affiliation_address", "department", "position", "affiliation_postcode", "affiliation_address", "contact_postcode", "contact_address", "email")')



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

        elif req == 'edit':
            pass




from req import RequestHandler
from req import reqenv
import smtplib
from email.mime.text import MIMEText
def SendMail(From, To, Subject, Msg):
    content = MIMEText(Msg)
    content['Suject'] = Subject
    content['From'] = From
    content['To'] = To
    s = smtplib.SMTP('localhost')
    s.sendmail(From, [To], content.as_string())
    s.quit()
    

class LoginService:

    def _hash(self, p):
        ret = 1048576
        MOD = 10000000007
        C = 213
        for i in p:
            ret = (ret * C + ord(i)) % MOD
        return str(ret)

    def __init__(self, db):
        self.db = db
        LoginService.inst = self

    def signin(self, email, password):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "account"."password", "account"."uid" FROM "account" '
                'WHERE "account"."email" = %s;', (email,))
        if cur.rowcount != 1:
            return ('Enoexist', None)
        meta = cur.fetchone()
        print(password, type(self._hash(password)),type( meta[0]))
        if str(self._hash(password)) != meta[0]:
            return ('Epassword', None)
        return (None, meta[1])

    def changepassword(self, email, password, newpassword, repassword):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "account"."password" "account"."uid" FROM "account" '
                'WHERE "account"."email" = %s;', (email,))
        if cur.rowcount != 1:
            return ('Enoexist', None)
        meta = cur.fetchone()
        if self._hash(password) != meta[0]:
            return ('Epassword', None)
        if newpassword != repassword:
            return ('Enewpassword')
        yield cur.execute('UPDATE "account" SET "password" = %s '
                'WHERE "account"."email" = %s;', (email, self._hash(newpassword)))
        if cur.rowcount != 1:
            return ('Edb', None)
        return (None, meta[1])

    def forgetpassword(self, email):
        def rand_password():
            return 'root'
        cur = yield self.db.cursor()
        newpassword = rand_password()
        yield cur.execute('UPDATE "account" SET "password" = %s '
                'WHERE "account"."email" = %s;', (self._hash(newpassword), email))
        print(cur.rowcount)
        if cur.rowcount != 1:
            return ('Edb', None)
        return (None, email)

    def edit(self, name, first_name, last_name, gender, degree, country, affiliation, department, position, affiliation_postcode, affiliation_address, contact_postcode, contact_address, ability, password):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "account"."password" "account"."uid" FROM "account" '
                'WHERE "account"."email" = %s;', (email,))
        if cur.rowcount != 1:
            return ('Enoexist', None)
        meta = cur.fetchone()
        if self._hash(password) != meta[0]:
            return ('Epassword', None)
        uid = meta['uid']
        yield cur.execute('UPDATE table "account" SET '
                '("name", "first_name", "last_name", "gender", "degree", "country, "affiliation", "department", "position"", "affiliation_postcode", "affiliation_address", "contact_postcode", "contact_address") = (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (name, first_name, last_name, gender, degree, country, affiliation, department, position, affiliation_postcode, affiliation_address, contact_postcode, contact_address, ability, password))
        yield cur.execute('DELETE FROM "account_ability" WHERE "account_ability"."uid" = %s;',(uid,))
        for a in ability:
            yield cur.execute('INSERT INTO "account_ability" '
                    '("uid", "skill") VALUES(%s, %s);', (uid, a))
        return (None, uid)


    def smalledit(self,email, name, first_name, last_name, gender, degree, country, affiliation, department, position, affiliation_postcode, affiliation_address, contact_postcode, contact_address, cellphone, telephone, password):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "account"."password","account"."uid" FROM "account" '
                'WHERE "account"."email" = %s;', (email,))
        if cur.rowcount != 1:
            return ('Enoexist', None)
        meta = cur.fetchone()
        print(self._hash(password),meta[0])
        if str(self._hash(password)) != meta[0]:
            return ('Epassword', None)
        uid = meta[1]
        yield cur.execute('UPDATE "account" SET '
                '("name") = (%s), ("first_name") = (%s), ("last_name") = (%s), ("gender") = (%s), ("degree") = (%s), ("country")=(%s), ("affiliation")=(%s), ("department")=(%s), ("position")=(%s), ("affiliation_postcode")=(%s), ("affiliation_address")=(%s), ("contact_postcode")=(%s), ("contact_address")=(%s), ("cellphone")=(%s), ("telephone")=(%s) WHERE "account"."email" = %s;', (name, first_name, last_name, gender, degree, country, affiliation, department, position, affiliation_postcode, affiliation_address, contact_postcode, contact_address, cellphone, telephone, email))
        return (None, uid)

    def get_account_info(self, uid):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "name", "first_name", "last_name", "gender", "degree", "country", "affiliation", "department", "position", "affiliation_postcode", "affiliation_address", "contact_postcode", "contact_address", "email", "cellphone", "tellphone" FROM "account" WHERE "account"."uid" = %s;', (uid,))
        data = cur.fetchone()
        meta = {'name': data[0],
                'first_name': data[1],
                'last_name': data[2],
                'gender': data[3],
                'degree': data[4],
                'country': data[5],
                'affiliation': data[6],
                'department': data[7],
                'position': data[8],
                'affiliation_postcode': data[9],
                'affiliation_address': data[10],
                'contact_postcode': data[11],
                'contact_address': data[12],
                'email': data[13],
                'cellphone': data[14],
                'tellphone': data[15]
                }
        return (None, meta)




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
            self.set_secure_cookie('uid', str(uid))
            self.finish('S')
            return
        elif req == 'changepassword':
            try: 
                email = str(self.get_argument('email'))
                password = str(self.get_argument('password'))
                newpassword = str(self.get_argument('newpassword'))
                repassword = str(self.get_argument('repassword'))
            except:
                 self.finish('E')
                 return

        elif req == 'edit':
            name = str(self.get_argument('name', default=''))
            first_name = str(self.get_argument('first_name', default=''))
            last_name = str(self.get_argument('last_name', default=''))
            gender = str(self.get_argument('gender', default=''))
            degree = str(self.get_argument('degree', default=''))
            country = str(self.get_argument('country', default=''))
            affiliation = str(self.get_argument('affiliation', default=''))
            department = str(self.get_argument('department', default=''))
            position = str(self.get_argument('position', default=''))
            affiliation_postcode = str(self.get_argument('affiliation_postcode', default=''))
            affiliation_address = str(self.get_argument('affiliation_address', default=''))
            contact_postcode = str(self.get_argument('contact_postcode', default=''))
            contact_address = str(self.get_argument('contact_address', default=''))
            cellphone = str(self.get_argument('cellphone', default=''))
            telephone = str(self.get_argument('telephone', default=''))
            password = str(self.get_argument('password', default=''))
            ability = str(self.get_argument('ability', default=''))
            err, uid = yield from LoginService.inst.smalledit(self.acct['email'],name, first_name, last_name, gender, degree, country, affiliation, department, position, affiliation_postcode, affiliation_address, contact_postcode, contact_address, cellphone, telephone, password)
            if err:
                self.finish(err)
                return
            self.finish('S')
            return
        elif req == 'forgetpassword':
            try:
                email = str(self.get_argument('email'))
            except:
                self.finish('EE')
                return

            err, uid = yield from LoginService.inst.forgetpassword(email)
            if err:
                self.finish(err)
                return
            self.finish('S')
            return

        elif req == 'logout':
            self.clear_cookie('uid')
            return



class ModifyuserHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render('modifyuser.html')
        pass


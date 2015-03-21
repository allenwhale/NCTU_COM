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
        yield cur.execute('SELECT "account"."password", "account"."uid" FROM "account" '
                'WHERE "account"."email" = %s;', (email,))
        if cur.rowcount != 1:
            return ('Enoexist', None)
        meta = cur.fetchone()
        print(password, type(_hash(password)),type( meta[0]))
        if str(_hash(password)) != meta[0]:
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
            return 'root'
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
                '("name", "first_name", "last_name", "gender", "degree", "country, "affiliation", "department", "position"", "affiliation_postcode", "affiliation_address", "contact_postcode", "contact_address", "email") = (%s, %s, %s, %s, %s, %s, %s, %s)')
        yield cur.execute('DELETE FROM "account_ability" WHERE "account_ability"."uid" = %s;',(uid,))
        for a in ability:
            yield cur.execute('INSERT INTO "account_ability" '
                    '("uid", "skill") VALUES(%s, %s);', (uid, a))
        return (None, uid)

        def get_account_info(self, uid):
            cur = yield self.db.cursor()
            yield cur.execute('SELECT "name", "first_name", "last_name", "gender", "degree", "country", "affiliation", "department", "position", "affiliation_postcode", "affiliation_address", "contact_postcode", "contact_address", "email" FROM "account" WHERE "account"."uid" = %s;', (uid,))
            data = cur.fetchone()
            meta = {'name': data[0],
                    'first_name': data[1],
                    'last_name': data[2],
                    'gender': data[3],
                    'degree': data[4],
                    'country': data[5],
                    'affiliation': data[6],
                    'department': data[7],
                    'position': data[8]
                    'affiliation_postcode': data[9],
                    'affiliation_address': data[10],
                    'contact_postcode': data[11],
                    'contact_address': data[12],
                    'email': data[13]
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
                repassword = sstr(self.get_argument('repassword'))
            except:
                 self.finish('E')
                 return

        elif req == 'edit':
            try:
                name = str(self.get_arugment('name'))
                first_name = str(self.get_arugment('first_name'))
                last_name = str(self.get_arugment('last_name'))
                gender = str(self.get_arugment('gender'))
                degreem = str(self.get_arugment('degreem'))
                country = str(self.get_arugment('country'))
                affiliation = str(self.get_arugment('affiliation'))
                department = str(self.get_arugment('department'))
                position = str(self.get_arugment('position'))
                affiliation_postcode = str(self.get_arugment('affiliation_postcode'))
                affiliation_adress = str(self.get_arugment('affiliation_adress'))
                contact_postcode = str(self.get_arugment('contact_postcode'))
                contact_address = str(self.get_arugment('contact_address'))
                cellphone = str(self.get_arugment('cellphone'))
                tellphone = str(self.get_arugment('tellphone'))
                password = str(self.get_arugment('password'))
                ability = str(self.get_arugment('ability'))
            except:
                self.finish('E')
                return
            err, uid = yield from LoginSerive.inst.edit(self, name, first_name, last_name, gender, degree, country, affiliation, department, position, affiliation_postcode, affiliation_address, contact_postcode, contact_address, ability)
            if err:
                self.finish(err)
                return
            self.finish('S')
            return
        elif req == 'forgetpassword':
            try:
                email = str(self.get_arugment('email'))
            except:
                self.finish('E')
                return

            err, uid = yield from LoginSerive.inst.forgetpassword(email)
            if err:
                self.finish(err)
                return
            self.finish('S')
            return


class ModifyuserHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render('modifyuser.html')
        pass


from req import RequestHandler
from req import reqenv
class LoginService:
    def __init__(self, db):
        self.db = db
        LoginService.inst = self

    def signup(self, name, first_name, last_name, gender, degree, country, affiliation, department, position, affiliation_postcode, affiliation_address, contact_postcode, contact_address, email, password, repassword, ability):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT 1 FROM "account" '
                'WHERE "account"."name" = %s OR "account"."email" = %s;', (name, email))
        if cur.rowcount != 0:
            return ('Eexist', None)
        yield cur.execute('INSERT INTO "sccount" '
                '("name", "first_name", "last_name", "gender", "degree", "country", '
                '"affiliation", "department", "affiliation_postcode", "affiliation_address", '
                '"contact_postcode", "contact_address", "email", "password") ')

class LoginHandler(RequestHandler):
    @reqenv
    def get(self):
        pass

    @reqenv
    def post(self):
        try:
            name = str(self.get_argument('name'))
            first_name = str(self.get_argument('first_name'))
            last_name = str(self.get_argument('last_name'))
            gender = str(self.get_argument('gender'))
            degree = str(self.get_argument('degree'))
            country = str(self.get_argument('country'))
            affiliation = str(self.get_argument('affiliation'))
            department = str(self.get_argument('department'))
            position = str(self.get_argument('position'))
            affiliation_postcode = str(self.get_argument('affiliation_postcode'))
            affiliation_address = str(self.get_argument('affiliation_address'))
            contact_postcode = str(self.get_argument('contact_postcode'))
            contact_address = str(self.get_argument('contact_address'))
            cellphone = str(self.get_argument('cellphone'))
            tellphone = str(self.get_argument('tellphone'))
            password = str(self.get_argument('password'))
            repassword = str(self.get_argument('repassword'))
            ability = str(self.get_arguments('ability'))
        except:
            self.finish('E')
            return


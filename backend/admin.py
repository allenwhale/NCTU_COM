from req import RequestHandler
from req import reqenv
import config

class AdminService:
    def __init__(self, db):
        self.db = db
        AdminService.inst = self

    def isadmin(self, acct):
        if not acct:
            return 0
        return 1 if int(acct['uid']) in  config.ADMIN_RANGE else 0

    def admin_reply(self, pid, f):
        if not f:
            return ('Efile', None)
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "papercheck", "status" FROM "paperupload" WHERE "pid" = %s;', (pid,))
        if cur.rowcount != 1:
            return ('Epaper', None)
        check, status = cur.fetchone()
        check = int(check)
        status = int(status)
        if status != 0:
            return ('Eturn', None)
        path = '../html/paper/'+str(pid)+'/reply-'+str(pid)+('' if check == 0 else '%d'%check)+'.'+f['filename'].split('.')[-1]
        _f = open(path, 'wb')
        _f.write(f['body'])
        _f.close()
        yield cur.execute('UPDATE "paperupload" SET "status" = 1 WHERE "pid"= %s;', (pid,)) 
        if cur.rowcount != 1:
            return ('Edb', None)
        return (None, pid)

    def user_reply(self, pid, f):
        if not f:
            return ('Efile', None)
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "papercheck", "status" FROM "paperupload" WHERE "pid" = %s;', (pid,))
        if cur.rowcount != 1:
            return ('Epaper', None)
        check, status = cur.fetchone()
        check = int(check)
        status = int(status)
        if status != 1:
            return ('Eturn', None)
        path = '../html/paper/'+str(pid)+'/rreply-'+str(pid)+('' if check == 0 else '%d'%check)+'.'+f['filename'].split('.')[-1]
        _f = open(path, 'wb')
        _f.write(f['body'])
        _f.close()
       
        yield cur.execute('UPDATE "paperupload" SET "status" = 1, "papercheck" = %s WHERE "pid"= %s;', (check+1, pid,)) 
        if cur.rowcount != 1:
            return ('Edb', None)
        return (None, pid)




class AdminHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render("admin.html")
        return
    @reqenv
    def post(self):
        req = self.get_argument('req', None)
        if req == 'isadmin':
            self.finish(str(AdminService.inst.isadmin(self.acct)))
        return

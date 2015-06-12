from req import RequestHandler
from req import reqenv
from req import Service
import config
from mail import MailHandler

class AdminService:
    def __init__(self, db):
        self.db = db
        self.reply = MailHandler('templates/reply.html')
        AdminService.inst = self

    def isadmin(self, acct):
        if not acct:
            return 0
        return 1 if int(acct['uid']) in  config.ADMIN_RANGE else 0

    def admin_reply(self, acct, pid, f, end, letter):
        if AdminService.inst.isadmin(acct) == 0:
            return ('Eaccess', None)
        if not f:
            return ('Efile', None)
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "papercheck", "status", "pass" FROM "paperupload" WHERE "pid" = %s;', (pid,))
        if cur.rowcount != 1:
            return ('Epaper', None)
        check, status, _pass = cur.fetchone()
        check = int(check)
        status = int(status)
        try:
            _pass = int(_pass)
        except:
            _pass = -1
        if status != 0:
            return ('Eturn', None)
        if _pass != -1:
            return ('Epassorfail', None)
        print(end, type(end))
        if end == '1':
            yield cur.execute('UPDATE "paperupload" SET ("papercheck", "pass", "lastcheck") = (%s, %s, %s) WHERE "pid" = %s;', (10, 1,check, pid,))
            #return (None, pid)

        if end == '0':
            yield cur.execute('UPDATE "paperupload" SET ("papercheck", "pass", "lastcheck") = (%s, %s, %s) WHERE "pid" = %s;', (11, 0,check, pid,))
            #return (None, pid)

        path = '../html/paper/'+str(pid)+'/reply-'+str(pid)+('' if check == 0 else '-%d'%check)+'.'+f['filename'].split('.')[-1]
        _f = open(path, 'wb')
        _f.write(f['body'])
        _f.close()
        if end == '0' or end == '1':
            return (None, pid)
        yield cur.execute('UPDATE "paperupload" SET "status" = 1 WHERE "pid"= %s;', (pid,)) 
        if cur.rowcount != 1:
            return ('Edb', None)
        if check == 2:
            yield cur.execute('UPDATE "paperupload" SET "pass" = %s WHERE "pid"= %s;', (end, pid))
            if cur.rowcount != 1:
                return ('Edb', None)
            if end == 0:
                #10
                yield cur.execute('UPDATE "paperupload" SET "papercheck" = %s WHERE "pid"= %s;', (10, pid))
            elif end == 1:
                #11
                yield cur.execute('UPDATE "paperupload" SET "papercheck" = %s WHERE "pid"= %s;', (11, pid))
            yield cur.execute('UPDATE "paperupload" SET "status" = 0 WHERE "pid"= %s;', (pid,)) 
        yield cur.execute('SELECT "uid" FROM "paperupload" WHERE "pid" = %s;', (pid,))
        uid = cur.fetchone()[0]
        err, meta = yield from Service.Login.get_account_info(uid)
        self.reply.send(meta['email'], 'MS-%s稿件通知，稿件審查完畢'%pid, pid=pid, letter=letter)
        return (None, pid)

    def user_reply(self, acct, pid, rreply, anony, non):
        if not rreply or not anony or not non:
            return ('Efile', None)
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "papercheck", "status", "uid" FROM "paperupload" WHERE "pid" = %s;', (pid,))
        if cur.rowcount != 1:
            return ('Epaper', None)
        check, status, uid = cur.fetchone()
        check = int(check)
        status = int(status)
        if str(uid) != str(acct['uid']):
            return ('Euser', None)
        if status != 1:
            return ('Eturn', None)
        path = '../html/paper/'+str(pid)+'/rreply-'+str(pid)+('' if check == 0 else '-%d'%check)+'.'+rreply['filename'].split('.')[-1]
        _f = open(path, 'wb')
        _f.write(rreply['body'])
        _f.close()
        check += 1
        path = '../html/paper/'+str(pid)+'/'+str(pid)+('' if check == 0 else '-%d'%check)+'.'+anony['filename'].split('.')[-1]
        _f = open(path, 'wb')
        _f.write(anony['body'])
        _f.close()
        path = '../html/paper/'+str(pid)+'/non-'+str(pid)+('' if check == 0 else '-%d'%check)+'.'+non['filename'].split('.')[-1]
        _f = open(path, 'wb')
        _f.write(non['body'])
        _f.close()
       
        yield cur.execute('UPDATE "paperupload" SET "status" = 0, "papercheck" = %s WHERE "pid"= %s;', (check, pid,)) 
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
        elif req == 'adminreply':
            pid = self.get_argument('pid', None)
            try:
                f = self.request.files['reply'][0]
            except:
                f = None
            end = self.get_argument('end', None)
            letter = self.get_argument('letter', None)
            err, pid = yield from AdminService.inst.admin_reply(self.acct, pid, f, end, letter)
            if err:
                self.finish(err)
                return
            self.finish('S')
        elif req == 'userreply':
            pid = self.get_argument('pid', None)
            try:
                anony = self.request.files['anony'][0]
                non = self.request.files['non-anony'][0]
                rreply = self.request.files['rreply'][0]
            except:
                anony = None
                non = None
                rreply = None
            err, pid = yield from AdminService.inst.user_reply(self.acct, pid, rreply, anony, non)
            if err:
                self.finish(err)
                return
            self.finish('S')
        return

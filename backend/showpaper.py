from req import RequestHandler
from req import reqenv
from req import Service
import os
import time
import json

class ShowpaperService:
    def __init__(self, db):
        self.db = db
        ShowpaperService.inst = self

    def get_author_bypid(self, pid):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "apid", "name", "first_name", "last_name", "affiliation", "department", "position", "country", "address", "phone", "email" FROM "author_paper" WHERE "author_paper"."pid" = %s;', (pid, ))
        meta = []
        for apid, name, first_name, last_name, affiliation, department, position, country, address, phone, email in cur:
            meta.append({'apid': apid,
                'name': name,
                'first_name': first_name,
                'last_name': last_name,
                'affiliation': affiliation,
                'department': department,
                'position': position,
                'country': country,
                'address': address,
                'phone': phone,
                'email': email})
        return (None, meta)

    def get_keywords_bypid(self, pid):
        cur = yield self.db.cursor()
        meta = {'chinese': [],
                'english': []}
        yield cur.execute('SELECT "keyword" FROM "chinesekeywords" WHERE "chinesekeywords"."pid" = %s;', (pid, ))
        for (k, ) in cur:
            meta['chinese'].append(k)
        yield cur.execute('SELECT "keyword" FROM "englishkeywords" WHERE "englishkeywords"."pid" = %s;', (pid, ))
        for (k, ) in cur:
            meta['english'].append(k)

        return (None, meta)


    def get_paper(self, acct, check=None, PID=None):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "pid", "papercheck", "chinesetitle", "englishtitle", "chineseabstract", "englishabstract", "letter", "picnum", "wordnum", "submitted", "confirm", "conflict", "conflict_explain", "status", "pass", "lastcheck" FROM "paperupload" '+('' if Service.Admin.isadmin(acct) else 'WHERE "paperupload"."uid" = %s')+' ORDER BY "papercheck" ASC, "pid" ASC;', (acct['uid'],))
        meta = []
        for pid, papercheck, chinesetitle, englishtitle, chineseabstract, englishabstract, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain, status, _pass, lastcheck in cur:
            meta.append({'pid': pid,
                'lastcheck': lastcheck,
                'papercheck': papercheck,
                'pass': _pass,
                'chinesetitle': chinesetitle,
                'englishtitle': englishtitle,
                'chineseabstract': chineseabstract,
                'englishabstract': englishabstract,
                'letter': letter,
                'picnum': picnum,
                'word': wordnum,
                'submitted': submitted,
                'confirm': confirm,
                'conflict': conflict,
                'conflict_explain': conflict_explain,
                'status': status
                })
        if check:
            tm = []
            for m in meta:
                if str(m['papercheck']) in check:
                    tm.append(m)
            meta = tm

        if PID:
            tm = []
            for m in meta:
                if str(m['pid']) in PID:
                    tm.append(m)
            meta = tm

        for m in meta:
            err, m['author'] = yield from self.get_author_bypid(m['pid'])
            err, m['keywords'] = yield from self.get_keywords_bypid(m['pid'])
        return (None, meta)

    def get_all_paper(self,acct, check=None, PID=None):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "pid", "papercheck", "chinesetitle", "englishtitle", "chineseabstract", "englishabstract", "letter", "picnum", "wordnum", "submitted", "confirm", "conflict", "conflict_explain","uid", "status", "pass" FROM "paperupload" ORDER BY "papercheck" ASC, "pid" ASC;', ())
        meta = [[],[],[],[],[],[],[],[],[],[],[],[],]
        for pid, papercheck, chinesetitle, englishtitle, chineseabstract, englishabstract, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain, uid, status, _pass in cur:
            if Service.Admin.isadmin(acct) or str(acct['uid'])== str(uid):
                meta[papercheck+status].append({'pid': pid,
                    'pass': _pass,
                    'papercheck': papercheck,
                    'chinesetitle': chinesetitle,
                    'englishtitle': englishtitle,
                    'chineseabstract': chineseabstract,
                    'englishabstract': englishabstract,
                    'letter': letter,
                    'picnum': picnum,
                    'word': wordnum,
                    'submitted': submitted,
                    'confirm': confirm,
                    'conflict': conflict,
                    'conflict_explain': conflict_explain
                    })
        return (None, meta)

    def get_author_save_byuid(self, uid):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "apid", "name", "first_name", "last_name", "affiliation", "department", "position", "country", "address", "phone", "email" FROM "author_paper_save" WHERE "uid" = %s;', (uid, ))
        meta = []
        for apid, name, first_name, last_name, affiliation, department, position, country, address, phone, email in cur:
            meta.append({'apid': apid,
                'name': name,
                'first_name': first_name,
                'last_name': last_name,
                'affiliation': affiliation,
                'department': department,
                'position': position,
                'country': country,
                'address': address,
                'phone': phone,
                'email': email})
        return (None, meta)

    def get_keywords_save_byuid(self, uid):
        cur = yield self.db.cursor()
        meta = {'chinese': [],
                'english': []}
        yield cur.execute('SELECT "keyword" FROM "chinesekeywords_save" WHERE"pid" = %s;', (pid, ))
        for (k, ) in cur:
            meta['chinese'].append(k)
        yield cur.execute('SELECT "keyword" FROM "englishkeywords_save" WHERE"pid" = %s;', (pid, ))
        for (k, ) in cur:
            meta['english'].append(k)

        return (None, meta)

    def get_paper_save(self, uid):
        def gen_sql(data):
            sql, prama = '', ()
            for d in data:
                if sql == '':
                    sql = '"%s"'%d
                else:
                    sql = sql + ',"%s" '%d
                prama = prama + (d,)
            return (sql, prama)
        args = ['chinesetitle', 'englishtitle', 'chineseabstract', 'englishabstract', 'letter', 'picnum', 'wordnum', 'submitted', 'confirm', 'conflict', 'conflict_explain', ]
        sql, prama = gen_sql(args)
        cur = yield self.db.cursor()
        yield cur.execute('SELECT '+sql+' FROM "paperupload_save" WHERE "uid" = %s;', (uid,))
        if cur.rowcount != 1:
            return (None, None)
        meta = {'uid': uid}
        q = cur.fetchone()
        for i,a in enumerate(args):
            meta[a] = q[i]
        err, meta['author'] = yield from self.get_author_bypid(meta['uid'])
        err, meta['keywords'] = yield from self.get_keywords_bypid(meta['uid'])
        return (None, meta)

    def get_file_name(self, pid):
        path = '../html/paper/'+ str(pid)
        res = {0:[None, None,None,None], 1: [None,None,None,None],2:[None,None,None,None],3:[None,None,None,None]}
        try:
            for f in os.listdir(path):
                if f.find('non-'+pid+'.')!=-1:
                    res[0][1]=f
                elif f.find('rreply-'+pid+'.')!=-1:
                    res[0][3]=f
                elif f.find('reply-'+pid+'.')!=-1:
                    res[0][2]=f
                elif f.find(pid+'.')!=-1:
                    res[0][0]=f
                for _ in range(1,4):
                    if f.find('non-'+pid+'-'+str(_)+'.')!=-1:
                        res[_][1]=f
                    elif f.find('rreply-'+pid+'-'+str(_)+'.')!=-1:
                        res[_][3]=f
                    elif f.find('reply-'+pid+'-'+str(_)+'.')!=-1:
                        res[_][2]=f
                    elif f.find(pid+'-'+str(_)+'.')!=-1:
                        res[_][0]=f
        except:
            pass
        return res



class ShowpaperHandler(RequestHandler):
    @reqenv
    def get(self):
        pid = self.get_argument('pid', None)
        if pid:
            err, meta = yield from ShowpaperService.inst.get_paper(self.acct, None, [pid])
            url = ShowpaperService.inst.get_file_name(pid)
            print(meta)
            self.render('showpaper_pid.html', meta=meta, url=url)
        else:
            err, meta = yield from ShowpaperService.inst.get_all_paper(self.acct)
            self.render('showpaper.html', meta=meta)

        return
    @reqenv
    def post(self):
        req = str(self.get_argument('req'))
        uid = self.acct['uid']
        if req == 'get_paper':
            try:
                papercheck = self.get_arguments('papercheck[]')
            except:
                papercheck = None
            try:
                pid = self.get_arguments('pid[]')
            except:
                pid = None
            #err, meta = yield from ShowpaperService.inst.get_all_paper(papercheck, pid)
            meta=0
            err =0
            if err:
                self.finish(err)
                return
            self.finish(json.dumps(meta))
            return
        return

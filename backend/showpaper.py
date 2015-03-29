from req import RequestHandler
from req import reqenv
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
        for k in cur:
            meta['chinese'].append(k)
        yield cur.execute('SELECT "keyword" FROM "englishkeywords" WHERE "englishkeywords"."pid" = %s;', (pid, ))
        for k in cur:
            meta['english'].append(k)

        return (None, meta)


    def get_paper(self, uid, check=None):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "pid", "papercheck", "chinesetitle", "englishtitle", "chineseabstract", "englishabstract", "letter", "picnum", "wordnum", "submitted", "confirm", "conflict", "conflict_explain" FROM "paperupload" WHERE "paperupload"."uid" = %s;', (uid,))
        meta = []
        for pid, papercheck, chinesetitle, englishtitle, chineseabstract, englishabstract, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain in cur:
            meta.append({'pid': pid,
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
        if check:
            tm = []
            for m in meta:
                print(type(m['papercheck']))
                if str(m['papercheck']) in check:
                    tm.append(m)
            meta = tm
        for m in meta:
            err, m['author'] = yield from self.get_author_bypid(m['pid'])
            err, m['keywords'] = yield from self.get_keywords_bypid(m['pid'])
        return (None, meta)


class ShowpaperHandler(RequestHandler):
    @reqenv
    def get(self):
        try:
            pid = self.get_argument('pid')
            self.render('showpaper_pid.html')
        except:
            self.render('showpaper.html')
        return
    @reqenv
    def post(self):
        req = str(self.get_argument('req'))
        if req == 'get_paper':
            uid = self.acct['uid']
            papercheck = self.get_arguments('papercheck[]')
            err, meta = yield from ShowpaperService.inst.get_paper(uid, papercheck)
            if err:
                self.finish(err)
                return
            self.finish(json.dumps(meta))
            return

        return

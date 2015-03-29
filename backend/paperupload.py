from req import RequestHandler
from req import reqenv

class PaperuploadService:
    def __init__(self, db):
        self.db = db
        PaperuploadService.inst = self

    def upload(self, uid, chinesetitle, englishtitle, chineseabstract, englishabstract, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain, anony_file, non_anony_file):
#            , chineseabstract, englishabstract, chinesekeywords, englishkeywords, authors, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain, attach_file):
       cur = yield self.db.cursor()
       yield cur.execute('INSERT INTO "paperupload" ("uid", "chinesetitle", "englishtitle", "chineseabstract", "englishabstract", "letter", "picnum", "wordnum", "submitted", "confirm", "conflict", "conflict_explain") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING "paperupload"."pid";', (uid, chinesetitle, englishtitle, chineseabstract, englishabstract, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain));
<<<<<<< HEAD
       pid = str(cur.fetchone()[0]);
       print(pid);
=======
       if cur.rowcount != 1:
           return ('EDB', None)
       pid = str(cur.fetchone()[0])
       anony_filename = '../html/paper/' + str(pid) + '.' + anony_file['filename'].split('.')[-1]
       non_anony_filename = '../html/paper/non-' + str(pid) + '.' + non_anony_file['filename'].split('.')[-1]
       f = open(anony_filename, 'wb+')
       f.write(anony_file['body'])
       f.close()
       f = open(non_anony_filename, 'wb+')
       f.write(non_anony_file['body'])
       f.close()
>>>>>>> 012917411fdad9e2f2caa8146f4ea5c4ec8319f9
       """
       apid = 0
       for a in authors:
           apid += 1
           yield cur.execute('INSERT INTO "author_paper" ("pid", "apid", "name", "first_name", "last_name", "affiliation", "department", "position", "country", "adress", "email") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (pid, apid,) + tuple(a))
       """
       return (None, True)

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


    def get_paper(self, uid):
        cur = yield self.db.cursor()
        yield cur.execute('SELECT "pid", "chinesetitle", "englishtitle", "chineseabstract", "englishabstract", "letter", "picnum", "wordnum", "submitted", "confirm", "conflict", "conflict_explain" FROM "paperupload" WHERE "paperupload"."uid" = %s;', (uid,))
        meta = []
        for pid, chinesetitle, englishtitle, chineseabstract, englishabstract, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain in cur:
            meta.append({'pid': pid,
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
        for m in meta:
            err, m['author'] = yield from self.get_author_bypid(m['pid'])
            err, m['keywords'] = yield from self.get_keywords_bypid(m['pid'])
        return (None, meta)


class PaperuploadHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render('paperupload.html')
        return

    @reqenv
    def post(self):
        chinesetitle = str(self.get_argument('chinesetitle', default=''))
        englishtitle = str(self.get_argument('englishtitle', default=''))
        chineseabstract = str(self.get_argument('chineseabstract', default=''))
        englishabstract = str(self.get_argument('englishabstract', default=''))
        chinesekeywords = list(self.get_arguments('chinesekeywords[]'))
        englishkeywords = list(self.get_arguments('englishkeywords[]'))
        letter = str(self.get_argument('letter', default=''))
        picnum = str(self.get_argument('picnum', default=''))
        wordnum = str(self.get_argument('wordnum', default=''))
        submitted = str(self.get_argument('submitted', default=''))
        confirm = str(self.get_argument('confirm', default=''))
        conflict = str(self.get_argument('conflict', default=''))
        conflict_explain = str(self.get_argument('conflict_explain', default=''))
        anony_file = self.request.files['anony'][0]
        non_anony_file = self.request.files['non-anony'][0]
        """
        authors = self.get_arguments('authors')
        attach_file = self.request.files['attach_file'][0]
        """
        print(self.acct['uid'])
        err, pid = yield from PaperuploadService.inst.upload(self.acct['uid'], chinesetitle, englishtitle, chineseabstract, englishabstract, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain, anony_file, non_anony_file)

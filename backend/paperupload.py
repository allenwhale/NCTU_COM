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
       """
       apid = 0
       for a in authors:
           apid += 1
           yield cur.execute('INSERT INTO "author_paper" ("pid", "apid", "name", "first_name", "last_name", "affiliation", "department", "position", "country", "adress", "email") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (pid, apid,) + tuple(a))
       """
       return (None, True)


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

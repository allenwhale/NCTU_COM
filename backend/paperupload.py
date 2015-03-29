from req import RequestHandler
from req import reqenv

class PaperuploadService:
    def __init__(self, db):
        self.db = db
        PaperuploadService.inst = self

    def upload(self, chinesetitle, englishtitle, chineseabstract, englishabstract, chinesekeywords, englishkeywords, authors, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain, attach_file):
       cur = yield self.db.cursor()
       yield cur.execute('INSERT INTO "paperupload" ("chinesetitle", "englishtitle", "chineseabstract", "englishabstract", "chinesekeywords" ,"englishkeywords", "letter", "picnum", "wordnum", "submitted", "confirm", "conflict", "conflict_explain") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING "paperupload"."pid";', (chinesetitle, englishtitle, chineseabstract, englishabstract, chinesekeywords, englishkeywords, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain))
       pid = str(cur.fetchone()[0])
       apid = 0
       for a in authors:
           apid += 1
           yield cur.execute('INSERT INTO "author_paper" ("pid", "apid", "name", "first_name", "last_name", "affiliation", "department", "position", "country", "adress", "email") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (pid, apid,) + tuple(a))
       filename = str(pid)
       f = open('../html/paper/' + filename, 'wb+')
       f.write(attach_file['body'])
       f.close()
       return (None, pid)



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
        chinesekeywords = list(self.get_arguments('chinesekeywords', default=''))
        englishkeywords = list(self.get_arguments('englishkeywords', default=''))
        authors = self.get_arguments('authors')
        letter = str(self.get_argument('letter', default=''))
        picnum = str(self.get_argument('picnum', default=''))
        wordnum = str(self.get_argument('wordnum', default=''))
        submitted = str(self.get_argument('submitted', default=''))
        confirm = str(self.get_arguments('confirm', default=''))
        conflict = str(self.get_argument('confllict', default=''))
        conflict_explain = str(self.get_argument('conflict_explain', default=''))
        attach_file = self.request.files['attach_file'][0]

        err, pid = yield from PaperuploadService.inst(chinesetitle, englishtitle, chineseabstract, englishabstract, chinesekeywords, englishkeywords, authors, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain, attach_file)

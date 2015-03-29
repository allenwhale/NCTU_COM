from req import RequestHandler
from req import reqenv

class PaperuploadService:
    def __init__(self, db):
        self.db = db
        PaperuploadService.inst = self

    def upload(self, uid, chinesetitle, englishtitle, chineseabstract, englishabstract, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain, anony_file, non_anony_file, author):
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
       apid = 0
       print(author)
       for a in author:
           print(a)
       for a in author:
           apid += 1
           print(apid)
           print(a)
           yield cur.execute('INSERT INTO "author_paper" ("pid", "apid", "name", "first_name", "last_name", "affiliation", "department", "position", "country", "address", "email") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (pid, apid,) + tuple(a))
       return (None, pid)
'''
   def set_papercheck(self, pid, papercheck):
       cur = yield from self.db.cursor()
       if papercheck not in range(4):
           return ('Eindex', None)
'''

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
        author_name = self.get_arguments('name[]')
        author_first_name = self.get_arguments('first_name[]')
        author_last_name = self.get_arguments('last_name[]')
        author_affiliation = self.get_arguments('affiliation[]')
        author_department = self.get_arguments('department[]')
        author_position = self.get_arguments('position[]')
        author_address = self.get_arguments('address[]')
        author_phone = self.get_arguments('phone[]')
        author_email = self.get_arguments('email[]')
        author = list(zip(author_name, author_first_name, author_last_name, author_affiliation, author_department, author_position, author_address, author_phone, author_email))
        for a in author:
            print(a)
        """
        authors = self.get_arguments('authors')
        attach_file = self.request.files['attach_file'][0]
        """
        print(self.acct['uid'])
        print(author)
        err, pid = yield from PaperuploadService.inst.upload(self.acct['uid'], chinesetitle, englishtitle, chineseabstract, englishabstract, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain, anony_file, non_anony_file, author)
        if err:
            self.finish(err)
            return
        self.finish('S')
        return

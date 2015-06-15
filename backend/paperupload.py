from req import RequestHandler
from req import reqenv
from req import Service
import os
from mail import MailHandler

class PaperuploadService:
    def __init__(self, db):
        self.db = db
        self.update_mail = MailHandler('templates/upload_mail.html')
        PaperuploadService.inst = self

    def upload(self, uid, chinesetitle, englishtitle, chineseabstract, englishabstract, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain, anony_file, non_anony_file, author, chinesekeywords, englishkeywords):
#            , chineseabstract, englishabstract, chinesekeywords, englishkeywords, authors, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain, attach_file):
        if chinesetitle == '' or englishtitle == '' or chineseabstract == '' or englishabstract == '' or letter == '' or picnum == '' or wordnum == '' :
            print(1)
            return ('Eempty', None)
        if chinesekeywords.count('') == 5 or englishkeywords.count('') == 5:
            print(2)
            return ('Eempty', None)
        print(confirm)
        if confirm.count('0') != 0:
            print(3)
            return ('Eempty', None)
        cur = yield self.db.cursor()
        yield cur.execute('INSERT INTO "paperupload" ("uid", "chinesetitle", "englishtitle", "chineseabstract", "englishabstract", "letter", "picnum", "wordnum", "submitted", "confirm", "conflict", "conflict_explain") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING "paperupload"."pid";', (uid, chinesetitle, englishtitle, chineseabstract, englishabstract, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain));
        if cur.rowcount != 1:
            return ('EDB', None)
        pid = str(cur.fetchone()[0])
        os.makedirs('../html/paper/'+pid)
        anony_filename = '../html/paper/' + pid + '/' + str(pid) + '.' + anony_file['filename'].split('.')[-1]
        non_anony_filename = '../html/paper/'+pid+'/non-' + str(pid) + '.' + non_anony_file['filename'].split('.')[-1]
        f = open(anony_filename, 'wb+')
        f.write(anony_file['body'])
        f.close()
        f = open(non_anony_filename, 'wb+')
        f.write(non_anony_file['body'])
        f.close()
        apid = 0
        for a in author:
            print(a)
            apid += 1
            yield cur.execute('INSERT INTO "author_paper" ("pid", "apid", "name", "first_name", "last_name", "affiliation", "department", "position", "address", "phone", "email") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (pid, apid,) + tuple(a))
        for k in chinesekeywords:
            yield cur.execute('INSERT INTO "chinesekeywords" ("pid", "keyword") VALUES(%s, %s)', (pid, k))
        for k in englishkeywords:
            yield cur.execute('INSERT INTO "englishkeywords" ("pid", "keyword") VALUES(%s, %s)', (pid, k))
        yield cur.execute('DELETE FROM "paperupload_save" WHERE "uid" = %s;', (uid,))
        yield cur.execute('DELETE FROM "author_paper_save" WHERE "uid" = %s;', (uid,))
        yield cur.execute('DELETE FROM "chinesekeywords_save" WHERE "uid" = %s;', (uid,))
        yield cur.execute('DELETE FROM "englishkeywords_save" WHERE "uid" = %s;', (uid,))
        err, meta = yield from Service.Login.get_account_info(uid)
        err = self.update_mail.send(meta['email'],'MS-%s稿件通知，已收到您的稿件'%pid, pid=pid)
        return (None, pid)
    def set_papercheck(self, pid, papercheck):
        cur = yield from self.db.cursor()
        if int(papercheck) not in range(4):
            return ('Eindex', None)
        yield cur.execute('UPDATE "paperupload" SET "papercheck" = %s WHERE "pid" = %s AND "uid" = %s;', (papercheck, pid, uid))
        if cur.rowcount != 1:
            return ('Eexeist', None)
        return (None, pid)

    def save_paper(self, data, chinesekeywords, englishkeywords, author):
        def gen_sql(data):
            sql1, sql2, prama = '', '', ()
            for d in data:
                if sql1 == '':
                    sql1 = '"%s"'%d
                else:
                    sql1 = sql1 + ',"%s" '%d
                if sql2 == '':
                    sql2 = '%s'
                else:
                    sql2 = sql2 + ',%s '
                prama = prama + (data[d],)
            return ('('+sql1+') VALUES ('+sql2+')', prama)
        
        uid = data['uid']
        #data.pop('uid')
        cur = yield self.db.cursor()
        yield cur.execute('DELETE FROM "paperupload_save" WHERE "uid" = %s;', (uid,))
        yield cur.execute('DELETE FROM "author_paper_save" WHERE "uid" = %s;', (uid,))
        yield cur.execute('DELETE FROM "chinesekeywords_save" WHERE "uid" = %s;', (uid,))
        yield cur.execute('DELETE FROM "englishkeywords_save" WHERE "uid" = %s;', (uid,))
        sql, prama = gen_sql(data)
        print(sql,prama)
        yield cur.execute('INSERT INTO "paperupload_save" '+sql+';', prama)
        if cur.rowcount != 1:
            return ('Edb', None)
        print(chinesekeywords)
        for k in chinesekeywords:
            yield cur.execute('INSERT INTO "chinesekeywords_save" ("uid", "keyword") VALUES (%s, %s);', (uid, k))
        for k in englishkeywords:
            yield cur.execute('INSERT INTO "englishkeywords_save" ("uid", "keyword") VALUES (%s, %s);', (uid, k))
        apid = 0
        for a in author:
           apid += 1
           yield cur.execute('INSERT INTO "author_paper_save" ("uid", "apid", "name", "first_name", "last_name", "affiliation", "department", "position", "address", "phone", "email") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (uid, apid,) + tuple(a))

        return (None, uid)

class PaperuploadHandler(RequestHandler):
    @reqenv
    def get(self):
        try:
            uid =self.acct['uid']
        except:
            uid = 0
        err, meta = yield from Service.Showpaper.get_paper_save( uid)
        self.render('paperupload.html', meta=meta)
        return

    @reqenv
    def post(self):
        req = self.get_argument('req', None)
        if req == 'save':
            args = ['chinesetitle', 'englishtitle', 'chineseabstract', 'englishabstract', 'letter', 'picnum', 'wordnum', 'submitted', 'confirm', 'conflict', 'conflict_explain', ]
            meta = self.get_args(args)
            try:
                meta['uid'] = self.acct['uid']
            except:
                meta['uid'] = 0
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
            chinesekeywords = list(self.get_arguments('chinesekeywords[]'))
            englishkeywords = list(self.get_arguments('englishkeywords[]'))
            err, uid = yield from PaperuploadService.inst.save_paper(meta, chinesekeywords, englishkeywords, author)
            if err:
                self.finsih(err)
                return
            self.finish('S')
            return
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
        """
        authors = self.get_arguments('authors')
        attach_file = self.request.files['attach_file'][0]
        """
        err, pid = yield from PaperuploadService.inst.upload(self.acct['uid'], chinesetitle, englishtitle, chineseabstract, englishabstract, letter, picnum, wordnum, submitted, confirm, conflict, conflict_explain, anony_file, non_anony_file, author, chinesekeywords, englishkeywords)
        if err:
            self.finish(err)
            return
        self.finish('S')
        return

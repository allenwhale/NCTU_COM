from req import RequestHandler
from req import reqenv

class PaperuploadService:
    def __init__(self, db):
        self.db = db
        PaperuploadService.inst = self

class PaperuploadHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render('paperupload.html')
        return

    @reqenv
    def post(self):
        classification = str(self.get_argument('classification', default=''))
        area = str(self.get_argument('area', default=''))
        chinesetitle = str(self.get_argument('chinesetitle', default=''))
        englishtitle = str(self.get_argument('englishtitle', default=''))
        chineseabstract = str(self.get_argument('chineseabstract', default=''))
        englishabstract = str(self.get_argument('englishabstract', default=''))
        chinesekeywords = list(self.get_arguments('chinesekeywords', default=''))
        englishkeywords = list(self.get_arguments('englishkeywords', default=''))
        authors = self.get_arguments('authors')
        letter = self.get_argument('letter', default='')
        picnum = self.get_argument('picnum', default='')
        wordnum = self.get_argument('wordnum', default='')
        submitted = self.get_argument('submitted', default='')
        confirm = self.get_arguments('confirm')
        conflict
        pass

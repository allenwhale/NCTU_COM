import re
import subprocess as sp
class MailHandler:
    def __init__(self, template):
        fd = open(template, 'r')
        self.templ = fd.read()

    def send(self, to, subject, cc=[], bcc=[], **kwargs):
        content = re.sub('<%(?P<name>.*)?%>', lambda m: kwargs[m.group('name')], self.templ)
        cmd = 'mail -s "$(echo "'+subject+'\nContent-Type: text/html\n")" '+to
        try:
            p = sp.Popen(cmd, stdin=sp.PIPE, shell=True)
            p.stdin.write(content.encode())
            p.communicate()
            p.stdin.close()
        except:
            return 1
        return None

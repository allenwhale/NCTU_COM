import re
import subprocess as sp
class MailHandler:
    def __init__(self, template):
        fd = open(template, 'r')
        self.templ = fd.read()

    def send(self, to, subject, cc=[], bcc=[], **kwargs):
        content = re.sub('<%(?P<name>.*)?%>', lambda m: kwargs[m.group('name')], self.templ)
        cmd = ['mail', '-s', subject, '-a', 'Content-Type: text/html', to]
        try:
            p = sp.Popen(cmd, stdin=sp.PIPE)
            print(p)
            p.stdin.write(content.encode())
            err = p.communicate()[0]
            print(err)
            p.stdin.close()
        except:
            return 1
        return None

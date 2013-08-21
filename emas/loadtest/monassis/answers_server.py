import os
import re
import sys
import cPickle
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler


class AnswerRequestHandler(SimpleHTTPRequestHandler):
    
    print 'Loading answers...'
    filename = os.path.join(os.getcwd(),
                            'src', 'emas.loadtest', 'emas', 'loadtest',
                            'monassis', 'oracular-answers.pickle')
    answers = cPickle.load(open(filename,'rb'))
    print 'done.'

    def do_GET(self):
        tid = sid = ''

        tid_exp = re.compile('^GET\ \/\?templateId=([0-9]*)')
        matches = tid_exp.findall(self.requestline)
        if matches:
            tid = int(matches[0])

        sid_exp = re.compile('&seed=([0-9]*)')
        matches = sid_exp.findall(self.requestline)
        if matches:
            sid = int(matches[0])
       
        if not tid in self.answers.keys():
            self.wfile.write('Could not find template:%s' % tid)
            return

        try:
            self.wfile.write(self.answers[tid][sid])
        except IndexError:
            self.wfile.write('Could not find answers for :%s' % sid)


HandlerClass = AnswerRequestHandler
ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('127.0.0.1', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()

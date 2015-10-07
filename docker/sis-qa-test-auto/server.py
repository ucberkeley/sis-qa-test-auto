#!/usr/bin/env python3

import subprocess

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer

__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"


class TestHandler(RequestHandler):
    def get(self):
        subprocess.call(['bundle', 'exec', 'cucumber'])
        self.write('tests completed!\n')


class CloseHandler(RequestHandler):
    def post(self):
        print('Server shutting down!')
        server.stop()


app = Application([
    (r'/close', CloseHandler),
    (r'/.*', TestHandler),
])

if __name__ == '__main__':
    import sys
    port = sys.argv[1] if len(sys.argv) >= 2 else 8421

    server = HTTPServer(app)
    server.bind(port)
    server.start(0)
    print('Server ready!')
    IOLoop.current().start()

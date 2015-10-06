#!/usr/bin/env python3

import subprocess

import tornado.ioloop
import tornado.web

__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        subprocess.call(['bundle', 'exec', 'cucumber'])
        self.write('tests completed!\n')


class CloseHandler(tornado.web.RequestHandler):
    def post(self):
        print('Server shutting down!')
        tornado.ioloop.IOLoop.current().stop()


app = tornado.web.Application([
    (r'/close', CloseHandler),
    (r'/.*', TestHandler),
])

if __name__ == '__main__':
    app.listen(8421)
    print('Server ready!')
    tornado.ioloop.IOLoop.current().start()

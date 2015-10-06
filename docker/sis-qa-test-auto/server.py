#!/usr/bin/env python

import subprocess

import tornado.ioloop
import tornado.web

__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        subprocess.call(['bundle', 'exec', 'cucumber'])
        self.write('tests completed!\n')

app = tornado.web.Application([
    (r'/.*', MainHandler),
])

if __name__ == '__main__':
    app.listen(8421)
    tornado.ioloop.IOLoop.current().start()

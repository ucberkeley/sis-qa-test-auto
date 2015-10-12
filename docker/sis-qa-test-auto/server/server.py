#!/usr/bin/env python3

from datetime import datetime
import os.path as osp

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

from __init__ import LOGS_DIR
from executor import TestResultsManager, TestsExecutor

__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"


class BaseHandler(RequestHandler):
    def initialize(self, executor):
        self.executor = executor


class ExecuteHandler(BaseHandler):
    def post(self):
        test_uuid = str(datetime.now().strftime("%Y%m%d%H%M%S%f"))
        self.executor.submit(test_uuid)
        self.write(test_uuid)


class StatusHandler(BaseHandler):
    def get(self, test_uuid):
        test_result = self.executor.current_tests.get(test_uuid, None)
        if test_result is not None:
            self.write(test_result.counters)
            return

        counters_file = osp.join(LOGS_DIR, test_uuid, 'result_counters.json')
        if osp.isfile(counters_file):
            with open(counters_file) as f:
                self.write(f.read())


if __name__ == '__main__':
    import sys
    port = sys.argv[1] if len(sys.argv) >= 2 else 8421

    with TestResultsManager() as manager:
        with TestsExecutor(results_manager=manager) as executor:
            init_kwargs = dict(executor=executor)
            app = Application([
                (r'/execute', ExecuteHandler, init_kwargs),
                (r'/status/(.*)', StatusHandler, init_kwargs)
            ])
            app.listen(port)
            print('Server ready!')
            IOLoop.current().start()

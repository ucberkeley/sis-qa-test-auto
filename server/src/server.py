#!/usr/bin/env python3

from datetime import datetime
import os.path as osp

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

from __init__ import LOGS_DIR
from executor import TestsExecResultsManager, TestsExecutor

__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"


class BaseHandler(RequestHandler):
    def initialize(self, executor):
        self.executor = executor


class ExecuteHandler(BaseHandler):
    def post(self):
        tests_exec_uuid = str(datetime.now().strftime("%Y%m%d%H%M%S%f"))
        self.executor.submit(tests_exec_uuid)
        self.write(tests_exec_uuid)


class StatusHandler(BaseHandler):
    def get(self, tests_exec_uuid):
        # check if tests are executing currently
        tests_exec_result = self.executor.current_tests_execs.get(tests_exec_uuid, None)
        if tests_exec_result is not None:
            self.write(tests_exec_result.counters)
            return

        # check if tests have already been completely executed.
        counters_file = osp.join(LOGS_DIR, tests_exec_uuid, 'result_counters.json')
        if osp.isfile(counters_file):
            with open(counters_file) as f:
                self.write(f.read())
            return

        self.send_error(400,
                        reason='Tests execution run with UUID {} does not exist'.format(tests_exec_uuid))


if __name__ == '__main__':
    import sys
    port = sys.argv[1] if len(sys.argv) >= 2 else 8421

    with TestsExecResultsManager() as manager:
        with TestsExecutor(results_manager=manager) as executor:
            init_kwargs = dict(executor=executor)
            app = Application([
                (r'/execute', ExecuteHandler, init_kwargs),
                (r'/status/(.*)', StatusHandler, init_kwargs)
            ])
            app.listen(port)
            print('Server ready!')
            IOLoop.current().start()

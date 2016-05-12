#!/usr/bin/env python3

from datetime import datetime
import json
import os.path as osp

from tornado.web import RequestHandler

from . import LOGS_DIR
from .executor import TestExecStatusEnum

__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"


class BaseHandler(RequestHandler):
    def initialize(self, executor):
        self.executor = executor

    def write_json(self, json_str: str):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json_str)


class TestsExecsListHandler(BaseHandler):
    def get(self, *args, **kwargs):
        status_name = self.get_argument('status', '')
        if status_name:
            status = ''
            try:
                status = TestExecStatusEnum[status_name]
            except KeyError:
                self.send_error(400,
                                reason='{} is not a valid status'.format(status_name))
                return
            results = []
            for uuid, test_exec_result in self.executor.current_test_execs.items():
                if test_exec_result.status == status:
                    results.append(uuid)
        else:
            results = list(self.executor.current_test_execs.keys())
        self.write_json(json.dumps(results))


class ExecuteHandler(BaseHandler):
    def post(self):
        test_exec_uuid = str(datetime.now().strftime("%Y%m%d%H%M%S%f"))
        self.executor.submit(test_exec_uuid)
        self.write(test_exec_uuid)


class StatusHandler(BaseHandler):
    def get(self, test_exec_uuid):
        # check if tests are executing currently
        test_exec_result = self.executor.current_test_execs.get(test_exec_uuid, None)
        if test_exec_result is not None:
            # print(test_exec_result.json())
            self.write_json(test_exec_result.json())
            return

        # print(self.executor.current_test_execs)

        # check if tests have already completely executed.
        tests_log_dir = osp.join(LOGS_DIR, test_exec_uuid)
        if osp.exists(tests_log_dir):
            result_file = osp.join(tests_log_dir, 'result.json')
            if osp.isfile(result_file):
                with open(result_file) as result_in:
                    self.write_json(result_in.read())
            return

        self.send_error(400,
                        reason='Tests execution run with UUID {} does not exist'.format(test_exec_uuid))

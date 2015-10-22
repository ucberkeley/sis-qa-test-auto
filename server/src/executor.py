#!/usr/bin/env python3

from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import enum
import json
from multiprocessing.managers import BaseManager, NamespaceProxy
import os
import os.path as osp
import subprocess

from multiprocessing import Process

from __init__ import LOGS_DIR

__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"



class TestsExecResult:
    """Wrapper for the results of executing a set of tests.

    This provides conversion from test output to result and an iterator
    for easy recording of results.
    """

    class TestStep:
        symbol_result_map = {
            '.': 'passed',
            'F': 'failed',
            '-': 'skipped',
        }

        def __init__(self, result: 'TestsExecResult' or 'TestsExecResultProxy', step: dict):
            self.tests_exec_results = result
            self._step = step

        def set_result(self, symbol: str):
            result = self.symbol_result_map[symbol]
            self._step['result']['status'] = result
            self.tests_exec_results.update_counters(result)

    def __init__(self, status=None, counters=None):
        self.status = status if status is not None else TestsExecStatusEnum.queued
        self.data = None
        self.counters = counters if counters is not None else Counter()

    def json(self):
        return json.dumps({
            'status': self.status.name.upper(),
            'counters': self.counters,
        }, indent=4)

    def iterator(self):
        if self.data is None:
            return

        for test_file in self.data:
            for test_scenario in test_file['elements']:
                for test_step in test_scenario['steps']:
                    yield TestsExecResult.TestStep(self, test_step)

    def update_counters(self, curr_result: str):
        self.counters[curr_result] += 1
        self.counters['completed'] += 1


@enum.unique
class TestsExecStatusEnum(enum.Enum):
    errored = -1
    done = 0
    queued = 1
    dryrun = 2
    executing = 3


class TestsExecResultProxy(NamespaceProxy):
    """Proxy for TestsSetResult, for syncing between multiple processes."""
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__',
                 'update_counters')

    def iterator(self):
        return TestsExecResult.iterator(self)

    def update_counters(self, curr_result: str):
        return self._callmethod('update_counters', (curr_result, ))


class TestsExecResultsManager(BaseManager):
    pass

TestsExecResultsManager.register('TestsExecResult', TestsExecResult, TestsExecResultProxy)
# TestsExecResultsManager.register('TestsExecResult_Status', TestsExecResult.Status)


CUCUMBER_DRYRUN_CMD = 'bundle exec cucumber -d -f json'
CUCUMBER_EXECUTION_CMD = 'bundle exec cucumber -f json -o {output}' \
                         ' -f progress'

def execute_tests(tests_exec_uuid: str, tests_exec_result: TestsExecResult or TestsExecResultProxy):
    logs_output = osp.join(LOGS_DIR, tests_exec_uuid)
    subprocess.check_call('mkdir -p {}'.format(logs_output).split())

    try:
        # dryrun
        tests_exec_result.status = TestsExecStatusEnum.dryrun
        dryrun = subprocess.Popen(CUCUMBER_DRYRUN_CMD.split(),
                                  stdout=subprocess.PIPE)
        json_data = dryrun.stdout.read().decode('utf-8')
        tests_exec_result.data = json.loads(json_data)

        # execution
        tests_exec_result.status = TestsExecStatusEnum.executing
        results_output_file = os.path.join(logs_output, 'cucumber_report.json')
        execution = subprocess.Popen(
            CUCUMBER_EXECUTION_CMD.format(output=results_output_file).split(),
            stdout=subprocess.PIPE)
        for test_step in tests_exec_result.iterator():
            symbol = execution.stdout.read1(1).decode('utf-8')
            test_step.set_result(symbol)

        # completion
        tests_exec_result.status = TestsExecStatusEnum.done
    except subprocess.SubprocessError as error:
        tests_exec_result.status = TestsExecStatusEnum.errored
        tests_exec_result.data = error
        with open(osp.join(logs_output, 'error.txt'), 'w') as error_out:
            error_out.write(error)
    finally:
        with open(osp.join(logs_output, 'result.json'), 'w') as result_out:
            result_out.write(tests_exec_result.json())


class TestsExecutor(ProcessPoolExecutor):
    """ProcessPoolExecutor implementation for tests set execution.

    This implementation adds a dictionary of current tests sets which get
    updated when tests set executions are requested and when tests set
    executions are completed.
    """

    def __init__(self, results_manager: TestsExecResultsManager, max_workers: int=None):
        super().__init__(max_workers)
        self.current_tests_execs = {}
        self.results_manager = results_manager

    def submit(self, tests_exec_uuid: str):
        tests_exec_result = self.results_manager.TestsExecResult()
        self.current_tests_execs[tests_exec_uuid] = tests_exec_result
        future = super().submit(execute_tests, tests_exec_uuid, tests_exec_result)
        future.add_done_callback(lambda _: self.current_tests_execs.pop(tests_exec_uuid))


#!/usr/bin/env python3

from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import json
from multiprocessing.managers import BaseManager, NamespaceProxy
import os
import os.path as osp
import subprocess

from __init__ import LOGS_DIR

__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"



class TestResult:
    """Wrapper for test results.

    This provides conversion from test output to result and an iterator
    for easy recording of results.
    """

    ERRORED = -1
    DONE = 0
    QUEUED = 1
    DRYRUN = 2
    RUNNING = 3

    class TestStep:
        symbol_result_map = {
            '.': 'passed',
            'F': 'failed',
            '-': 'skipped',
        }

        def __init__(self, result: 'TestResult' or 'TestResultProxy', step: dict):
            self._test_results = result
            self._step = step

        def set_result(self, symbol: str):
            result = self.symbol_result_map[symbol]
            self._step['result']['status'] = result
            self._test_results.update_counters(result)

    def __init__(self, status=None):
        self.status = status if status is not None else self.QUEUED
        self.data = None
        self.counters = Counter()

    def iterator(self):
        if self.data is None:
            return

        for test_file in self.data:
            for test_scenario in test_file['elements']:
                for test_step in test_scenario['steps']:
                    yield TestResult.TestStep(self, test_step)

    def update_counters(self, curr_result: str):
        self.counters[curr_result] += 1
        self.counters['completed'] += 1


class TestResultProxy(NamespaceProxy):
    """Proxy for TestResult, for syncing between multiple processes."""
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__',
                 'update_counters')

    def iterator(self):
        return TestResult.iterator(self)

    def update_counters(self, curr_result: str):
        return self._callmethod('update_counters', (curr_result, ))


class TestResultsManager(BaseManager):
    pass

TestResultsManager.register('TestResult', TestResult, TestResultProxy)


CUCUMBER_DRYRUN_CMD = 'bundle exec cucumber -d -f json'
CUCUMBER_EXECUTION_CMD = 'bundle exec cucumber -f json -o {output}' \
                         ' -f progress'

def execute_tests(test_uuid: str, test_result: TestResult or TestResultProxy):
    try:
        # dryrun
        test_result.status = TestResult.DRYRUN
        dryrun = subprocess.Popen(CUCUMBER_DRYRUN_CMD.split(),
                                  stdout=subprocess.PIPE)
        json_data = dryrun.stdout.read().decode('utf-8')
        test_result.data = json.loads(json_data)

        # execution
        test_result.status = TestResult.RUNNING
        logs_output = osp.join(LOGS_DIR, test_uuid)
        subprocess.check_call('mkdir -p {}'.format(logs_output).split())
        results_output_file = os.path.join(logs_output, 'results.json')
        execution = subprocess.Popen(
            CUCUMBER_EXECUTION_CMD.format(output=results_output_file).split(),
            stdout=subprocess.PIPE)
        for test_step in test_result.iterator():
            symbol = execution.stdout.read1(1).decode('utf-8')
            test_step.set_result(symbol)

        # completion
        test_result.status = TestResult.DONE
        with open(osp.join(logs_output, 'result_counters.json'), 'w') as out:
            json.dump(test_result.counters, out)
    except subprocess.SubprocessError as error:
        test_result.status = TestResult.ERRORED
        test_result.data = error


class TestsExecutor(ProcessPoolExecutor):
    """ProcessPoolExecutor implementation for test execution.

    This implementation adds a dictionary of current tests which get
    updated when test executions are requested and when test executions
    are completed.
    """

    def __init__(self, results_manager: TestResultsManager, max_workers=None):
        super().__init__(max_workers)
        self.current_tests = {}
        self.results_manager = results_manager

    def submit(self, test_uuid: str):
        test_result = self.results_manager.TestResult()
        self.current_tests[test_uuid] = test_result
        future = super().submit(execute_tests, test_uuid, test_result)
        future.add_done_callback(lambda _: self.current_tests.pop(test_uuid))


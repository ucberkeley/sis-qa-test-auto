#!/usr/bin/env python3

from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import enum
import json
import multiprocessing
from multiprocessing.managers import BaseManager, NamespaceProxy
import os
import os.path as osp
import subprocess

from . import LOGS_DIR

__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"


@enum.unique
class TestExecStatusEnum(enum.Enum):
    errored = -1
    done = 0
    queued = 1
    dryrun = 2
    executing = 3


class TestExecResult:
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

        def __init__(self, result: 'TestExecResult' or 'TestExecResultProxy', step: dict):
            self.test_exec_result = result
            self.step = step

        def set_result(self, symbol: str):
            result = self.symbol_result_map[symbol]
            self.step['result']['status'] = result
            self.test_exec_result.update_counters(result)

    def __init__(self, status: TestExecStatusEnum=TestExecStatusEnum.queued,
                 counters: dict=None, data=None):
        self.status = status
        self.counters = counters if counters is not None else Counter()
        self._data = data if data is not None else []
        self._step_refs = list(test_step.step for test_step in self.iterator())
        self._step_ref_pos = 0

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self._step_refs = list(test_step.step for test_step in self.iterator())
        self.counters['total'] = sum(1 for _ in self.iterator())

    def json(self):
        steps = []
        for test_file in self._data:
            file = []
            for test_scenario in test_file['elements']:
                scenario = []
                for test_step in test_scenario['steps']:
                    scenario.append([
                        test_step['keyword'] + test_step['name'],
                        test_step['result']['status']
                    ])
                file.append(scenario)
            steps.append(file)
        return json.dumps({
            'status': self.status.name.upper(),
            'counters': self.counters,
            'steps': steps
        }, indent=4)

    def iterator(self):
        if self.data is None or isinstance(self.data, Exception):
            return

        for test_file in self.data:
            for test_scenario in test_file['elements']:
                for test_step in test_scenario['steps']:
                    yield TestExecResult.TestStep(self, test_step)

    def update_counters(self, curr_result: str):
        step = self._step_refs[self._step_ref_pos]
        step['result']['status'] = curr_result
        self._step_ref_pos += 1
        self.counters[curr_result] += 1
        self.counters['completed'] += 1


class TestExecResultProxy(NamespaceProxy):
    """Proxy for TestExecResult, for syncing between multiple processes."""
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__',
                 'update_counters')

    def iterator(self):
        return TestExecResult.iterator(self)

    def update_counters(self, curr_result: str):
        return self._callmethod('update_counters', (curr_result, ))


class TestExecResultsManager(BaseManager):
    pass

TestExecResultsManager.register('TestExecResult', TestExecResult, TestExecResultProxy)


CUCUMBER_DRYRUN_CMD = 'bundle exec cucumber -d' \
                      ' -f json'
CUCUMBER_EXECUTION_CMD = 'bundle exec cucumber' \
                         ' -f json -o {output}' \
                         ' -f progress'


def execute_tests(test_exec_uuid: str, test_exec_result: TestExecResult or TestExecResultProxy):
    print('{worker}: starting {uuid}'.format(worker=multiprocessing.current_process().name,
                                             uuid=test_exec_uuid))
    logs_output = osp.join(LOGS_DIR, test_exec_uuid)
    subprocess.check_call('mkdir -p {}'.format(logs_output).split())

    try:
        # dryrun
        test_exec_result.status = TestExecStatusEnum.dryrun
        dryrun = subprocess.Popen(CUCUMBER_DRYRUN_CMD.split(),
                                  stdout=subprocess.PIPE)
        json_data = dryrun.stdout.read().decode('utf-8')
        test_exec_result.data = json.loads(json_data)

        # execution
        test_exec_result.status = TestExecStatusEnum.executing
        results_output_file = os.path.join(logs_output, 'cucumber_report.json')
        execution = subprocess.Popen(
            CUCUMBER_EXECUTION_CMD.format(output=results_output_file).split(),
            stdout=subprocess.PIPE)
        for test_step in test_exec_result.iterator():
            symbol = execution.stdout.read1(1).decode('utf-8')
            test_step.set_result(symbol)

        # completion
        test_exec_result.status = TestExecStatusEnum.done
    except Exception as error:
        test_exec_result.status = TestExecStatusEnum.errored
        print(error)
        test_exec_result.data = error
        with open(osp.join(logs_output, 'error.txt'), 'w') as error_out:
            error_out.write(str(error))
    finally:
        with open(osp.join(logs_output, 'result.json'), 'w') as result_out:
            result_out.write(test_exec_result.json())


class TestsExecutor(ProcessPoolExecutor):
    """ProcessPoolExecutor implementation for tests set execution.

    This implementation adds a dictionary of current tests sets which get
    updated when tests set executions are requested and when tests set
    executions are completed.
    """
    def __init__(self, results_manager: TestExecResultsManager, max_workers: int=None,
                 execute_tests_func=execute_tests):
        super().__init__(max_workers)
        self.current_test_execs = {}
        self.results_manager = results_manager
        self.execute_tests_func = execute_tests_func

    def submit(self, test_exec_uuid: str):
        test_exec_result = self.results_manager.TestExecResult()
        self.current_test_execs[test_exec_uuid] = test_exec_result
        future = super().submit(self.execute_tests_func, test_exec_uuid, test_exec_result)
        future.add_done_callback(lambda _: self.current_test_execs.pop(test_exec_uuid))

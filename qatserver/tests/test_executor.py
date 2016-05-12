#!/usr/bin/env python3

from enum import Enum
import json
import os.path as osp
from multiprocessing import Pipe
import pytest

from qatserver.executor import TestExecResult, TestsExecutor

__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"


class StubTestExecResultsManager:
    def __init__(self):
        self.TestExecResult_called = None
        self.stub_reset()

    def stub_reset(self):
        self.TestExecResult_called = False

    def TestExecResult(self):
        self.TestExecResult_called = True


class StubExecuteTestsFuncConnMessages(Enum):
    CALLED = 1
    COMPLETE = 2


class StubExecuteTestsFunc:
    def __init__(self):
        self.main_conn, self.func_conn = Pipe()
        self._called = self._complete = None
        self.stub_reset()

    def stub_reset(self):
        self._called = self._complete = False

    def stub_complete(self):
        self._complete = True
        self.main_conn.send(StubExecuteTestsFuncConnMessages.COMPLETE)

    def stub_called(self):
        if not self._called and self.main_conn.poll():
            conn_message = self.main_conn.recv()
            if conn_message == StubExecuteTestsFuncConnMessages.CALLED:
                self._called = True
        return self._called

    def __enter__(self):
        self.stub_reset()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stub_complete()

    def __call__(self, *_):
        self._called = True
        self.func_conn.send(StubExecuteTestsFuncConnMessages.CALLED)
        while not self._complete:
            conn_message = self.func_conn.recv()
            if conn_message == StubExecuteTestsFuncConnMessages.COMPLETE:
                self._complete = True


class TestTestExecResult:
    @pytest.fixture
    def test_cucumber_report(self):
        with open(osp.join(osp.dirname(__file__), 'test_cucumber_report.json')) as report:
            return json.load(report)

    @pytest.fixture
    def result(self, test_cucumber_report):
        r = TestExecResult()
        r.data = test_cucumber_report
        return r

    @staticmethod
    def assert_correct_number_of_counters(counters, passed=0, failed=0, skipped=0):
        assert counters['passed'] == passed, 'not the correct number of passed'
        assert counters['failed'] == failed, 'not the correct number of failed'
        assert counters['skipped'] == skipped, 'not the correct number of skipped'
        assert counters['completed'] == passed + failed + skipped, \
            'not the correct number of completed'

    def test_iterator(self, result):
        expected_steps = set()
        for file in result.data:
            for element in file['elements']:
                for step in element['steps']:
                    expected_steps.add(step['name'])

        actual_total_steps = 0
        for test_step in result.iterator():
            assert test_step.step['name'] in expected_steps, 'test step not in expected steps'
            actual_total_steps += 1
        assert actual_total_steps == len(expected_steps), 'not the expected number of test steps'

    def test_initial_counters(self, result):
        assert result.counters == {
            'total': (5 + 3) + 5
        }, 'result counters not initialized correctly'

    def test_update_counters(self, result):
        self.assert_correct_number_of_counters(result.counters)

        result.update_counters('passed')
        self.assert_correct_number_of_counters(result.counters,
                                               passed=1)

        result.update_counters('passed')
        self.assert_correct_number_of_counters(result.counters,
                                               passed=2)

        result.update_counters('failed')
        self.assert_correct_number_of_counters(result.counters,
                                               passed=2, failed=1)

        result.update_counters('skipped')
        self.assert_correct_number_of_counters(result.counters,
                                               passed=2, failed=1, skipped=1)

        result.update_counters('skipped')
        self.assert_correct_number_of_counters(result.counters,
                                               passed=2, failed=1, skipped=2)

    def test_test_step(self, result):
        assert result.counters['total'] > 0, 'no test steps for test'
        it = result.iterator()

        try:
            self.assert_correct_number_of_counters(result.counters)

            next(it).set_result('.')
            self.assert_correct_number_of_counters(result.counters,
                                                   passed=1)

            next(it).set_result('.')
            self.assert_correct_number_of_counters(result.counters,
                                                   passed=2)

            next(it).set_result('F')
            self.assert_correct_number_of_counters(result.counters,
                                                   passed=2, failed=1)

            next(it).set_result('-')
            self.assert_correct_number_of_counters(result.counters,
                                                   passed=2, failed=1, skipped=1)

            next(it).set_result('-')
            self.assert_correct_number_of_counters(result.counters,
                                                   passed=2, failed=1, skipped=2)
        except StopIteration:
            raise RuntimeError('not enough test steps for test')


class TestTestsExecutor:
    @pytest.yield_fixture
    def executor(self):
        manager = StubTestExecResultsManager()
        with StubExecuteTestsFunc() as func, TestsExecutor(manager, 1, func) as e:
            yield e
            e.shutdown(wait=False)

    @pytest.mark.timeout(timeout=5)
    def test_submit(self, executor):
        executor.results_manager.stub_reset()
        executor.execute_tests_func.stub_reset()

        assert len(executor.current_test_execs) == 0, \
            'erroneous current_test_exec instance on initialization'

        sample_test_exec_uuid = 'sample_uuid'
        executor.submit(sample_test_exec_uuid)
        assert executor.results_manager.TestExecResult_called, \
            'TestExecResult not used'
        assert sample_test_exec_uuid in executor.current_test_execs, \
            'test exec instance not added to current_test_execs'

        while not executor.execute_tests_func.stub_called():
            pass
        assert executor.execute_tests_func.stub_called(), \
            'execute_tests_func not called'

        executor.execute_tests_func.stub_complete()
        while sample_test_exec_uuid in executor.current_test_execs:
            pass
        assert sample_test_exec_uuid not in executor.current_test_execs, \
            'test exec instance not removed from current_test_exec'

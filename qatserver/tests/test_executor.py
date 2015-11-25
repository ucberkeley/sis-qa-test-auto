#!/usr/bin/env python3

import copy
import json
import os.path as osp
import pytest

from qatserver.executor import TestExecResult

__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"


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

    def test_iterator(self, result):
        expected_steps = set()
        for file in result.data:
            for element in file['elements']:
                for step in element['steps']:
                    expected_steps.add(step['name'])

        actual_total_steps = 0
        for test_step in result.iterator():
            assert test_step._step['name'] in expected_steps, 'test step not in expected steps'
            actual_total_steps += 1
        assert actual_total_steps == len(expected_steps), 'not the expected number of test steps'

    def test_initial_counters(self, result):
        assert result.counters == {
            'total': (5 + 3) + 5
        }, 'result counters not initialized correctly'

    def test_update_counters(self, result):
        def assert_correct_number_of_counters(counters, passed=0, failed=0, skipped=0):
            assert counters['passed'] == passed, 'not the correct number of passed'
            assert counters['failed'] == failed, 'not the correct number of failed'
            assert counters['skipped'] == skipped, 'not the correct number of skipped'
            assert counters['completed'] == passed + failed + skipped, \
                'not the correct number of completed'

        assert_correct_number_of_counters(result.counters)

        result.update_counters('passed')
        assert_correct_number_of_counters(result.counters,
                                          passed=1)

        result.update_counters('passed')
        assert_correct_number_of_counters(result.counters,
                                          passed=2)

        result.update_counters('failed')
        assert_correct_number_of_counters(result.counters,
                                          passed=2, failed=1)

        result.update_counters('skipped')
        assert_correct_number_of_counters(result.counters,
                                          passed=2, failed=1, skipped=1)

        result.update_counters('skipped')
        assert_correct_number_of_counters(result.counters,
                                          passed=2, failed=1, skipped=2)

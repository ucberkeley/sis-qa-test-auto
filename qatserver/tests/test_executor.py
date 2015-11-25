#!/usr/bin/env python3

import os.path as osp
import json
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

    def test_initial_counters(self, result):
        assert result.counters == {
            'total': (5 + 3) + 5,
        }, 'result counters not initialized correctly'

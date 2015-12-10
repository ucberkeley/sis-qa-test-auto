#!/usr/bin/env python3

import os
import os.path as osp

__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"

SIS_LOGS_DIR_ENV = 'SIS_LOGS_DIR'
try:
    LOGS_DIR = osp.abspath(os.environ[SIS_LOGS_DIR_ENV])
except KeyError:
    LOGS_DIR = osp.abspath(osp.join(osp.dirname(__file__), '..', '..', 'logs'))

SIS_TEST_DIR_ENV = 'SIS_TEST_DIR'
try:
    TEST_DIR = osp.abspath(os.environ[SIS_TEST_DIR_ENV])
except KeyError:
    raise KeyError('{} environment variable not set'.format(SIS_TEST_DIR_ENV))

#!/usr/bin/env python3

import os
import os.path as osp

__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"

SIS_LOGS_DIR_ENV = 'SIS_LOGS_DIR'
if SIS_LOGS_DIR_ENV in os.environ:
    LOGS_DIR = osp.abspath(os.environ['SIS_LOGS_DIR'])
else:
    LOGS_DIR = osp.abspath(osp.join(osp.dirname(__file__), '..', '..', 'logs'))

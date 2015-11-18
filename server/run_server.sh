#!/usr/bin/env bash
source /etc/profile.d/rvm.sh
cd /test
bundle install
SIS_TEST_DIR=/test \
  SIS_LOGS_DIR=/logs \
  ./../server/src/server.py "$@"

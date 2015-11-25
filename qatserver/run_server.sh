#!/usr/bin/env bash

: ${SIS_SERVER_PORT:=8421}

source /etc/profile.d/rvm.sh
cd /test
bundle install
SIS_TEST_DIR=/test \
  SIS_LOGS_DIR=/logs \
  ./../qatserver/qatserver/server.py ${SIS_SERVER_PORT} ${SIS_SERVER_EXTRA_ARGS}

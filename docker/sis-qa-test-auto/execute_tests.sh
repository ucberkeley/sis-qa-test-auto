#!/usr/bin/env bash
source /etc/profile.d/rvm.sh
cd /test
bundle install
export SIS_TEST_DIR=/test
bundle exec cucumber
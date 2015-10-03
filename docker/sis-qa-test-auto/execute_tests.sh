#!/usr/bin/env bash
source /etc/profile.d/rvm.sh
cd /test
bundle install
bundle exec cucumber
#!/usr/bin/env bash
source /home/developer/.rvm/scripts/rvm
# rvm rvmrc warning ignore /test/.rvmrc
cd /test
bundle install
bundle exec cucumber
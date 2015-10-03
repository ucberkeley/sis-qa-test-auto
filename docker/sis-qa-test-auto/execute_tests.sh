#!/usr/bin/env bash
source ${HOME}/.rvm/scripts/rvm
cd /test
bundle install
bundle exec cucumber
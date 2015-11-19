#!/usr/bin/env bash

: ${SIS_DASHBOARD_PORT:=3000}

cd /dashboard
bundle install
npm install
bin/rails server -p ${SIS_DASHBOARD_PORT}

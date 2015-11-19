#!/usr/bin/env bash

if [ $( id | sed -e 's/(.*//' ) == "uid=0" ]; then
  echo "Please rerun without super user privileges. "
  exit 1
fi

: ${DOCKER_NAMESPACE:=ucberkeley}
project_dir=$(cd $(dirname ${BASH_SOURCE[0]})/.. && pwd )
: ${SIS_TEST_DIR:=${project_dir}/test}
SIS_SERVER_DIR=${project_dir}/server

if [ -f ${SIS_TEST_DIR}/Gemfile ] && ! cmp --silent ${SIS_TEST_DIR}/Gemfile ${SIS_SERVER_DIR}/Gemfile; then
  cp ${SIS_TEST_DIR}/Gemfile ${SIS_SERVER_DIR}
  if [ -f ${SIS_TEST_DIR}/Gemfile.lock ]; then
    cp ${SIS_TEST_DIR}/Gemfile.lock ${SIS_SERVER_DIR}
  fi
  echo "Server Docker image stale. Synced and rebuilding..."
  ./build.sh server
fi

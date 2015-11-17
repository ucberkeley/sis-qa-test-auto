#!/usr/bin/env bash

if [ $( id | sed -e 's/(.*//' ) == "uid=0" ]; then
  echo "Please rerun without super user privileges. "
  exit 1
fi

: ${DOCKER_NAMESPACE:=ucberkeley}
project_dir=$(cd $(dirname ${BASH_SOURCE[0]})/.. && pwd )
: ${SIS_TEST_DIR:=${project_dir}/test}
DOCKER_IMAGE_DIR=${project_dir}/docker/sis-qa-test-auto

stale=false

diff -br ${project_dir}/server ${DOCKER_IMAGE_DIR}/server &> /dev/null;
if [ $? -ne 0 ]; then
  stale=true
  rm -rf ${DOCKER_IMAGE_DIR}/server
  cp -r ${project_dir}/server ${DOCKER_IMAGE_DIR}
fi

if [ -f ${SIS_TEST_DIR}/Gemfile ] && ! cmp --silent ${SIS_TEST_DIR}/Gemfile ${DOCKER_IMAGE_DIR}/Gemfile; then
  stale=true
  cp ${SIS_TEST_DIR}/Gemfile ${DOCKER_IMAGE_DIR}
  if [ -f ${SIS_TEST_DIR}/Gemfile.lock ]; then
      cp ${SIS_TEST_DIR}/Gemfile.lock ${DOCKER_IMAGE_DIR}
  fi
fi

if ${stale}; then
  echo "Docker image stale. Synced and rebuilding..."
  sudo docker build -t ${DOCKER_NAMESPACE}/sis-qa-test-auto ${DOCKER_IMAGE_DIR}
fi

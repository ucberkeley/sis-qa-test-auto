#!/usr/bin/env bash

if [ $( id | sed -e 's/(.*//' ) == "uid=0" ]; then
  echo "Please rerun without super user privileges. "
  exit 1
fi

: ${DOCKER_NAMESPACE:=ucberkeley}
PROJECT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
: ${SIS_TEST_DIR:=${PROJECT_DIR}/test}
DOCKER_IMAGE_DIR=${PROJECT_DIR}/docker/sis-qa-test-auto

if [ -f ${SIS_TEST_DIR}/Gemfile ] && ! cmp --silent ${SIS_TEST_DIR}/Gemfile ${DOCKER_IMAGE_DIR}/Gemfile; then
    echo "Gemfiles different. Syncing and rebuilding Docker image..."
    cp ${SIS_TEST_DIR}/Gemfile ${DOCKER_IMAGE_DIR}
    if [ -f ${SIS_TEST_DIR}/Gemfile.lock ]
    then
        cp ${SIS_TEST_DIR}/Gemfile.lock ${DOCKER_IMAGE_DIR}
    fi
    sudo docker build -t ${DOCKER_NAMESPACE}/sis-qa-test-auto ${DOCKER_IMAGE_DIR}
fi
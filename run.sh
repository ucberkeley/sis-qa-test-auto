#!/usr/bin/env bash

if [ `id | sed -e 's/(.*//'` != "uid=0" ]; then
  echo "Please rerun with super user privileges. "
  exit 1
fi

: ${DOCKER_NAMESPACE:=ucberkeley}
PROJECT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
: ${SIS_TEST_DIR:=${PROJECT_DIR}/test}
DOCKER_IMAGE=${DOCKER_NAMESPACE}/sis-qa-test-auto

docker inspect ${DOCKER_IMAGE} &> /dev/null; if [ $? -ne 0 ]; then
    docker pull ${DOCKER_IMAGE}
fi
docker run \
    --rm \
    --net=host \
    -t \
    -e DISPLAY=${DISPLAY} \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ${SIS_TEST_DIR}:/test \
    ${DOCKER_IMAGE}

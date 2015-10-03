#!/usr/bin/env bash

DOCKER_NAMESPACE=ucberkeley

PROJECT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
: ${CC_TEST_DIR:=${PROJECT_DIR}/test}
DOCKER_IMAGE=${DOCKER_NAMESPACE}/sis-qa-test-auto

docker pull ${DOCKER_IMAGE} && docker run \
    --rm \
    --net=host \
    -t \
    -e DISPLAY=${DISPLAY} \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ${CC_TEST_DIR}:/test \
    ${DOCKER_IMAGE}

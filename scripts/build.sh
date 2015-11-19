#!/usr/bin/env bash

: ${DOCKER_NAMESPACE:=ucberkeley}
project_dir=$(cd $(dirname ${BASH_SOURCE[0]})/.. && pwd )


build_server() {
sudo docker build \
  -t ${DOCKER_NAMESPACE}/sis-qa-test-auto-server \
  ${project_dir}/server
}

build_dashboard() {
sudo docker build \
  -t ${DOCKER_NAMESPACE}/sis-qa-test-auto-dashboard \
  ${project_dir}/dashboard
}


case "$1" in
  server)
    build_server
    ;;
  dashboard)
    build_dashboard
    ;;
  all)
    build_server
    build_dashboard
    ;;
esac

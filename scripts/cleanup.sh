#!/usr/bin/env bash

project_dir=$(cd $(dirname ${BASH_SOURCE[0]})/.. && pwd )
: ${SIS_LOGS_DIR:=${project_dir}/logs}
rm -rf ${SIS_LOGS_DIR}/*

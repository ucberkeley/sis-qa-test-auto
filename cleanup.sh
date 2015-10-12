#!/usr/bin/env bash

project_dir="$(dirname "$(readlink -f "$0")")"
: ${SIS_LOGS_DIR:=${project_dir}/logs}
rm -rf ${SIS_LOGS_DIR}/*

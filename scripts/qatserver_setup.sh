#!/usr/bin/env bash

project_dir=$(cd $(dirname ${BASH_SOURCE[0]})/.. && pwd)
export PYTHONPATH=project_dir/qatserver:${PYTHONPATH}

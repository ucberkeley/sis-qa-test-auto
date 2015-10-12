#!/usr/bin/env bash

if [ $( id | sed -e 's/(.*//' ) != "uid=0" ]; then
  echo "Please rerun with super user privileges. "
  exit 1
fi

project_dir=$(cd $(dirname ${BASH_SOURCE[0]})/.. && pwd )
ln -s ${project_dir}/qata /usr/bin/qata

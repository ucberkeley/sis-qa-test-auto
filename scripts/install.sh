#!/usr/bin/env bash

if [ $( id | sed -e 's/(.*//' ) != "uid=0" ]; then
  echo "Please rerun with super user privileges. "
  exit 1
fi

installation_target=/usr/bin/qata
if [ ! -f ${installation_target} ]; then
  project_dir=$(cd $(dirname ${BASH_SOURCE[0]})/.. && pwd )
  ln -s ${project_dir}/qata ${installation_target}
fi

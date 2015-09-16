#!/usr/bin/env bash

PROJECT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

sudo docker run \
  --rm \
  -t \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $PROJECT_DIR/test:/test \
  dibyo/firefox-browser-gui
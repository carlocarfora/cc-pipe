#!/bin/bash

# Export environment variables
export FPS=$1
export WIDTH=$2
export HEIGHT=$3
export PROJECT=$4
export TASK=$5
export SHOT=$6
export JOB=$7
export NUKE_PATH=$8

# Launch Nuke
pushd /usr/local/Nuke11.0v2
optirun ./Nuke11.0 --nc
popd


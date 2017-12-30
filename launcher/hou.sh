#!/bin/bash

# secho $@

# Source houdini env
pushd /opt/hfs16.0.557
source houdini_setup
popd

# Run license server
pushd /opt/hfs16.0.557/houdini/sbin
./sesinetd
popd

# Export environment variables
export FPS=$1
export WIDTH=$2
export HEIGHT=$3
export PROJECT=$4
export TASK=$5
export SHOT=$6
export JOB=$7


# Launch Houdini
vblank_mode=0 primusrun houdini


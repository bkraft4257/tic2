#!/usr/bin/env bash

study_switcher.py $@
source $TIC_INIT_PATH/tic_study_switcher.sh

echo "The ACTIVE_STUDY is now " $ACTIVE_STUDY
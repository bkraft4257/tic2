#!/usr/bin/env bash

tic_active_study_bash_script=${TIC_INIT_PATH}/tic_study_switcher.txt

study_switcher.py $@

source $tic_active_study_bash_script

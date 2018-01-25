#!/usr/bin/env bash

tic_active_study_bash_script=tic_study_switcher.txt

echo "Previous active study : " $ACTIVE_STUDY

study_switcher.py $@

source $tic_active_study_bash_script
# rm $tic_active_study_bash_script

echo "Current active study :" $ACTIVE_STUDY

term
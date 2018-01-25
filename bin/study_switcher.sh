#!/usr/bin/env bash

tic_active_study_bash_script=tic_study_switcher.txt


study_switcher.py $@

source $tic_active_study_bash_script

echo 'Current active study = ' $ACTIVE_STUDY

#rm $tic_active_study_bash_script

#!/usr/bin/env bash

study_switcher.py $@


params=$@

echo "$params" | grep -q "\-d"

if [ $? -ne 0 ];then
    source $TIC_INIT_PATH/tic_study_switcher.sh
    echo 'ACTIVE_STUDY is ' $ACTIVE_STUDY
fi

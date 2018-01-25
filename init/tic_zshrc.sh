#!/usr/bin/env bash

# TIC Environment Setup ======================================

# Users must define their TIC_PATH in the .zshrc file. 

if [ ! -d $TIC_PATH ]; then

    echo
    echo "$TIC_PATH does not exist. Please edit your .zshrc or .bashrc file accordingly."
    echo
    sleep 10

fi

source $TIC_PATH/init/tic_aliases.sh

export HOME_TIC_PATH=$TIC_INIT_PATH  # Done for backward compatibility.

source ${TIC_INIT_PATH}/tic_wake_aging1a_environment.sh


# TIC NIPYPE Workflows

PATH=$TIC_PATH/bin/:$TIC_PATH/workflows:$PATH
PYTHONDONTWRITEBYTECODE=1

umask 0002

echo
echo "TIC_PATH     : $TIC_PATH"
echo "SUBJECTS_DIR : $SUBJECTS_DIR"
echo "umask        : $(umask)"
echo

 

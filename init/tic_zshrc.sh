#!/usr/bin/env bash

# TIC Environment Setup ======================================

# Users must define their TIC_PATH in the .zshrc file. 

if [ ! -d $TIC_PATH ]; then

    echo
    echo "$TIC_PATH does not exist. Please edit your $HOME/.tic/tic.sh file."
    echo
    sleep 10

fi

source $TIC_PATH/tic_aliases.sh

export HOME_TIC_PATH=$HOME/.tic
source ${HOME_TIC_PATH}/tic_wake_software_environment.sh

# TIC NIPYPE Workflows

PATH=$TIC_PATH/nipype_workflows/:$PATH
PYTHONDONTWRITEBYTECODE=1

umask 0002

echo
echo "TIC_PATH     : $TIC_PATH"
echo "SUBJECTS_DIR : $SUBJECTS_DIR"
echo "umask        : $(umask)"
echo

 

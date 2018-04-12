#!/usr/bin/env bash

# TIC Environment Setup ======================================

# Users must define their TIC_PATH in the .zshrc file. 

if [ ! -d $TIC_PATH ]; then

    echo
    echo "$TIC_PATH does not exist. Please edit your .zshrc or .bashrc file accordingly."
    echo
    sleep 10

fi

export TIC_STUDIES_PATH=$TIC_PATH/studies
export TIC_PYTHONPATH=$TIC_PATH/:$TIC_PATH/bin

export PYTHONPATH=$TIC_PYTHONPATH:$PYTHONPATH

source $TIC_PATH/init/tic_aliases.sh
source $TIC_STUDIES_PATH/study/active/aliases.sh

export HOME_TIC_PATH=$TIC_INIT_PATH  # Done for backward compatibility.

source ${TIC_INIT_PATH}/tic_environment.sh

# TIC NIPYPE Workflows

PATH=$TIC_PATH/bin/:$TIC_PATH/workflows:$PATH

# Final TIC Python Setup

PYTHONDONTWRITEBYTECODE=1

#umask 0002 # u=rwx,g=rwx,o=rx
umask 0007 # u=rwx,g=rwx,o=


 

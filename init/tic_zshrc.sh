#!/usr/bin/env bash

# TIC Environment Setup ======================================

# Users must define their TIC_PATH in the .zshrc file. 

if [ ! -d $TIC_PATH ]; then

    echo
    echo "$TIC_PATH does not exist. Please edit your .zshrc or .bashrc file accordingly."
    echo
    sleep 10

fi

source $TIC_PATH/init/tic_environment.sh
source $TIC_PATH/init/tic_aliases.sh
source $TIC_STUDIES_PATH/active/aliases.sh
# source $HOME/.tic/tic_default_study.sh
# umask 0002 # u=rwx,g=rwx,o=rx
umask 0007 # u=rwx,g=rwx,o=


 

#!/bin/bash

#
# Script to clean_bids directory.
#
# This is a simple pass through script and will run whatever script the ACTIVE_CLEAN_BIDS environment variable
# points to.

echo
echo
echo 'active study = ' $ACTIVE_STUDY
echo 'bids path    = ' $ACTIVE_BIDS_PATH
echo 'clean_bids   = ' $ACTIVE_CLEAN_BIDS
echo
echo 'parameters   = ' $@
echo
echo

$ACTIVE_CLEAN_BIDS $@

create_acrostic_list.py


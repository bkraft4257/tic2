#!/bin/bash

#
# Script to clean_bids directory.
#
# This is a simple pass through script and will run whatever script the ACTIVE_CLEAN_BIDS environment variable
# points to.


$ACTIVE_CLEAN_BIDS $@


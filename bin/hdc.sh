#!/bin/bash


ACTIVE_APP_OUTPUT_PATH=$ACTIVE_BIDS_PATH

echo
echo 'active study           = ' $ACTIVE_STUDY
echo 'bids path              = ' $ACTIVE_BIDS_PATH
echo

/cenc/software/heudiconv/python/heudiconv/bin/heudiconv \
          -c dcm2niix \
          -b --minmeta \
          -f $ACTIVE_HEUDICONV_PROTOCOL \
          -o $ACTIVE_BIDS_PATH \
          -d "{subject}/2*/*/*.DCM" \
          $@


#!/usr/bin/env bash

echo
echo 'active study = ' $ACTIVE_STUDY
echo 'bids path    = ' $ACTIVE_BIDS_PATH
echo 'protocol     = ' $ACTIVE_HEUDICONV_PROTOCOL
echo 'pattern      = ' $ACTIVE_HEUDICONV_PATTERN
echo
echo 'parameters   = ' $@
echo

if [ $# -eq 0 ]
  then
    echo
    echo "No arguments supplied for heudiconv. Displaying heudiconv help."
    echo

    heudiconv -h | more


else

    echo
    echo "Running heudiconv for DICOM to NIFTI conversion"
    echo

    cmd="heudiconv \
            -f $ACTIVE_HEUDICONV_PROTOCOL                 \
            -c dcm2niix                                   \
            -b                                            \
            --minmeta                                     \
            -o $ACTIVE_BIDS_PATH                          \
            -d $ACTIVE_HEUDICONV_PATTERN                  \
            $@"
           
    echo
    echo $cmd
    echo

    $cmd

fi
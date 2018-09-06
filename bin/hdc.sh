#!/usr/bin/env bash

echo
echo 'active study = ' $ACTIVE_STUDY
echo 'bids path    = ' $ACTIVE_BIDS_PATH
echo 'protocol     = ' $ACTIVE_HEUDICONV_PROTOCOL
echo 'pattern      = ' $ACTIVE_HEUDICONV_PATTERN
echo
echo 'parameters   = ' $@
echo

if [ $# -ne 4 ]; then
    echo
    echo "Usage: hdc.sh -s <participantID> -ss <sessionNum>"
    echo
    exit 1
fi


    echo
    echo "Running heudiconv for DICOM to NIFTI conversion"
    echo

    cmd="singularity run                           \
            -w                                     \
            -B $ACTIVE_SINGULARITY_USER_BIND_PATHS \
            $HDC_SINGULARITY_IMAGE                 \
            -c dcm2niix                            \
            -b                                     \
            --minmeta                              \
            -f $ACTIVE_HEUDICONV_PROTOCOL          \
            -o $ACTIVE_BIDS_PATH                   \
            -d $ACTIVE_HEUDICONV_PATTERN           \
            $@"

    echo
    echo $cmd
    echo

    $cmd



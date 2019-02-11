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

# CAHTMP:
ACTIVE_HEUDICONV_PROTOCOL="/data/CENC_protocol.py"
ACTIVE_BIDS_PATH="/cenclocal/new2018/cenc/bids"
ACTIVE_HEUDICONV_PATTERN={subject}/2*/MR0001/*.DCM

    echo
  echo "Running heudiconv for DICOM to NIFTI conversion"
    echo


    cmd="docker run      \
           --rm          \
           -it           \
           -v $PWD:/data \
                         \
           nipy/heudiconv \
            -f $ACTIVE_HEUDICONV_PROTOCOL \
            -c dcm2niix                   \
            -b                            \
            --minmeta                     \
            -o $ACTIVE_BIDS_PATH          \
            -d /data/$ACTIVE_HEUDICONV_PATTERN  \
            $@"

    echo
    echo $cmd
    echo

    $cmd

fi
           
# docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
# Options:
# --rm : automatically remove the container when it exits
# -it : ???
# -v <local dir>:<mount point inside container>: bind mount a volume

# heudiconv 
#  -d: filespec for dicom images
#  -s: list of subjects
#  -f: heuristics file
#  -c: command for conversion
#  -o: where to put the output


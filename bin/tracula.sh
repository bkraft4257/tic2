#!/usr/bin/env bash

myos=`uname`

echo "myos"
echo $myos

if [ `uname` = "Darwin" ]; then
    echo "tracula.sh will not run on mac (no singularity command)"
    exit

if [ $# -ne 4 ]; then
    echo
    echo "Usage: tracula.sh -s <participantID> -ss <sesnum>"
    echo
    exit 1
fi

BIDS_APP=tracula

ACTIVE_APP_OUTPUT_PATH=$ACTIVE_IMAGE_PROCESSING_PATH/tracula
APP_SINGULARITY_IMAGE=$TRACULA_SINGULARITY_IMAGE
FREESURFER_DATA_DIR=$ACTIVE_IMAGE_PROCESSING_PATH/freesurfer
ACTIVE_APP_WORKING_PATH=$ACTIVE_IMAGE_PROCESSING_PATH/_working

if [ $# -eq 0 ]
  then
    echo "No arguments supplied, displaying help."
    /usr/local/bin/singularity run $APP_SINGULARITY_IMAGE -h
    exit
fi

# Convert to lower case
study_prefix=$(echo "${ACTIVE_STUDY,,}")

# mriqc.sh and fmriprep.sh uses --participant-label and hdc.sh uses -s to indicated the subject acrostic.
# I am using sed as a hack to replace -s with --participant-label.  This allows people to use the shorter
# -s.
#

parameters=$(echo $@ | sed -e 's/-s /--participant_label /')

parameters=$(echo $parameters | sed -e 's/-ss /--session_label /')

# tracula wants the freesurfer license
parameters=$parameters" --license_key /opt/freesurfer/license.txt"

# create the output and work directories parallel to BIDS hierarchy, not inside it

datetime_stamp=`date '+d%Y%m%d_%H%M%S'`
log_file=${ACTIVE_IMAGE_PROCESSING_LOG_PATH}/${study_prefix}_${BIDS_APP}_${datetime_stamp}.log


# NOTE: any -B mount points must exist in the container
#       run "sudo singularity shell -s xx.img"  and create the mount points

# https://askubuntu.com/questions/625224/how-to-redirect-stderr-to-a-file
# Redirect stdout to one file and stderr to another file:
#  command > out 2>error
#
# Redirect stderr to stdout (&1), and then redirect stdout to a file:
# command >out 2>&1
#
# Redirect both to a file:
# command &> out

# Write information to log file
source $TIC_PATH/studies/active/scripts/bids_app_status.sh

echo  $SINGULARITY_COMMAND \
           $ACTIVE_SINGULARITY_USER_BIND_PATHS \
           $APP_SINGULARITY_IMAGE \
           $ACTIVE_BIDS_PATH \
           $ACTIVE_APP_OUTPUT_PATH \
           participant \
           --license_key $FREESURFER_HOME/.license \
           --freesurfer_dir $FREESURFER_DATA_DIR \
           $parameters 

# Run BIDS App

nohup time $SINGULARITY_COMMAND  \
           $ACTIVE_SINGULARITY_USER_BIND_PATHS \
           $APP_SINGULARITY_IMAGE \
           $ACTIVE_BIDS_PATH \
           $ACTIVE_APP_OUTPUT_PATH \
           participant \
           --license_key $FREESURFER_HOME/.license \
           --freesurfer_dir $FREESURFER_DATA_DIR \
           $parameters >> $log_file 2>&1 &

echo "Waiting 30 seconds before displaying the log file ..."
sleep 10

cat $log_file


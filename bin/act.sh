#!/bin/bash

ACTIVE_ACT_OUTPUT_PATH=$ACTIVE_IMAGE_PROCESSING_PATH/act

echo
echo 'active study = ' $ACTIVE_STUDY
echo 'bids path    = ' $ACTIVE_BIDS_PATH
echo 'log path     = ' $ACTIVE_IMAGE_PROCESSING_LOG_PATH
echo 'output path  = ' $ACTIVE_ACT_OUTPUT_PATH
echo

# Convert to lower case
study_prefix=$(echo "${ACTIVE_STUDY,,}")

# create the output and work directories parallel to BIDS hierarchy, not inside it

datetime_stamp=`date '+d%Y%m%d_%H:%M:%S'`
log_file=${ACTIVE_IMAGE_PROCESSING_LOG_PATH}/${study_prefix}.${datetime_stamp}.log

echo
echo $log_file
echo

# NOTE: any -B mount points must exist in the container
#       run "sudo singularity shell -s xx.img"  and create the mount points

$ANTS_CORTICAL_THICKNESS_SINGULARITY_IMAGE='/cenc/software/bids_apps/antsCorticalThickness/bids_antscorticalthickness-2017-10-14-95aa110c26f8.img'

echo 'singularity command  = ' $SINGULARITY_COMMAND
echo 'act command          = ' $ANTS_CORTICAL_THICKNESS_SINGULARITY_IMAGE


# https://askubuntu.com/questions/625224/how-to-redirect-stderr-to-a-file
# Redirect stdout to one file and stderr to another file:
#  command > out 2>error
#
# Redirect stderr to stdout (&1), and then redirect stdout to a file:
# command >out 2>&1
#
# Redirect both to a file:
# command &> out


# run it in the background so that it continues if user logs out
nohup time $SINGULARITY_COMMAND \
           $ANTS_CORTICAL_THICKNESS_SINGULARITY_IMAGE \
           $ACTIVE_BIDS_PATH \
           $ACTIVE_ACT_OUTPUT_PATH \
           participant  ${@} &> $log_file &







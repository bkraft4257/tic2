#!/bin/bash


ANTS_CORTICAL_THICKNESS_SINGULARITY_IMAGE='/cenc/software/bids_apps/antsCorticalThickness/bids_antscorticalthickness-2017-10-14-95aa110c26f8.img'

BIDS_APP=ants_cortical_thickness

ACTIVE_APP_OUTPUT_PATH=$ACTIVE_IMAGE_PROCESSING_PATH/act
APP_SINGULARITY_IMAGE=$ANTS_CORTICAL_THICKNESS_SINGULARITY_IMAGE
ACTIVE_APP_WORKING_PATH=$ACTIVE_APP_OUTPUT_PATH/_working

# Convert to lower case
study_prefix=$(echo "${ACTIVE_STUDY,,}")

# create the output and work directories parallel to BIDS hierarchy, not inside it

datetime_stamp=`date '+d%Y%m%d_%H:%M:%S'`
log_file=${ACTIVE_IMAGE_PROCESSING_LOG_PATH}/${study_prefix}_${BIDS_APP}_${datetime_stamp}.log

source ${TIC_PATH}/studies/active/scripts/bids_app_status.sh


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


# run it in the background so that it continues if user logs out
cmd="act_full_command=$SINGULARITY_COMMAND \
     $ANTS_CORTICAL_THICKNESS_SINGULARITY_IMAGE \
                 $ACTIVE_BIDS_PATH \
                 $ACTIVE_ACT_OUTPUT_PATH \
                 participant ${@}"

echo
echo $cmd > $log_file
echo

#nohup time /usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 \

nohup time $SINGULARITY_COMMAND \
           $APP_SINGULARITY_IMAGE \
           $ACTIVE_BIDS_PATH \
           $ACTIVE_APP_OUTPUT_PATH \
           participant ${@} > $log_file 2>&1 &








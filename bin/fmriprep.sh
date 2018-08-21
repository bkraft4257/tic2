#!/bin/env bash


BIDS_APP=fmriprep

ACTIVE_APP_OUTPUT_PATH=$ACTIVE_IMAGE_PROCESSING_PATH
APP_SINGULARITY_IMAGE=$FMRIPREP_SINGULARITY_IMAGE

ACTIVE_APP_WORKING_PATH=$ACTIVE_APP_OUTPUT_PATH/_working

# Convert to lower case
study_prefix=$(echo "${ACTIVE_STUDY,,}")

# mriqc.sh and fmriprep.sh uses --participant-label and hdc.sh uses -s to indicated the subject acrostic.
# I am using sed as a hack to replace -s with --participant-label.  This allows people to use the shorter
# -s.
#

parameters=$(echo $@ | sed -e 's/-s /--participant-label /')

# create the output and work directories parallel to BIDS hierarchy, not inside it

datetime_stamp=`date '+d%Y%m%d_%H%M%S'`
log_file=${ACTIVE_IMAGE_PROCESSING_LOG_PATH}/${study_prefix}_${BIDS_APP}_${datetime_stamp}.log


# run it in the background so that it continues if user logs out
export FULL_BIDS_APP_COMMAND="nohup time /usr/local/bin/singularity run -w -B $ACTIVE_SINGULARITY_USER_BIND_PATHS \
  $APP_SINGULARITY_IMAGE \
  $ACTIVE_BIDS_PATH \
  $ACTIVE_APP_OUTPUT_PATH \
  --work-dir $ACTIVE_APP_WORKING_PATH \
  participant ${parameters} >> $log_file 2>&1 &"

# Write information to log file
source $TIC_PATH/studies/active/scripts/bids_app_status.sh


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

nohup time /usr/local/bin/singularity run -w -B $ACTIVE_SINGULARITY_USER_BIND_PATHS \
                 $APP_SINGULARITY_IMAGE \
                 $ACTIVE_BIDS_PATH \
                 $ACTIVE_APP_OUTPUT_PATH \
                 --work-dir $ACTIVE_APP_WORKING_PATH \
                 participant ${parameters} >> $log_file 2>&1 &

echo "Waiting 30 seconds before displaying the log file ..."
sleep 30

cat $log_file

echo

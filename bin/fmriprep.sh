#!/usr/bin/env bash


ACTIVE_APP_OUTPUT_PATH=$ACTIVE_MRIQC_PATH
APP_SINGULARITY_IMAGE=$FMRIPREP_SINGULARITY_IMAGE
BIDS_APP=fmriprep

# Convert to lower case
study_prefix=$(echo "${ACTIVE_STUDY,,}")

# create the output and work directories parallel to BIDS hierarchy, not inside it

datetime_stamp=`date '+d%Y%m%d_%H:%M:%S'`
log_file=${ACTIVE_IMAGE_PROCESSING_LOG_PATH}/${study_prefix}_${BIDS_APP}_${datetime_stamp}.log

echo
echo 'active study           = ' $ACTIVE_STUDY
echo 'bids app               = ' $BIDS_APP
echo 'bids path              = ' $ACTIVE_BIDS_PATH
echo 'log path               = ' $ACTIVE_IMAGE_PROCESSING_LOG_PATH
echo 'output path            = ' $ACTIVE_APP_OUTPUT_PATH
echo 'app singularity image  = ' $APP_SINGULARITY_IMAGE
echo 'log file               = ' $log_file
echo

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


nohup time /usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 \
                 $APP_SINGULARITY_IMAGE \
                 $ACTIVE_BIDS_PATH \
                 $ACTIVE_APP_OUTPUT_PATH \
                 participant ${@} > $log_file 2>&1 &
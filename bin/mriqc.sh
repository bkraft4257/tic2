#!/bin/bash

BIDS_APP='mriqc'
ACTIVE_APP_WORKING_PATH=$ACTIVE_MRIQC_PATH/_working
ACTIVE_IMAGE_PROCESSING_LOG_PATH=$ACTIVE_MRIQC_PATH/logs
ACTIVE_APP_OUTPUT_PATH=$ACTIVE_MRIQC_PATH
APP_SINGULARITY_IMAGE=$MRIQC_SINGULARITY_IMAGE

# Convert to lower case
app=mriqc
study_prefix=$(echo "${ACTIVE_STUDY,,}")

# mriqc.sh and fmriprep.sh uses --participant-label and hdc.sh uses -s to indicated the subject acrostic.
# I am using sed as a hack to replace -s with --participant-label.  This allows people to use the shorter
# -s.
#

parameters=$(echo $@ | sed -e 's/-s /--participant-label /')

other_parameters=' --no-sub '

# create the output and work directories parallel to BIDS hierarchy, not inside it

datetime_stamp=`date '+d%Y%m%d_%H:%M:%S'`
log_file=${ACTIVE_IMAGE_PROCESSING_LOG_PATH}/${study_prefix}_${BIDS_APP}_${datetime_stamp}.log

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


# run it in the background so that it continues if user logs out
# I was having problems with running the command from a variable. I am not certain why.
# As an intermediate step i save the file to a variable and then run the variable. This
# is why I don't use the $SINGULARITY_COMMAND in when running the BIDS_APP
#

#full_command=$SINGULARITY_COMMAND \
#                 $APP_SINGULARITY_IMAGE \
#                 $ACTIVE_BIDS_PATH \
#                 $ACTIVE_APP_OUTPUT_PATH \
#                  --work-dir $ACTIVE_APP_WORKING_PATH \
#                 participant ${@} >> $log_file 2>&1 &

/usr/local/bin/singularity run -w -B $ACTIVE_SINGULARITY_USER_BIND_PATHS \
                 $APP_SINGULARITY_IMAGE \
                 $ACTIVE_BIDS_PATH \
                 $ACTIVE_APP_OUTPUT_PATH \
                 --work-dir $ACTIVE_APP_WORKING_PATH \
                 participant $other_parameters  $parameters >> $log_file 2>&1 &


echo "Waiting 30 seconds before displaying the log file ..."
sleep 30

cat $log_file

echo





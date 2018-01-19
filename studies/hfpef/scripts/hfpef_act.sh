#!/bin/bash

BIDSDIR=$HFPEF_BIDS_PATH
OUTPUTDIR=$HFPEF_IMAGE_PROCESSING_PATH/act
OUTPUTDIR=$HFPEF_IMAGE_PROCESSING_PATH/act

echo
echo $BIDSDIR
echo $OUTPUTDIR
echo

study_prefix='hfpef'

# create the output and work directories parallel to BIDS hierarchy, not inside it

LOGDIR=$HFPEF_IMAGE_PROCESSING_PATH/_working/logs

datetime_stamp=`date '+d%Y%m%d_%H:%M:%S'`
log_file=${LOGDIR}/act.${datetime_stamp}.log
echo $log_file

# NOTE: any -B mount points must exist in the container
#       run "sudo singularity shell -s xx.img"  and create the mount points

singularity_command='/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1'
act_use='/cenc/software/bids_apps/antsCorticalThickness/bids_antscorticalthickness-2017-10-14-95aa110c26f8.img'

echo $singularity_command
echo $act_use

# run it in the background so that it continues if user logs out
nohup time $singularity_command $act_use $BIDSDIR $OUTPUTDIR participant  ${@} &> $log_file &







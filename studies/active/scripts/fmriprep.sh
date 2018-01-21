#!/bin/bash

BIDSDIR=$HFPEF_BIDS_PATH
OUTPUTDIR=$HFPEF_IMAGE_PROCESSING_PATH

fmriprep_v1=/cenc/software/fmriprep/poldracklab_fmriprep_latest-2017-08-28-8f9c2862d74f.img 
fmriprep_v2=/cenc/software/fmriprep/poldracklab_fmriprep_latest-2017-11-10-9ae650872d1e.img
fmriprep_use=$fmriprep_v2

study_prefix='hfpef'

if [[ $# -lt 1 ]]; then
   echo "Usage: ${study_prefix}_fmriprep_2.sh <subject_value,hfs070> <other options> ..."
   echo "You may enter more than one subject at a time."
   exit 0
fi


# verify the data directory exists
if  [ ! -d "$BIDSDIR" ]; then
    echo "Data directory does not exist - aborting."
    exit 0
fi

# verify it is read/writeable
if [ ! -r "$BIDSDIR" ] ||  [ ! -x "$BIDSDIR" ]; then
    echo "Data directory not read/writeable - aborting."
    exit 0
fi

# create the output and work directories parallel to BIDS hierarchy, not inside it

WORKDIR=$OUTPUTDIR/fmriprep_working
LOGDIR=$OUTPUTDIR/fmriprep_logs

fmriprep_datetime_stamp=`date '+d%Y%m%d_%H:%M:%S'`
fmriprep_log_file=$LOGDIR/${study_prefix}_fmriprep.$fmriprep_datetime_stamp.output.log

echo " "
echo "${study_prefix}_fmriprep.sh $BIDSDIR $OUTPUTDIR -w $WORKDIR participant --write-graph --participant_label ${@} "
echo " "
echo "Log file is $fmriprep_log_file"
echo " "
echo '[If you need to stop the processing, run "killall fmriprep"]'
echo " "

# NOTE: any -B mount points must exist in the container
#       run "sudo singularity shell -s xx.img"  and create the mount points

# run it in the background so that it continues if user logs out
nohup time /usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 $fmriprep_use $BIDSDIR $OUTPUTDIR \
         -w $WORKDIR participant --write-graph ${@} &> $fmriprep_log_file &




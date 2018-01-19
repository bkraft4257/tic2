#!/bin/bash

if [[ $# -lt 1 ]]; then
   echo "Usage: fmriprep_hfpef.sh <subject_value,hfs070> ..."
   echo "You may enter more than one subject at a time."
   exit 0
fi

# get the full path to the BIDS data directory
BIDSDIR=$HFPEF_BIDS_PATH
echo $BIDSDIR


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
OUTPUTDIR=$HFPEF_IMAGE_PROCESSING_PATH
WORKDIR=$OUTPUTDIR/fmriprep_working
LOGDIR=$OUTPUTDIR/fmriprep_logs

echo " "
echo "fmriprep_hfpef.sh $BIDSDIR $OUTPUTDIR -w $WORKDIR participant --participant_label $PART --write-graph ${@:2} "
echo " "
echo '[If you need to stop the processing, run "killall fmriprep"]'
echo " "

# NOTE: any -B mount points must exist in the container
#       run "sudo singularity shell -s xx.img"  and create the mount points

fmriprep_use=/cenc/software/fmriprep/poldracklab_fmriprep_latest-2017-08-28-ead41c0ca50e.img
fmriprep_datetime_stamp=`date '+d%Y%m%d_%H:%M'`
fmriprep_log_file=$FMRIPREP_LOGDIR/inf_fmriprep.$fmriprep_datetime_stamp.output.log

# run it in the background so that it continues if user logs out
nohup time /usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 $fmriprep_use $BIDSDIR $OUTPUTDIR \
         -w $WORKDIR participant --write-graph --participant_label ${@} &> $fmriprep_log_file &




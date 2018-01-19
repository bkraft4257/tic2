#!/bin/bash

if [[ $# -lt 1 ]]; then
   echo "Usage: inf_mriqc.sh <participant, sub-inf0117>"
   exit 0
fi

BIDSDIR=$SYNERGY_BIDS_PATH
MRIQC_OUTPUT_DIR=$SYNERGY_MRIQC_PATH



PARTICIPANTS="$@"

# verify the data directory exists
if  [ ! -d "$BIDSDIR" ]; then
    echo "BIDS data directory $BIDSDIR does not exist - aborting."
    exit 0
fi

# verify it is read/writeable
if [ ! -r "$BIDSDIR" ] ||  [ ! -x "$BIDSDIR" ]; then
    echo "Data directory not read/writeable - aborting."
    exit 0
fi

# verify the data directory exists
if  [ ! -d "$MRIQC_OUTPUT_DIR" ]; then
    echo "Data directory does not exist - aborting."
    exit 0
fi

# verify it is read/writeable
if [ ! -r "$MRIQC_OUTPUT_DIR" ] ||  [ ! -x "$MRIQC_OUTPUT_DIR" ]; then
    echo "Data directory not read/writeable - aborting."
    exit 0
fi



# create the output and work directories parallel to BIDS hierarchy, not inside it
MRIQC_WORKDIR=$MRIQC_OUTPUT_DIR/working
MRIQC_LOGDIR=$MRIQC_OUTPUT_DIR/logs

echo " "
echo "inf_mriqc.sh <participant, sub-inf0117> "
echo '[If you need to stop the processing, run "killall mriqc"]'
echo " "

# NOTE: any -B mount points must exist in the container
#       run "sudo singularity shell -s xx.img"  and create the mount points

# run it in the background so that it continues if user logs out

mriqc_use=/cenc/software/mriqc/poldracklab_mriqc_latest-2017-08-30-f54388a6fb57.img 
mriqc_datetime_stamp=`date '+d%Y%m%d_%H:%M'`
mriqc_log_file=$MRIQC_LOGDIR/inf_mriqc.$mriqc_datetime_stamp.output.log

echo "running mriqc on $ii: output log is in $mriqc_log_file"

nohup time /usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 \
$mriqc_use $BIDSDIR $MRIQC_OUTPUT_DIR \
--no-sub -w $MRIQC_WORKDIR participant --participant_label $PARTICIPANTS &> $mriqc_log_file &

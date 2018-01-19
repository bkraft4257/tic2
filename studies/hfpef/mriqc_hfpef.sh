#!/bin/bash

if [[ $# -lt 1 ]]; then
   echo "Usage: mriqc_hfpef.sh <participant>"
   exit 0
fi

# get the full path to the BIDS data directory
BIDSDIR=/gandg/hfpef/bids  #"$(readlink -e "$1")"

# get the full path to the BIDS data directory
MRIQC_OUTPUT_DIR=/gandg/hfpef/mriqc  #"$(readlink -e "$1")"

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
echo "mriqc_hfpef.sh $PARTICIPANTS "
echo '[If you need to stop the processing, run "killall mriqc"]'
echo " "

# NOTE: any -B mount points must exist in the container
#       run "sudo singularity shell -s xx.img"  and create the mount points

# run it in the background so that it continues if user logs out


for ii in ${PARTICIPANTS}; do
    echo "running mriqc on $ii: output log is in ${MRIQC_LOG_DIR}.output.log"
    nohup time /usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 /cenc/software/mriqc/poldracklab_mriqc_latest-2017-08-30-f54388a6fb57.img $BIDSDIR $MRIQC_OUTPUT_DIR \
        -w $MRIQC_WORKDIR participant --participant_label $ii &> $MRIQC_LOGDIR/mriqc_hfpef.$ii.output.log &
done

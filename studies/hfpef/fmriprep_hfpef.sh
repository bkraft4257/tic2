#!/bin/bash

if [[ $# -lt 1 ]]; then
   echo "Usage: fmriprep_hfpef.sh <subject_value,hfs070> ..."
   echo "You may enter more than one subject at a time."
   exit 0
fi

# get the full path to the BIDS data directory
BIDSDIR=/gandg/hfpef/bids  #"$(readlink -e "$1")"
echo $BIDSDIR

PARTICIPANT="$1"

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
PARENT="$(dirname "$BIDSDIR")"
OUTPUTDIR=$PARENT/image_processing/
WORKDIR=$OUTPUTDIR/fmriprep_working
LOGDIR=$OUTPUTDIR/fmriprep_logs

echo " "
echo "fmriprep_hfpef.sh $BIDSDIR $OUTPUTDIR -w $WORKDIR participant --participant_label $PART --write-graph ${@:2} "
echo " "
echo '[If you need to stop the processing, run "killall fmriprep"]'
echo " "

# NOTE: any -B mount points must exist in the container
#       run "sudo singularity shell -s xx.img"  and create the mount points

# run it in the background so that it continues if user logs out
nohup time /usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 /cenc/software/fmriprep/poldracklab_fmriprep_latest-2017-08-28-ead41c0ca50e.img $BIDSDIR $OUTPUTDIR \
         -w $WORKDIR participant --participant_label $PARTICIPANT --write-graph ${@:2} &> $LOGDIR/fmriprep_hfpef.$PARTICIPANT.output.log &




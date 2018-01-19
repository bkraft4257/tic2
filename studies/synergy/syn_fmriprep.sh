x#!/bin/bash

if [[ $# -lt 1 ]]; then
   echo "Usage: syn_fmriprep <participant,sub-syn020>"
   exit 0
fi

# get the full path to the BIDS data directory
BIDSDIR=/gandg/synergy/bids/   #"$(readlink -e "$1")"
echo $BIDSDIR

PART=$1

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
OUTPUTDIR=$SYNERGY_IMAGE_PROCESSING_PATH
WORKDIR=$OUTPUTDIR/fmriprep_working
LOGDIR=$OUTPUTDIR/fmriprep_logs

echo " "
echo "fmriprep_synergy.sh $BIDSDIR $OUTPUTDIR -w $WORKDIR participant --participant_label $PART --write-graph ${@:2} "
echo " "
echo "running fmriprep: output log is in $BIDSDIR.output.log"
echo " "
echo '[If you need to stop the processing, run "killall fmriprep"]'
echo " "

#http://fmriprep.readthedocs.io/en/stable/installation.html
#
# "Singularity by default exposes all environment variables from the host inside the container. Because of this your host libraries (such as nipype)
#  could be accidentally used instead of the ones inside the container - if they are included in PYTHONPATH. To avoid such situation we recommend
#   unsetting PYTHONPATH in production use. For example:
#
# $ PYTHONPATH="" singularity run ~/poldracklab_fmriprep_latest-2016-12-04-5b74ad9a4c4d.img \
#  /work/04168/asdf/lonestar/ $WORK/lonestar/output \
#    participant \
#  --participant-label 387 --nthreads 16 -w $WORK/lonestar/work \
#  --ants-nthreads 16
#

PYTHONPATH=""

# NOTE: any -B mount points must exist in the container
#       run "sudo singularity shell -s xx.img"  and create the mount points

# run it in the background so that it continues if user logs out
nohup time /usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 /cenc/software/fmriprep/poldracklab_fmriprep_latest-2017-08-28-ead41c0ca50e.img $BIDSDIR $OUTPUTDIR \
-w $WORKDIR participant --participant_label $PART --write-graph ${@:2} &> $LOGDIR/fmriprep_synergy.$PART.output.log &


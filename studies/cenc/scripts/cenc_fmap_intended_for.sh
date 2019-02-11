#!/usr/bin/env bash

# This script finds the functional data sets and inserts the IntendedFor and EchoTimes (for phase difference fieldmaps)
# into the corresponding JSON files in the fmap directory.
#
# This script does not do any error checking.  It MUST be run in the fmap directory.
#

echo
echo

find ../func/ -name "*rest_*bold.nii.gz" | sort | xargs fmap_intended_for.py -i *_acq-resttopup_dir-{ap,pa}*_epi.json --overwrite -v

echo
echo

find ../func/ -name "*pcasl_*bold.nii.gz" | sort | xargs fmap_intended_for.py -i *_acq-pcasltopup_dir-{ap,pa}*_epi.json --overwrite -v

echo
echo

find ../func/ -name "*rest_*bold.nii.gz"       | sort | xargs fmap_intended_for.py -i *_acq-gre_*phasediff.json --overwrite -f -v 

echo
echo

find ../dwi/ -name "*dwi.nii.gz"       | sort | xargs fmap_intended_for.py -i *_acq-dwitopup_dir-{ap,pa}_*epi.json --overwrite -v

echo
echo

find ../dki/ -name "*dki.nii.gz"       | sort | xargs fmap_intended_for.py -i *_acq-dkitopup_dir-{ap,pa}_*epi.json --overwrite -v

echo
echo

grep -i \"PhaseEncodingDirection\" *.json

echo
echo

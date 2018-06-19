#!/usr/bin/env bash

# This script finds the functional data sets and inserts the IntendedFor and EchoTimes (for phase difference fieldmaps)
# into the corresponding JSON files in the fmap directory.
#
# This script does not do any error checking.  It MUST be run in the fmap directory.
#

echo
echo

find ../func/ -name "*post*topup*.nii.gz" | sort | xargs fmap_intended_for.py -i *_acq-postEpi_dir-{ap,pa}_epi.json --overwrite -v

echo
echo

find ../func/ -name "*pre*topup*.nii.gz"  | sort | xargs fmap_intended_for.py -i *_acq-preEpi_dir-{ap,pa}_epi.json --overwrite -v

echo
echo

find ../func/ -name "*fmap*.nii.gz"       | sort | xargs fmap_intended_for.py -i *_acq-pre_phasediff.json --overwrite -v -f

echo
echo
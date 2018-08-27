#!/usr/bin/env bash

# This script finds the functional data sets and inserts the IntendedFor and EchoTimes (for phase difference fieldmaps)
# into the corresponding JSON files in the fmap directory.
#
# This script does not do any error checking.  It MUST be run in the fmap directory.
#
#                                        json_file                                              intended_for_filename  exists
# 0   sub-imove1101_ses-1_acq-epse_dir-ap_epi.json  /func/sub-imove1101_ses-1_task-rest_acq-epi_rec-topup_bold.nii.gz    True
# 1   sub-imove1101_ses-1_acq-epse_dir-pa_epi.json  /func/sub-imove1101_ses-1_task-rest_acq-epi_rec-topup_bold.nii.gz    True
# 2  sub-imove1101_ses-1_acq-mbepi_dir-lr_epi.json          /func/sub-imove1101_ses-1_task-rest_acq-mbepi_bold.nii.gz    True
# 3  sub-imove1101_ses-1_acq-mbepi_dir-rl_epi.json          /func/sub-imove1101_ses-1_task-rest_acq-mbepi_bold.nii.gz    True
# 4  sub-imove1101_ses-1_acq-pcasl_dir-lr_epi.json          /func/sub-imove1101_ses-1_task-rest_acq-pcasl_bold.nii.gz    True
# 5  sub-imove1101_ses-1_acq-pcasl_dir-rl_epi.json          /func/sub-imove1101_ses-1_task-rest_acq-pcasl_bold.nii.gz    True

if [[ ! $(basename ${PWD}) == "fmap" ]]; then
    echo
    echo "NOT You must be in the fmap directory to run this script"
    echo
    return

fi

echo
echo

find ../func/ -name "*task-rest_acq-epi_rec-topup_bold.nii.gz" | sort | xargs fmap_intended_for.py -i *_acq-epse_dir-{ap,pa}_epi.json --overwrite -v

echo
echo

find ../func/ -name "*task-rest_acq-mbepi_bold.nii.gz" | sort | xargs fmap_intended_for.py -i *_acq-mbepi_dir-{lr,rl}_epi.json --overwrite -v

echo
echo

find ../func/ -name "*_task-rest_acq-pcasl_bold.nii.gz" | sort | xargs fmap_intended_for.py -i *_acq-pcasl_dir-{lr,rl}_epi.json --overwrite -v

echo
echo

fmap_intended_for_check.py *.json -v

echo
echo


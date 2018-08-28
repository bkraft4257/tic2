#!/usr/bin/env bash

# This script finds the functional data sets and inserts the IntendedFor and EchoTimes (for phase difference fieldmaps)
# into the corresponding JSON files in the fmap directory.
#
# This script does not do any error checking.  It MUST be run in the fmap directory.
#
# sub-hfs075_ses-1_acq-bold_phasediff.json:  "IntendedFor": [ "ses-1/func/sub-hfs075_ses-1_task-rest_acq-epi_rec-fmap_bold.nii.gz" ],
# sub-hfs075_ses-1_acq-epse_dir-ap_epi.json:  "IntendedFor": [ "ses-1/func/sub-hfs075_ses-1_task-rest_acq-epi_rec-topup_bold.nii.gz" ],
# sub-hfs075_ses-1_acq-epse_dir-pa_epi.json:  "IntendedFor": [ "ses-1/func/sub-hfs075_ses-1_task-rest_acq-epi_rec-topup_bold.nii.gz" ],
# sub-hfs075_ses-1_acq-mbepi_dir-lr_epi.json:  "IntendedFor": [ "ses-1/func/sub-hfs075_ses-1_task-rest_acq-mbepi_bold.nii.gz" ],
# sub-hfs075_ses-1_acq-mbepi_dir-rl_epi.json:  "IntendedFor": [ "ses-1/func/sub-hfs075_ses-1_task-rest_acq-mbepi_bold.nii.gz" ],
# sub-hfs075_ses-1_acq-pcasl_dir-lr_epi.json:  "IntendedFor": [ "ses-1/func/sub-hfs075_ses-1_task-rest_acq-pcasl_bold.nii.gz" ],
# sub-hfs075_ses-1_acq-pcasl_dir-rl_epi.json:  "IntendedFor": [ "ses-1/func/sub-hfs075_ses-1_task-rest_acq-pcasl_bold.nii.gz" ],

if [[ ! $(basename ${PWD}) == "fmap" ]]; then
    echo
    echo "NOT You must be in the fmap directory to run this script"
    echo
    return

fi

echo
echo

find ../func/ -name "*task-restmbepi_acq-mbepi_bold.nii.gz" | sort | xargs fmap_intended_for.py -i *_acq-mbepi_dir-{lr,rl}_epi.json --overwrite -v

echo
echo

find ../func/ -name "*task-restpcasl_acq-pcasl_bold.nii.gz" | sort | xargs fmap_intended_for.py -i *_acq-pcasl_dir-{lr,rl}_epi.json --overwrite -v

echo
echo

find ../func/ -name "*_task-restepifmap_acq-epi_rec-fmap_bold.nii.gz" | sort | xargs fmap_intended_for.py -i *acq-bold_phasediff.json --overwrite -v -f

echo
echo

find ../func/ -name "*_task-restepitopup_acq-epi_rec-topup_bold.nii.gz" | sort | xargs fmap_intended_for.py -i *_acq-epse_dir-{ap,pa}_epi.json --overwrite -v

echo
echo

fmap_intended_for_check.py *epi.json -v

echo
echo


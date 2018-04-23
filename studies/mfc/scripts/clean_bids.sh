#!/bin/bash

start_dir=$PWD

subject_value=$1
session_value=$2

full_subject_session_value=sub-${subject_value}_ses-${session_value}

session_dir=${ACTIVE_BIDS_PATH}/sub-${subject_value}/ses-${session_value}

echo 
echo "================================================================================="
echo
echo "session_value = " $subject_value 
echo "subject_value = " $session_value
echo
echo "session_dir   = " $session_dir

#--- Remove .1., fmap/*.bval, fmap/*.bvec, fmap/*magnitude1*.json --------------------------------------------
#chmod +w -R ${session_dir}

cd $ACTIVE_BIDS_PATH

find ${session_dir} -name "*.1.*" | xargs rename .1. .
find ${session_dir} -name "*.nii.gz" -or -name "*.json"  | xargs chmod +w

cd ${session_dir}/fmap

# magnitude1 of the phasediff fieldmap does not require a json file according to BIDS. 
# Since the JSON file will be almost identical to phasediff.json file and is not required
# by the BIDS requirements I am removing it. 
rm -rf *magnitude1.json





echo
echo "grep -H IntendedFor *.json"
echo "-------------------------------------------------------------------------------------------------"
grep -H "IntendedFor" *.json
echo

cd ${session_dir}/fmap

# epi topup
pre_topup_ap_json=${full_subject_session_value}_acq-preEpi_dir-ap_bold.json
pre_topup_pa_json=${full_subject_session_value}_acq-preEpi_dir-ap_bold.json

sed -i 's%"AcquisitionMatrixPE": 64,%"IntendedFor": [ "ses-__session_value__/func/sub-__subject_value___ses-__session_value___task-rest_acq-epi_rec-topup_bold.nii.gz" ],\n  "AcquisitionMatrixPE": 64,%' \
     $rest_topup_ap_json

sed -i 's%"AcquisitionMatrixPE": 64,%"IntendedFor": [ "ses-__session_value__/func/sub-__subject_value___ses-__session_value___task-rest_acq-epi_rec-topup_bold.nii.gz" ],\n  "AcquisitionMatrixPE": 64,%' \
     $rest_topup_pa_json


# Replace __session__ with ${session_value} and __subject__ with ${subject_value}.
#  I would prefer to do this in a single call. Unfortunately, I haven't worked out the syntax

sed -i 's#__session_value__#'${session_value}'#g' *.json
sed -i 's#__subject_value__#'${subject_value}'#g' *.json

#--- Reorient all images to match FSL orientation -------------------------------------------------
echo "Reorienting all *.gz files with fslreorient2std"
echo "-----------------------------------------------"

for ii in $(find $session_dir -name "*.gz"); do
    echo "reorienting $ii "
    fslreorient2std $ii $ii
done

#echo 
#echo
#echo "Set permission to read only for *.nii.gz and *.json files"
#echo "--------------------------------------------------------------------------------"
#find $session_dir -type f -name "*.nii.gz" | xargs chmod -w -R 
#find $session_dir -type f -name "*.json"   | xargs chmod -w -R 

#--- Look for repeat scans -----------------------------------------------------------------------
echo
echo
echo "Looking for repeated scans one last time. "
echo "If you see something reported here you must CHOOSE which images you want to use."
echo "--------------------------------------------------------------------------------"
find $session_dir -name "*.[0-9]*"


echo " "

cd $start_dir
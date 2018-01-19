#!/bin/bash

# Example on how to use this script.
#
# 1) Goto $SYNERGY_BIDS_PATH.  Alias created cdsb
# 2) syn_clean_bids.sh  <subject_value> <session_value>

# Contents of anat
#
#    sub-syn020_ses-1_T1w.nii.gz
#
#    sub-syn020_ses-1_acq-3dtof_angio.nii.gz
#    sub-syn020_ses-1_acq-pcbilateral_angio.nii.gz
#    sub-syn020_ses-1_acq-pcleft_angio.nii.gz
#    sub-syn020_ses-1_acq-pcright_angio.nii.gz

# Contents of fmap directory
#
#    sub-syn020_ses-1_acq-topup_dir-ap_epi.nii.gz
#    sub-syn020_ses-1_acq-topup_dir-pa_epi.nii.gz

# Contents of func directory
#
#    sub-syn020_ses-1_task-rest_acq-epi_bold.nii.gz

start_dir=$PWD

subject_value=$1  
session_value=$2

full_subject_session_value=sub-${subject_value}_ses-${session_value}

session_dir=${start_dir}/sub-${subject_value}/ses-${session_value}

echo 
echo "================================================================================="
echo
echo "session_value = " $subject_value 
echo "subject_value = " $session_value
echo
echo "session_dir   = " $session_dir

echo
echo "List images collected and stored as DICOM files"
echo "------------------------------------------------------------------------------------------------"-

hdc_bids_path=$SYNERGY_PATH/bids.heudiconv/${subject_value}/ses-${session_value}/info/

$HDC_PATH/hdc_add_header.py -v ${hdc_bids_path}/dicominfo_ses-${session_value}.tsv \
                            -o ${hdc_bids_path}/dicominfo_ses-${session_value}.csv

echo
echo "List images converted by heudiconv (HDC)"
echo "-------------------------------------------------------------------------------------------------"
echo
cat -n ${hdc_bids_path}/${subject_value}_ses-${session_value}.auto.txt
echo
echo


#--- Remove .1. from filenames and enable write permission --------------------------------------------
find ${session_dir} \( -name "*.gz" -or -name "*.json" \)| xargs chmod +w 

find ${session_dir} -name "*.1.*" | xargs rename .1. .

cd ${session_dir}/fmap

#--- Update JSON files to include IntendedFor information -------------------------------------

rest_topup_ap_json=${full_subject_session_value}_acq-topup_dir-ap_epi.json
rest_topup_pa_json=${full_subject_session_value}_acq-topup_dir-pa_epi.json

if [ -f $rest_topup_ap_json ] 
then         
    sed -i 's%"AcquisitionMatrixPE": 64,%"IntendedFor": [ "ses-__session_value__/func/sub-__subject_value___ses-__session_value___task-rest_acq-epi_bold.nii.gz" ],\n  "AcquisitionMatrixPE": 64,%' \
    $rest_topup_ap_json
else
    echo "rest_topup_ap_json file not found"
fi


if [ -f $rest_topup_pa_json ] 
then
    sed -i 's%"AcquisitionMatrixPE": 64,%"IntendedFor": [ "ses-__session_value__/func/sub-__subject_value___ses-__session_value___task-rest_acq-epi_bold.nii.gz" ],\n  "AcquisitionMatrixPE": 64,%' \
     $rest_topup_pa_json
else
    echo "rest_topup_pa_json file not found"
fi


# Replace __session__ with ${session_value} and __subject__ with ${subject_value}.
#  I would prefer to do this in a single call. Unfortunately, I haven't worked out the syntax

sed -i 's#__session_value__#'${session_value}'#g' *.json
sed -i 's#__subject_value__#'${subject_value}'#g' *.json


# This awk script removed the second IntendedFor if script is run multiple times. This is a complete hack
# but it works

for ii in *.json; do
    echo $ii
    awk '/IntendedFor/&&c++>0 {next} 1' $ii > tmp.$ii
    mv -f tmp.$ii $ii
done



echo
echo "grep -H IntendedFor *.json"
echo "-------------------------------------------------------------------------------------------------"
grep -H "IntendedFor" *.json
echo

cd $start_dir 

#--- Reorient all images to match FSL orientation -------------------------------------------------
echo "Reorienting all *.gz files with fslreorient2std"
echo "-----------------------------------------------"

for ii in $(find $session_dir -name "*.gz"); do
    echo "reorienting $ii "
    fslreorient2std $ii $ii
done

# Clean up any backup files.   These shouldn't exist unless the user inspected JSON files with a text
# editor.  Since I do this often I thought it would be helpful to remove them here

find $session_dir -name "*~" -delete

#--- Remove write permission --------------------------------------------
find ${session_dir} \( -name "*.gz" -or -name "*.json" \)| xargs chmod -w 

#--- Look for scan counter.  These should be removed by now.  If there are repeat scans (i.e. <1)
#    then user will need to decide which scans to use.
echo
echo
echo "Looking for repeated scans one last time. "
echo "If you see something reported here you must CHOOSE which images you want to use."
echo "--------------------------------------------------------------------------------"
find $session_dir -name "*.[0-9]*"



echo " "

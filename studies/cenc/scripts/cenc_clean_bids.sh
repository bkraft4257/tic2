#!/bin/bash

# Contents of func directory
#
#    uses topup ...
#    sub-34P1992_ses-1_task-rest_bold.1.nii.gz
#    sub-34P1992_ses-1_task-rest_acq-pcasl_bold.nii.gz
#
# Contents of fmap directory
#
#    sub-34P1992_ses-1_acq-pcasltopup_dir-ap_epi.1.nii.gz
#    sub-34P1992_ses-1_acq-pcasltopup_dir-pa_epi.1.nii.gz
#    sub-34P1992_ses-1_acq-resttopup_dir-ap.1.nii.gz
#    sub-34P1992_ses-1_acq-resttopup_dir-pa.1.nii.gz

start_dir=$PWD

subject_value=$1
session_value=$2


full_subject_session_value=sub-${subject_value}_ses-${session_value}

session_dir=${CENC_BIDS_PATH}/sub-${subject_value}/ses-${session_value}

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
hdc_bids_path=$CENC_BIDS_PATH/.heudiconv/${subject_value}/ses-${session_value}/info/

$HDC_PATH/hdc_add_header.py -v ${hdc_bids_path}/dicominfo_ses-${session_value}.tsv \
                            -o ${hdc_bids_path}/dicominfo_ses-${session_value}.csv

echo
echo "List images converted by heudiconv (HDC)"
echo "-------------------------------------------------------------------------------------------------"
echo
cat -n ${hdc_bids_path}/${subject_value}_ses-${session_value}.auto.txt
echo
echo


#--- Remove .1., fmap/*.bval, fmap/*.bvec, fmap/*magnitude1*.json --------------------------------------------
#chmod +w -R ${session_dir}

find ${session_dir} -name "*.1.*" | xargs rename .1. .
find ${session_dir} -name "*.nii.gz" | xargs chmod +w
find ${session_dir} -type d | xargs chmod +w


cd $CENC_BIDS_PATH

#--- Reorient all images to match FSL orientation -------------------------------------------------
# echo "Reorienting all *.gz files with fslreorient2std"
#echo "-----------------------------------------------"

for ii in $(find $session_dir -name "*.gz"); do
    echo "reorienting $ii "
    fslreorient2std $ii $ii
done

#echo 
#echo
#echo "Set permission to read only for *.nii.gz and *.json files"
#echo "--------------------------------------------------------------------------------"
find $session_dir -type f -name "*.nii.gz" | xargs chmod -w -R 
find $session_dir -type f -name "*.json"   | xargs chmod -w -R 

#--- Look for repeat scans -----------------------------------------------------------------------
echo
echo
echo "Looking for repeated scans one last time. "
echo "If you see something reported here you must CHOOSE which images you want to use."
echo "--------------------------------------------------------------------------------"
find $session_dir -name "*.[0-9]*"

echo " "

cd $start_dir
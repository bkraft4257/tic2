#!/bin/bash

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

hdc_bids_path=$INFINITE_PATH/bids.heudiconv/${subject_value}/ses-${session_value}/info/

$HDC_PATH/hdc_add_header.py -v ${hdc_bids_path}/dicominfo_ses-${session_value}.tsv \
                            -o ${hdc_bids_path}/dicominfo_ses-${session_value}.csv

echo
echo "List images converted by heudiconv (HDC)"
echo "-------------------------------------------------------------------------------------------------"
echo
cat -n ${hdc_bids_path}/${subject_value}_ses-${session_value}.auto.txt
echo
echo
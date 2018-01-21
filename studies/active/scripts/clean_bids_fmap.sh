#!/bin/bash

start_dir=$PWD

subject_id=$1
session_id=$2

session_dir=${start_dir}/ses-${session_id}

echo 
echo "================================================================================="
echo $subject_id  $session_id

find ${session_dir} -name "*.1.*" | xargs rename .1. .
chmod +w -R ${session_dir}

cd ses-${session_id}/fmap

echo "Copying fmap_mag_t1.nii.gz"

cp /gandg/infinite/imaging_data/individuals/${subject_id}/${session_id}/fmap_bold/fmap_mag_t1.nii.gz sub-${subject_id}_ses-${session_id}_acq-bold_magnitude1.nii.gz
cp /gandg/infinite/imaging_data/individuals/${subject_id}/${session_id}/fmap_asl/fmap_mag_t1.nii.gz sub-${subject_id}_ses-${session_id}_acq-pcasl_magnitude1.nii.gz

chmod +w *

# "IntendedFor": [ "ses-1/func/sub-inf0117_ses-1_task-rest_acq-epi_bold.nii.gz",
#                   "ses-1/func/sub-inf0117_ses-1_task-rest_acq-pcasl_bold.nii.gz",
#                   "ses-1/dwi/sub-inf0117_ses-1_acq-30dir_dwi.nii.gz"
#                 ],

#  "EchoTime1": 0.00492,
#  "EchoTime2": 0.00738,

echo "sed EchoTime"

sed -i 's/"EchoTime": 0.00738,/"EchoTime1": 0.00492,\n  "EchoTime2": 0.00738,/' *.json

echo "sed AcquisitionMatrixPE: 48"

sed -i 's%"AcquisitionMatrixPE": 48,%"IntendedFor": [ "ses-__session_id__/func/sub-__subject_id___ses-__session_id___task-rest_acq-epi_bold.nii.gz" ],\n  "AcquisitionMatrixPE": 48,%' \
     sub-${subject_id}_ses-${session_id}_acq-bold_phasediff.json

echo "sed AcquisitionMatrixPE: 128"
sed -i 's%"AcquisitionMatrixPE": 128,%"IntendedFor": [ "ses-__session_id__/func/sub-__subject_id___ses-__session_id___task-rest_acq-pcasl_bold.nii.gz",\n                    "ses-__session_id__/dwi/sub-__subject_id___ses-__session_id___acq-30dir_dwi.nii.gz" ],\n  "AcquisitionMatrixPE": 128,%' \
     sub-${subject_id}_ses-${session_id}_acq-pcasl_phasediff.json

echo "sed __session__id"
sed -i 's#__session_id__#'${session_id}'#g' *.json

echo "sed __subject__id"
sed -i 's#__subject_id__#'${subject_id}'#g' *.json

cd $start_dir 

echo "fslreorient2std"
find $session_dir -name "*.gz" | xargs -L 1 -I % fslreorient2std % % 

echo "clean tsv and *~"
find $session_dir -path "*func*" -name "*.tsv" -delete
find $session_dir -name "*~" -delete

echo "find *.[0-9]*"
find $session_dir -name "*.[0-9]*"

#chmod -w -R $session_dir

echo

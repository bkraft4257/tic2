#!/bin/bash

if [[ $# -lt 1 ]]; then
   echo "Usage: hfpef_conn.sh <subject_value,hfs070> <session_value,1>"
   echo "You may only enter one subject value and session value at a time."

   exit 0
fi

HFPEF_CONN_PATH=$HFPEF_IMAGE_PROCESSING_PATH/conn

subject_id=${1}
session_id=${2-1}
subject=sub-${subject_id}
session=ses-${session_id}

conn_input=${HFPEF_CONN_PATH}/${subject}/${session}/epi/input

bold_mni_preproc=$HFPEF_FMRIPREP_PATH/${subject}/${session}/func/${subject}_${session}_task-rest_acq-epi_rec-fmap_bold_space-MNI152NLin2009cAsym_preproc.nii.gz

t1w_gm_probtissue=$HFPEF_FMRIPREP_PATH/${subject}/${session}/anat/${subject}_${session}_T1w_class-GM_probtissue.nii.gz
t1w_wm_probtissue=$HFPEF_FMRIPREP_PATH/${subject}/${session}/anat/${subject}_${session}_T1w_class-WM_probtissue.nii.gz
t1w_csf_probtissue=$HFPEF_FMRIPREP_PATH/${subject}/${session}/anat/${subject}_${session}_T1w_class-CSF_probtissue.nii.gz

ln -f ${bold_mni_preproc} ${conn_input}/bold_mni_preproc.nii.gz


ln -f ${t1w_gm_probtissue} ${conn_input}/t1w_gm_probtissue.nii.gz
ln -f ${t1w_wm_probtissue} ${conn_input}/t1w_gm_probtissue.nii.gz
ln -f ${t1w_gm_probtissue} ${conn_input}/t1w_gm_probtissue.nii.gz

cd ${conn_input}
echo 
pwd
echo
ls
echo




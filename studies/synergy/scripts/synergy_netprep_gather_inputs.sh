#!/bin/bash

if [[ $# -lt 1 ]]; then
   echo "Usage: synergy_netprep_gather_inputs.sh <subject_value,syn243> <session_value,1>"
   echo "You must enter one subject value and session value at a time."

   exit 0
fi

subject_id=${1}
session_id=${2-1}
subject=sub-${subject_id}
session=ses-${session_id}

confound_columns=1,2,13,14,15,16,17,18,24,25,26,27,28,29

netprep_input=${SYNERGY_NETPREP_PATH}/${subject}/${session}/input

mkdir -p ${netprep_input}
cp ${SYNERGY_SCRIPTS_PATH}/synergy_netprep.yaml ${netprep_input}/netprep.yaml

bold_mni_preproc=$SYNERGY_FMRIPREP_PATH/${subject}/${session}/func/${subject}_${session}_task-rest_acq-epi_bold_space-MNI152NLin2009cAsym_preproc.nii.gz
t1w_gm_probtissue=$SYNERGY_FMRIPREP_PATH/${subject}/${session}/anat/${subject}_${session}_T1w_class-GM_probtissue.nii.gz
bold_confounds_tsv=$SYNERGY_FMRIPREP_PATH/${subject}/${session}/func/${subject}_${session}_task-rest_acq-epi_bold_confounds.tsv

ln -f ${bold_mni_preproc} ${netprep_input}/bold_mni_preproc.nii.gz
ln -f ${t1w_gm_probtissue} ${netprep_input}/t1w_gm_probtissue.nii.gz

echo
csvcut -t -n ${bold_confounds_tsv}

echo
echo ${confound_name_columns}
echo


csvcut -t -c ${confound_columns} ${bold_confounds_tsv} > ${netprep_input}/bold_confound.csv



cd ${netprep_input}
echo 
pwd
echo
ls
echo



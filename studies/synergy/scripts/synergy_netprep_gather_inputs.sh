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

netprep_input=${SYNERGY_NETPREP_PATH}/${subject}/${session}/input

bold_mni_preproc=$SYNERGY_FMRIPREP_PATH/${subject}/${session}/func/${subject}_${session}_task-rest_acq-epi_bold_space-MNI152NLin2009cAsym_preproc.nii.gz
bold_confounds_tsv=$SYNERGY_FMRIPREP_PATH/${subject}/${session}/func/${subject}_${session}_task-rest_acq-epi_bold_confounds.tsv
t1w_gm_probtissue=$SYNERGY_FMRIPREP_PATH/${subject}/${session}/anat/${subject}_${session}_T1w_class-GM_probtissue.nii.gz

grep_results=$(grep NonSteadyStateOutlier00 $bold_confounds_tsv)

if [[ -z $grep_results ]]; then
    confound_name_columns="WhiteMatter,GlobalSignal,aCompCor00,aCompCor02,aCompCor03,aCompCor04,aCompCor05,X,Y,Z,RotX,RotY,RotZ"
else
    confound_name_columns="WhiteMatter,GlobalSignal,aCompCor00,aCompCor02,aCompCor03,aCompCor04,aCompCor05,X,Y,Z,RotX,RotY,RotZ,NonSteadyStateOutlier00"
fi


mkdir -p ${netprep_input}
cp ${SYNERGY_SCRIPTS_PATH}/synergy_netprep.yaml ${netprep_input}/synergy_netprep.yaml


ln -f ${bold_mni_preproc} ${netprep_input}/bold_mni_preproc.nii.gz
ln -f ${t1w_gm_probtissue} ${netprep_input}/t1w_gm_probtissue.nii.gz

echo
csvcut -t -n ${bold_confounds_tsv}

echo
echo ${confound_name_columns}
echo


csvcut -t -c ${confound_name_columns} ${bold_confounds_tsv} > ${netprep_input}/bold_confound.csv



cd ${netprep_input}
echo
pwd
echo
ls
echo




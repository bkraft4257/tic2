#!/bin/bash

if [[ $# -lt 1 ]]; then
   echo "Usage: inf_netprep_gi.sh <subject_value,inf0238> <session_value,1>"
   echo "You may only enter one subject value and session value at a time."

   exit 0
fi
#subject=${1}
#session=${2-"ses-1"}

#subject_id=$(echo ${subject} | sed 's/^sub-//')
#session_id=$(echo ${session} | sed 's/^ses-//')


subject_id=${1}
session_id=${2-1}

subject='sub-'$subject_id
session='ses-'$session_id

netprep_input=${INFINITE_NETPREP_PATH}/${subject}/${session}/epi/input

bold_mni_preproc=$INFINITE_FMRIPREP_PATH/${subject}/${session}/func/${subject}_${session}_task-rest_acq-epi_bold_space-MNI152NLin2009cAsym_preproc.nii.gz
bold_confounds_tsv=$INFINITE_FMRIPREP_PATH/${subject}/${session}/func/${subject}_${session}_task-rest_acq-epi_bold_confounds.tsv

bold_confounds_csv=${netprep_input}/bold_confounds.csv

t1w_gm_probtissue=$INFINITE_FMRIPREP_PATH/${subject}/anat/${subject}_T1w_space-MNI152NLin2009cAsym_class-GM_probtissue.nii.gz
grep_results=$(grep NonSteadyStateOutlier $bold_confounds_tsv)

if [[ -z $grep_results ]]; then
    confound_name_columns="WhiteMatter,GlobalSignal,aCompCor00,aCompCor02,aCompCor03,aCompCor04,aCompCor05,X,Y,Z,RotX,RotY,RotZ"
else
    echo "Warning NonSteadyStateOutlier(s) found.  Check bold_confound.csv to make sure it is what you want."
    confound_name_columns="WhiteMatter,GlobalSignal,aCompCor00,aCompCor02,aCompCor03,aCompCor04,aCompCor05,X,Y,Z,RotX,RotY,RotZ,NonSteadyStateOutlier00"
fi


mkdir -p ${netprep_input}
cp ${INFINITE_SCRIPTS_PATH}/inf_netprep.yaml ${netprep_input}/inf_netprep.yaml

ln -f ${bold_mni_preproc} ${netprep_input}/bold_mni_preproc.nii.gz
ln -f ${t1w_gm_probtissue} ${netprep_input}/t1w_gm_probtissue.nii.gz

echo

csvcut -t -c ${confound_name_columns} ${bold_confounds_tsv} > ${bold_confounds_csv}

echo
echo
echo "List of confounds in ${bold_confounds_tsv}"
echo

csvcut -t -n ${bold_confounds_tsv}

echo
echo
echo "List of confounds in ${bold_confounds_csv}"
echo
csvcut -n ${bold_confounds_csv}



cd ${netprep_input}
echo 
pwd
echo
ls
echo




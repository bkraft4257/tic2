#!/bin/bash


subject_id=${1-$PWD}
subject_dir=$(readlink -f ${subject_id} )
topup_input=${subject_dir}/diffusion/topup/input
reorient_dir=${subject_dir}/reorient

echo
echo $CENC_MRI_DATA
echo $subject_id
echo $subject_dir
echo $topup_input
echo

mkdir -p ${topup_input}

cd ${topup_input}

#
# Copy files
#

for ii in dki dti; do
    cp ${reorient_dir}/${ii}.nii.gz $topup_input
#
#   Copy files from the reorient directory if they were converted
#   with dcm2nii
#
#    cp ${reorient_dir}/${ii}.bval   $topup_input
     cp ${CENC_PYTHON}/${ii}.bval   $topup_input

    extract_b0.py ${ii}.nii.gz  ${ii}.bval --verbose
done

cp ${CENC_PYTHON}/cenc_topup_acqparams.txt  ${topup_input}/acqparams.txt
cp ${CENC_PYTHON}/cenc_topup_b02b0.cnf      ${topup_input}/b02b0.cnf

#
# Extract directory
#

fslmerge -t b0.nii.gz  b0.dki.nii.gz  b0.dti.nii.gz

fslroi   b0.nii.gz b0.nii.gz 0 -1 0 -1 0 58 0 -1 
rm -rf   b0.dki.nii.gz  b0.dti.nii.gz dki* dti*



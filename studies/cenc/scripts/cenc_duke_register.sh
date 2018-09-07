#!/bin/bash

subject_id=${1}

cenc_id="34P1${subject_id}"
duke_id="34P9${subject_id}"

cenc_subject_dir=${CENC_MRI_DATA}/${cenc_id}
duke_subject_dir=${CENC_MRI_DATA}/${duke_id}

wmlesions_long=${cenc_subject_dir}/structural/wmlesions_long/input
reference_t1w=$wmlesions_long/nu.nii.gz

affine_prefix="duke_a_cenc_"
syn_prefix="duke_s_cenc_"

cenc_t1w=${cenc_subject_dir}/results/native/images/nu.nii.gz


echo $cenc_subject_dir
echo $duke_subject_dir



[ ! -d $wmlesions_long ] | mkdir -p ${wmlesions_long}
cd ${wmlesions_long}

[ ! -f nu.nii.gz ] | cp ${cenc_t1w} $reference_t1w
[ ! -f duke_t1w.nii.gz ] | cp ${duke_subject_dir}/reorient/t1w.nii.gz ${wmlesions_long}/duke_t1w.nii.gz
[ ! -f duke_t2flair.nii.gz ] | cp ${duke_subject_dir}/reorient/t2flair.nii.gz ${wmlesions_long}/duke_t2flair.nii.gz

pwd




##--------------------------------------------------------------------------------------------------
## Affine Transformation
antsRegistrationSyNQuick.sh -d 3 -m duke_t1w.nii.gz -f ${reference_t1w} -t a -o ${affine_prefix}

#rename output from antsRegistrationSyNQuick
mv ${affine_prefix}Warped.nii.gz ${affine_prefix}_duke_t1w.nii.gz
cmd="antsApplyTransforms -d 3 -i duke_t2flair.nii.gz -r ${reference_t1w} -o ${affine_prefix}_duke_t2flair.nii.gz -t ${affine_prefix}0GenericAffine.mat -v"  

echo $cmd 
$cmd

##--------------------------------------------------------------------------------------------------
## Syn Transformation

antsRegistrationSyNQuick.sh -d 3 -m duke_t1w.nii.gz -f ${reference_t1w} -t s -o ${syn_prefix}
#rename output from antsRegistrationSyNQuikc
mv ${syn_prefix}Warped.nii.gz ${syn_prefix}_duke_t1w.nii.gz
cmd="antsApplyTransforms -d 3 -i duke_t2flair.nii.gz -r ${reference_t1w} -o ${syn_prefix}_duke_t2flair.nii.gz -t ${syn_prefix}1Warp.nii.gz -t ${syn_prefix}0GenericAffine.mat -v"

echo $cmd
$cmd
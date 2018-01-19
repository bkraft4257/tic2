#!/bin/bash

T1brain=${1}
fmapPhase=fmap_phase.nii.gz
fmapMag=fmap_mag_brain.nii.gz
fmapRads=fmap_rads.nii.gz

# rm -rf T1_brain.nii.gz
# cp -f ${T1brain} T1_brain.nii.gz

##
#  Down Sample T1 Brain to fmap


dim=3
its=10x10x10
percentage=0.1

antsApplyTransforms \
-d $dim             \
-i ${T1brain}       \
-r ${fmapPhase}     \
-n NearestNeighbor  \
-t identity         \
-o ${fmapMag}


##
#  Prepare Field Map

fsl_prepare_fieldmap SIEMENS ${fmapPhase} ${fmapMag} ${fmapRads} 2.46

##
#

# fslview ${fmapPhase} ${fmapMag} ${fmapRads} 


## Create FEAT FSF template 
#

fmriDir=../../rfmri/

mkdir ${fmriDir}
cp  -f  ${fmapRads} ${fmriDir}
cp  -f  ${fmapMag}  ${fmriDir}
cp  -f  ${T1brain}  ${fmriDir}T1_brain.nii.gz
cp  -f  T1.nii.gz   ${fmriDir}

cd ${fmriDir}
echo $PWD

#rm -rf ${fmriDir}/rfmri.fsf
#sed -e "s#{PWD}#${PWD}#" $IC_GIT_PATH/ic/studies/infinite/infinite_rfmritemplate.fsf > ${fmriDir}/rfmri.fsf





#!/bin/bash

fmapDir=${PWD}/${1}/asl_fmap
linkedDir=${PWD}/${1}/data/linked
antsCtDir=${PWD}/${1}/antsCT

if [ ! -d $fmapDir ];
then
    mkdir ${fmapDir}
fi

cp -f ${linkedDir}/asl_fmap*.gz ${fmapDir}

if [ ! -f ${fmapDir}/asl_fmap_mag.nii.gz ];
then

    antsBet=${antsCtDir}/act_ExtractedBrain0N4.nii.gz
#    cp ${antsBet} ${fmapDir}
    antsApplyTransforms -d 3 -r ${fmapDir}/asl_fmap_phase.nii.gz -i ${antsBet} -o ${fmapDir}/t1_fmap_mag.nii.gz -t identity 
    ln -sf ${fmapDir}/t1_fmap_mag.nii.gz ${fmapDir}/asl_fmap_mag.nii.gz
fi

fmapPhase=${fmapDir}/asl_fmap_phase.nii.gz
fmapMag=${fmapDir}/asl_fmap_mag.nii.gz
fmapRads=${fmapDir}/asl_fmap_rads.nii.gz

# fsl_prepare_fieldmap SIEMENS ${fmapPhase} ${fmapMag} ${fmapRad} 2.46

fsl_prepare_fieldmap SIEMENS ${fmapPhase}  ${fmapMag} ${fmapRads} 2.46 

sed -e "s#<PWD>#${PWD}#"  /gandg/infinite3/infinite/icGit/release/ic/studies/infinite/infinite_bold_template.fsf > ${fmapDir}/bold.fsf




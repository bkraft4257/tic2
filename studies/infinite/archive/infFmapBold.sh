#!/bin/bash

fmapDir=${PWD}/${1}/fmap_${2}
linkedDir=${PWD}/${1}/data/linked
antsCtDir=${PWD}/${1}/antsCT

if [ ! -d $fmapDir ];
then
    mkdir ${fmapDir}
fi

cp -f ${linkedDir}/${2}_fmap*.gz ${fmapDir}
rename ${2}_fmap fmap ${fmapDir}/*.gz

if [ -f ${fmapDir}/fmap_mag.nii.gz ];
then

    bet2 ${fmapDir}/fmap_mag.nii.gz ${fmapDir}/fmap_mag_brain.nii.gz
    ln -sf 

else

    antsBet=${antsCtDir}/act_ExtractedBrain0N4.nii.gz
#    cp ${antsBet} ${fmapDir}
    antsApplyTransforms -d 3 -r ${fmapDir}/fmap_phase.nii.gz -i ${antsBet} -o ${fmapDir}/fmap_mag_t1.nii.gz -t identity 
    ln -sf ${fmapDir}/fmap_mag_t1.nii.gz ${fmapDir}/fmap_mag_brain.nii.gz
fi

fmapPhase=${fmapDir}/fmap_phase.nii.gz
fmapMag=${fmapDir}/fmap_mag_brain.nii.gz
fmapRads=${fmapDir}/fmap_rads.nii.gz

fsl_prepare_fieldmap SIEMENS ${fmapPhase}  ${fmapMag} ${fmapRads} 2.46 

#sed -e "s#<PWD>#${PWD}#"  /gandg/infinite3/infinite/icGit/release/ic/studies/infinite/infinite_bold_template.fsf > ${fmapDir}/bold.fsf

echo
ls -l ${fmapDir}
echo

# freeview ${fmapDir}/fmap_mag_brain.nii.gz fmap_rads.nii.gz &


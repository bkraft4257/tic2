#!/bin/bash
# user to change

ANTS_CT_DIR=${IC_TEMPLATES}/ixi/
OUT_DIR=$PWD/${2}/${1}/

inFile=${PWD}/${1}.nii.gz

echo $ANTS_CT_DIR
echo $OUT_DIR

# ls -l ${ANTS_CT_DIR}brainWithSkullTemplate.nii.gz  

eOption=${ANTS_CT_DIR}T_template2.nii.gz
tOption=${ANTS_CT_DIR}T_template2_BrainCerebellum.nii.gz
mOption=${ANTS_CT_DIR}T_template_BrainCerebellumProbabilityMask.nii.gz  
fOption=${ANTS_CT_DIR}T_template_BrainCerebellumExtractionMask.nii.gz
pOption=${ANTS_CT_DIR}Priors/priors%d.nii.gz


if [ ${2} = "display" ];then
    freeview $eOption $tOption $mOption $fOption ${ANTS_CT_DIR}Priors/priors[1-6].nii.gz &
else
    ${ANTSPATH}antsCorticalThickness.sh -d 3 -a ${inFile} -t ${tOption} -e ${eOption} -m ${mOption} -f ${fOption} -p ${pOption} -o ${OUT_DIR}act_
fi

#antsCorticalThickness.sh -d imageDimension
#                         -a anatomicalImage
#                         -e brainTemplate (not skull stripped)
#                         -t template for t1 registration (same as -e but skull stripped) 
#                         -m brainExtractionProbabilityMask
#                         -p brainSegmentationPriors
#                        <OPTARGS>
#                        -o outputPrefix


# -t: template for t1 registration   Anatomical *intensity* template (assumed to be skull-stripped). 
#             
#   A common use case would be where this would be the same template as specified in the
#                                 -e option which is not skull stripped.
#                      We perform the registration (fixed image = individual subjec#t
#                  and moving image = template) to produce the files.
#
#                 The output from this step is
#
#                   * tmpTemplateToSubject0GenericAffine.mat
#                   * tmpTemplateToSubject1Warp.nii.gz
#                   * tmpTemplateToSubject1InverseWarp.nii.gz
#                   * tmpTemplateToSubjectLogJacobian.nii.gz

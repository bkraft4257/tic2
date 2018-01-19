#!/bin/bash

NAME=`echo "$FILE" | cut -d'.' -f1`

${ANTSPATH}/antsBrainExtraction.sh -d 3 -a ${1} -e ${2}/infiniteGroup_e_T1wFullImage.nii.gz  -m ${2}/infiniteGroup_m_BrainCerebellumProbabilityMask.nii.gz -o $NAME_aBE.nii.gz
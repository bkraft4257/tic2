#!/bin/bash

input_dir=${1-$PWD}

subject_dir=$(readlink -f ${input_dir})

nifti_dir=${subject_dir}/nifti
dicom_dir=${subject_dir}/dicom

echo
echo $input_dir
echo $subject_dir
echo $nifti_dir
echo $dicom_dir
echo


echo
echo "===================================================="

if [ ! -d ${nifti_dir} ]; then

    echo "Converting DICOM files for $subject_dir "
    echo

    cd ${subject_dir}

    mkdir -p $dicom_dir
    mv $(ls -1d *) ${dicom_dir}
    cd ${dicom_dir}

    find . -type f  | xargs lnflatten.sh dcm_flat

#   Convert DCM to NIFTI 
#   -d Date in filename [filename.dcm -> 20061230122032.nii]: Y,N = Y
#   -f Source filename [e.g. filename.par -> filename.nii]: Y,N = Y
#   -i ID  in filename [filename.dcm -> johndoe.nii]: Y,N = Y
#   -p Protocol in filename [filename.dcm -> TFE_T1.nii]: Y,N = Y
#   -r Reorient image to nearest orthogonal: Y,N

    cd dcm_flat
    dcm2nii -d N -f N -p N -r N .
    mkdir ${nifti_dir}
    mv *.gz ${nifti_dir}
    cp *.bval *.bvec ${nifti_dir}

    [ -f .bval ] && cp .bval ${nifti_dir}/bval
    [ -f .bvec ] && cp .bvec ${nifti_dir}/bvec

    cd ${nifti_dir}
    rm *s9999*.gz

else

    echo "Conversion from DICOM to NIFTI complete for $subject_dir"
    echo
    pwd
    echo
    cd ${nifti_dir}
    ls

fi

echo


# Chris Rorden's dcm2nii :: 16 Oct 2008
# Either drag and drop or specify command line options:
#   dcm2nii <options> <sourcenames>
#
# OPTIONS:
#
#   -d Date in filename [filename.dcm -> 20061230122032.nii]: Y,N = Y
#   -f Source filename [e.g. filename.par -> filename.nii]: Y,N = Y
#   -i ID  in filename [filename.dcm -> johndoe.nii]: Y,N = Y
#   -p Protocol in filename [filename.dcm -> TFE_T1.nii]: Y,N = Y
#   -r Reorient image to nearest orthogonal: Y,N
#
#  You can also set defaults by editing /home/sunny/medeng/bkraft/.dcm2nii/dcm2nii.ini
#
# EXAMPLE: dcm2nii -a y /Users/Joe/Documents/dcm/IM_0116
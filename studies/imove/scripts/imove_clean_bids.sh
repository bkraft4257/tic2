#!/usr/bin/env bash

# Contents of func directory
#
#
# Contents of fmap directory
#

start_dir=$PWD

subject_value=$1
session_value=$2

full_subject_session_value=sub-${subject_value}_ses-${session_value}

session_dir=${start_dir}/sub-${subject_value}/ses-${session_value}

echo 
echo "================================================================================="
echo
echo "session_value = " $subject_value 
echo "subject_value = " $session_value
echo
echo "session_dir   = " $session_dir

echo
echo "List images collected and stored as DICOM files"
echo "------------------------------------------------------------------------------------------------"-
bids_path=$ACTIVE_BIDS_PATH/.heudiconv/${subject_value}/ses-${session_value}/info/

$HDC_PATH/hdc_add_header.py -v ${bids_path}/dicominfo_ses-${session_value}.tsv \
                            -o ${bids_path}/dicominfo_ses-${session_value}.csv

echo
echo "List images converted by heudiconv (HDC)"
echo "-------------------------------------------------------------------------------------------------"
echo
cat -n ${bids_path}/${subject_value}_ses-${session_value}.edit.txt
echo
echo


#--- Remove .1., fmap/*.bval, fmap/*.bvec, fmap/*magnitude1*.json --------------------------------------------
#chmod +w -R ${session_dir}

find ${session_dir} -name "*.1.*" | xargs rename .1. .
find ${session_dir} -name "*.gz" -or -name "*.json" | xargs chmod +w 

cd ${session_dir}/fmap

# magnitude1 of the phasediff fieldmap does not require a json file according to BIDS. 
# Since the JSON file will be almost identical to phasediff.json file and is not required
# by the BIDS requirements I am removing it. 
rm -rf *magnitude1.json

# removing bval and bvecs from this directory.  These files were created from the DWI file 
# which is being used as its own TOPUP reference for distortion correction.
rm -rf *bvec *bval


#--- Extract volumes for topup distortion correction from data to match corresponding topup calibration scans ------
# Keep only the first 3 volumes of pcasl
echo
echo "Extract reference images for topup distortion correction"
echo "--------------------------------------------------------"

# Keep only the first 3 volumes of pcasl_rl
pcasl_topup_lr=${full_subject_session_value}_acq-pcasl_dir-rl_epi.nii.gz

if [ -f $pcasl_topup_lr ] 
then         
   echo fslroi $pcasl_topup_lr
   fslroi $pcasl_topup_lr  $pcasl_topup_lr 0 3

   echo
   fslinfo  $pcasl_topup_lr
   echo
else
    echo "$pcasl_topup_lr file not found"
fi

# Keep only the first 10 volumes of mbepi_rl
mbepi_topup_rl=${full_subject_session_value}_acq-mbepi_dir-rl_epi.nii.gz
if [ -f $mbepi_topup_rl ] 
then         
    echo fslroi $mbepi_topup_r
    fslroi $mbepi_topup_rl  $mbepi_topup_rl 0 10

    echo
    fslinfo $mbepi_topup_rl 
    echo

else
    echo "$mbepi_topup_rl file not found"
fi

#--- Update JSON files to include Echo1, Echo2, and IntendedFor information -------------------------------------

#--- Update JSON files to include IntendedFor information -------------------------------------

rest_topup_ap_json=${full_subject_session_value}_acq-epse_dir-ap_epi.json
rest_topup_pa_json=${full_subject_session_value}_acq-epse_dir-pa_epi.json
                                                
for ii in $rest_topup_ap_json $rest_topup_pa_json;
do 

    if [ -f $ii ] 
    then         
        sed -i 's%"AcquisitionNumber": 1,%"IntendedFor": [ "ses-__session_value__/func/sub-__subject_value___ses-__session_value___task-rest_acq-epi_rec-topup_bold.nii.gz" ],\n  "AcquisitionNumber": 1,%' $ii
	
	echo 
	grep -H -B 3 AcquisitionNumber $ii

    else
        echo "$ii file not found."
    fi  
done



mbepi_topup_lr_json=${full_subject_session_value}_acq-mbepi_dir-lr_epi.json
mbepi_topup_rl_json=${full_subject_session_value}_acq-mbepi_dir-rl_epi.json


for ii in $mbepi_topup_lr_json $mbepi_topup_rl_json;
do 

    if [ -f $ii ] 
    then         
        sed -i 's%"AcquisitionNumber": 1,%"IntendedFor": [ "ses-__session_value__/func/sub-__subject_value___ses-__session_value___task-rest_acq-mbepi_bold.nii.gz" ],\n  "AcquisitionNumber": 1,%' $ii
	
	echo 
	grep -H -B 3 AcquisitionNumber $ii

    else
        echo "$ii file not found."
    fi  
done


pcasl_topup_lr_json=${full_subject_session_value}_acq-pcasl_dir-lr_epi.json
pcasl_topup_rl_json=${full_subject_session_value}_acq-pcasl_dir-rl_epi.json

for ii in $pcasl_topup_lr_json $pcasl_topup_rl_json;
do 

    if [ -f $ii ] 
    then         
        sed -i 's%"AcquisitionNumber": 1,%"IntendedFor": [ "ses-__session_value__/func/sub-__subject_value___ses-__session_value___task-rest_acq-pcasl_bold.nii.gz" ],\n  "AcquisitionNumber": 1,%' $ii
	
	echo 
	grep -H -B 3 AcquisitionNumber $ii

    else
        echo "$ii file not found."
    fi  
done


# Replace __session__ with ${session_value} and __subject__ with ${subject_value}.
#  I would prefer to do this in a single call. Unfortunately, I haven't worked out the syntax

sed -i 's#__session_value__#'${session_value}'#g' *.json
sed -i 's#__subject_value__#'${subject_value}'#g' *.json

# This awk script removed the second IntendedFor if script is run multiple times. This is a complete hack
for ii in *.json; do
    awk '/IntendedFor/&&c++>0 {next} 1' $ii > tmp.$ii
    mv -f tmp.$ii $ii
done



echo
echo "grep -H IntendedFor *.json"
echo "-------------------------------------------------------------------------------------------------"
grep -H "IntendedFor" *.json
echo

cd $start_dir 

#--- Reorient all images to match FSL orientation -------------------------------------------------
echo "Reorienting all *.gz files with fslreorient2std"
echo "-----------------------------------------------"

for ii in $(find $session_dir -name "*.gz"); do
    echo "reorienting $ii "
    fslreorient2std $ii $ii
done

#echo 
#echo
#echo "Set permission to read only for *.nii.gz and *.json files"
#echo "--------------------------------------------------------------------------------"
#find $session_dir -type f -name "*.nii.gz" | xargs chmod -w -R 
#find $session_dir -type f -name "*.json"   | xargs chmod -w -R 

#--- Look for repeat scans -----------------------------------------------------------------------
echo
echo
echo "Looking for repeated scans one last time. "
echo "If you see something reported here you must CHOOSE which images you want to use."
echo "--------------------------------------------------------------------------------"

# The normal call is just
#
# find $session_dir -name "*.[0-9]*.*"
#
# I have specifically excluded swi scans because there is something peculiar with the conversion.  This needs and multiple
# copies are created. I am in the process of looking into this.

find $session_dir -name "*.[0-9]*.*" ! -path "*swi*"

echo

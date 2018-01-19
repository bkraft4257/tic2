#!/bin/bash

# Example on how to use this script.
#
# 1) Goto $INFINITE_BIDS_PATH.  Alias created cdsb
# 2) inf_clean_bids.sh  <subject_value,inf0117> <session_value,1>

# Contents of anat
#
#    sub-inf0122_ses-1_FLAIR.nii.gz  
#    sub-inf0122_ses-1_T1w.nii.gz
#
#
# Contents of fmap directory
#
#    sub-inf0122_ses-1_acq-bold_magnitude1.nii.gz
#    sub-inf0122_ses-1_acq-bold_phasediff.nii.gz
#
#    sub-inf0122_ses-1_acq-pcasl_magnitude1.nii.gz
#    sub-inf0122_ses-1_acq-pcasl_phasediff.nii.gz
#
#
# Contents of func directory
#
#   sub-inf0122_ses-1_task-rest_acq-epi_bold.nii.gz
#   sub-inf0122_ses-1_task-rest_acq-pcasl_bold.nii.gz
#
#
# Contents of dwi directory
#
#    sub-inf0122_ses-1_acq-30dir_dwi.nii.gz
#
#
#            series_id    sequence_name  dim1  dim2  dim3  dim4     TR      TE  is_derived  is_motion_corrected
#  0    2-MPRAGE_GRAPPA2     *tfl3d1_16ns   256   240   176     1  2.300    2.95       False                False
#  1    3-T2 SAG FLAIR SPACE  *spcir3d1_203ns   256   220   160     1  6.000  283.00       False                False
#  2    4-DTI_30dir_1b0_run1     *ep_b1000#29   112   112    60    31  8.500   82.00       False                False
#  3    5-DTI_30dir_1b0_run1      *ep_b0_1000   112   112    60     1  8.500   82.00        True                False
#  4    6-DTI_30dir_1b0_run1       *ep_b1000t   112   112    60     1  8.500   82.00        True                False
#  5    7-DTI_30dir_1b0_run1      *ep_b0_1000   112   112    60     1  8.500   82.00        True                False
#  6    8-DTI_30dir_1b0_run1        Not found   112   112    60     1 -1.000   -1.00        True                False
#  7   10-BOLD_resting     *epfid2d1_64    64    64    35   190  2.000   25.00       False                False
#  8   11-MPRAGE_GRAPPA2     *tfl3d1_16ns   256   256   131     1  2.300    2.95        True                False
#  9   12-Field_mapping          *fm2d2r    64    48    28     1  0.488    7.38       False                False
# 10   13-ASL_PERFUSION     *epfid2d1_64    64    64    24   105  3.400   13.00       False                False
# 11   14-ASL_PERFUSION     *epfid2d1_64    64    64    24   105  3.400   13.00        True                 True
# 12   15-ASL_PERFUSION     *epfid2d1_64    64    64    24     1  3.400   13.00        True                 True
# 13   16-ASL_PERFUSION     *epfid2d1_64    64    64    24     1  3.400   13.00        True                 True
# 14   17-gre_field_mapping          *fm2d2r   128   128    45     1  0.488    7.38       False                False


start_dir=$PWD

subject_value=$1  
session_value=$2

full_subject_session_value=sub-${subject_value}_ses-${session_value}

session_dir=${start_dir}/sub-${subject_value}/ses-${session_value}

source $INFINITE_SCRIPTS_PATH/inf_display_bids.sh $1 $2 

#echo 
#echo "================================================================================="
#echo
#echo "session_value = " $subject_value 
#echo "subject_value = " $session_value
#echo
#echo "session_dir   = " $session_dir
#
#echo
#echo "List images collected and stored as DICOM files"
#echo "------------------------------------------------------------------------------------------------"-
#
#hdc_bids_path=$INFINITE_PATH/bids.heudiconv/${subject_value}/ses-${session_value}/info/
#
#$HDC_PATH/hdc_add_header.py -v ${hdc_bids_path}/dicominfo_ses-${session_value}.tsv \
#                            -o ${hdc_bids_path}/dicominfo_ses-${session_value}.csv
#
#echo
#echo "List images converted by heudiconv (HDC)"
#echo "-------------------------------------------------------------------------------------------------"
#echo
#cat -n ${hdc_bids_path}/${subject_value}_ses-${session_value}.auto.txt
#echo
#echo


#--- Remove .1. from filenames and enable write permission --------------------------------------------
find ${session_dir} \( -name "*.gz" -or -name "*.json" \)| xargs chmod +w 

find ${session_dir} -name "*.1.*" | xargs rename .1. .


cd ${session_dir}/fmap

# magnitude1 of the phasediff fieldmap does not require a json file according to BIDS. 
# Since the JSON file will be almost identical to phasediff.json file and is not required
# by the BIDS requirements I am removing it. 
rm -rf *magnitude1*


#--- Update JSON files to include Echo1, Echo2, and IntendedFor information -------------------------------------

fmap_phasediff_bold=${full_subject_session_value}_acq-bold_phasediff.json
fmap_phasediff_pcasl=${full_subject_session_value}_acq-pcasl_phasediff.json

echo
echo "sed EchoTime and IntendedFor" 
echo "-----------------------------------------------------------------------"



#--- Update JSON files to include IntendedFor information -------------------------------------

if [ -f $fmap_phasediff_bold ] 
then  
    echo "Updating $fmap_phasediff_bold"          
    sed -i 's/"EchoTime": 0.00738,/"EchoTime1": 0.00492,\n  "EchoTime2": 0.00738,/' $fmap_phasediff_bold
    sed -i 's%"AcquisitionMatrixPE": 48,%"IntendedFor": [ "ses-__session_value__/func/sub-__subject_value___ses-__session_value___task-rest_acq-epi_bold.nii.gz" ],\n  "AcquisitionMatrixPE": 48,%' \
	$fmap_phasediff_bold
else
    echo "$fmap_phasediff_bold file not found"
fi

if [ -f $fmap_phasediff_pcasl ] 
then         
    echo "Updating $fmap_phasediff_bold"          
    sed -i 's/"EchoTime": 0.00738,/"EchoTime1": 0.00492,\n  "EchoTime2": 0.00738,/' $fmap_phasediff_pcasl
    sed -i 's%"AcquisitionMatrixPE": 128,%"IntendedFor": [ "ses-__session_value__/func/sub-__subject_value___ses-__session_value___task-rest_acq-pcasl_bold.nii.gz"],\n  "AcquisitionMatrixPE": 128,%' \
         $fmap_phasediff_pcasl
else
    echo "$fmap_phasediff_pcasl file not found"
fi

echo

# Replace __session__ with ${session_value} and __subject__ with ${subject_value}.
#  I would prefer to do this in a single call. Unfortunately, I haven't worked out the syntax

sed -i 's#__session_value__#'${session_value}'#g' *.json
sed -i 's#__subject_value__#'${subject_value}'#g' *.json

# This awk script removed the second IntendedFor if script is run multiple times. This is a complete hack
# but it works

for ii in *.json; do
    awk '/IntendedFor/&&c++>0 {next} 1' $ii > tmp.$ii
    mv -f tmp.$ii $ii
done

echo
echo "grep -H EchoTime *.json"
echo "-------------------------------------------------------------------------------------------------"
grep -H "EchoTime" *.json
echo

echo
echo "grep -H IntendedFor *.json"
echo "-------------------------------------------------------------------------------------------------"
grep -A 1 -H "IntendedFor" *.json
echo

cd $start_dir 

#--- Reorient all images to match FSL orientation -------------------------------------------------
echo "Reorienting all *.gz files with fslreorient2std"
echo "-----------------------------------------------"

for ii in $(find $session_dir -name "*.gz"); do
    echo "reorienting $ii "
    fslreorient2std $ii $ii
done



# Clean up any backup files.   These shouldn't exist unless the user inspected JSON files with a text
# editor.  Since I do this often I thought it would be helpful to remove them here

find $session_dir -name "*~" -delete

#--- Remove write permission from *.gz and *.json files   --------------------------------------------
# find ${session_dir} \( -name "*.gz" -or -name "*.json" \)| xargs chmod -w 

#--- Look for scan counter.  These should be removed by now.  If there are repeat scans (i.e. <1)
#    then user will need to decide which scans to use.
echo
echo
echo "Looking for repeated scans one last time. "
echo "If you see something reported here you must CHOOSE which images you want to use."
echo "--------------------------------------------------------------------------------"
find $session_dir -name "*.[0-9]*"

echo " "

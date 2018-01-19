#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('/cenc/software/heudiconv/python/heudiconv/heuristics')

import os
import numpy
from collections import namedtuple, OrderedDict
import re
import pprint

from hdc_protocol import *


"""
    ./heudiconv_add_header.py output/.heudiconv/syn054/ses-1/info/dicominfo_ses-1.tsv
    csvcut -c 3,7,8,9,10,11,12,13,14,15 dicominfo.csv | csvlook --max-rows 20

    Here is the criteria that you can use to select which dicom images to convert to NIFTI.

    regex criteria are fields that accept any valid regular expression.  If you provide a simple string the
    regex condition will return True if the string is contained in the corresponding DICOM field.  A useful
    regex expression when searching the series_id field is '^N'  where the ^ indicates that the expression 
    following the ^ starts at the beginning of the string.  This is helpful for selecting DICOM images
    to convert by series number.  

    range criteria are reserved for fields that contain either integers or floating point numbers.  A
    range criteria takes a minimum and maximum value.  The numbers are inclusive so the expression

    dim1 = [240, 272]   is equal to    240 <= dim1 <= 272

    boolean criteria are reserved for fields that can either be True or False. 

    You do not have to specify all the criteria. You just need to provide enough criteria to uniquely 
    identify the DICOM images that you want to convert.  If your images are not specific enough and 
    multiple images are found to be converted a number will be appended onto the name of the NIFTI images. 
    For example,  t1w_1.nii.gz, t1w_2.nii.gz and t1w_3.nii.gz.
   
    Here are the most useful criteria for specifying which DICOM images to convert to NIFTI
   
         3. series_id (regex) - contains series number and series description

         7. dim1 (range) - number of pixels in x direction
         8. dim1 (range) - number of pixels in y direction
         9. dim1 (range) - number of slices
        10. dim1 (range) - number of volumes

        11. TR,  (range) - Repetition Time
        12. TE,  (range) - Echo Time

        13. protocol_name (regex) - 

        14. is_motion_corrected (boolean) - 
        15. is_derived (boolean) - 

        20. sequence_name (regex) - sequence name used to acquired images.  Some of Siemens sequence names contain a 
                                    * in the name. * has special meaning in regex. It is easier to not include 
                                    the * in regex unless you are using it as a regular expression.  If you want to
                                    include the * in the regular expression as just another character
                                    without any special meaning then precede it with a \

        Rarely needed or used

         1. total_files_till_now
         2. example_dcm_file

         4. unspecified1 (regex)
         5. unspecified2 (regex)
         6. unspecified3 (regex)

        16. patient_id (regex) - 
        17. study_description (regex)
        18. referring_physician_name,
        19. series_description (regex)

        21. image_type (regex)
        22. accession_number (regex)
        23 patient_age (regex)
        24. patient_sex (regex)
        25. date (regex)

   In additon to specifying the criteria for converting DICOM fields if you are converting to the BIDS 
   directory structure you must specify the key

         key - key specifies where NIFTI files will be stored in BIDS directory
               'sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w'

   {subject} is the subject acrostic. This is a mandatory field and must be included
   {session} is the session identifier and is optional.    


"""

"""
https://docs.google.com/document/d/1HFUkAEE-pB-angVcYe6pf_-fVf4sCpOHKesUvfb8Grc/edit#heading=h.qdzsf8lh4for

BIDS Templates: 

    anat/
         sub-<participant_label>
            [_ses-<session_label>]
            [_acq-<label>]
            [_ce-<label>]
            [_rec-<label>]
            [_run-<index>]
            [_mod-<label>]_<modality_label>.nii[.gz]
"""
"""
                                      series_id sequence_name  dim1  dim2  dim3  dim4     TR      TE  is_derived  is_motion_corrected
0                              2-MPRAGE_GRAPPA2  *tfl3d1_16ns   256   240   192     1  2.300    2.98       False                False
1                        3-mbep2d_bold 3mm L>>R   epfid2d1_64    72    64    64     1  0.570   30.00       False                False
2                        4-mbep2d_bold 3mm L>>R   epfid2d1_64    72    64    64    10  0.570   30.00       False                False
3                        5-mbep2d_bold 3mm R>>L   epfid2d1_64    72    64    64     1  0.570   30.00       False                False
4                        6-mbep2d_bold 3mm R>>L   epfid2d1_64    72    64    64   500  0.570   30.00       False                False
5                          7-T2 FLAIR SPACE NEW  *spcir_192ns   256   236   192     1  5.000  395.00       False                False
6                     8-BOLD_resting 4X4X4 A>>P  *epfid2d1_64    64    64    35   190  2.000   25.00       False                False
7                             9-rest_topup_A>>P   *epse2d1_64    64    64   140     1  2.000   25.00       False                False
8                            10-rest_topup_P>>A   *epse2d1_64    64    64   140     1  2.000   25.00       False                False
9                   11-Field_mapping 4X4X4 A>>P       *fm2d2r    64    64    35     1  0.488    4.92       False                False
10                  12-Field_mapping 4X4X4 A>>P       *fm2d2r    64    64    35     1  0.488    7.38       False                False
11              13-pcasl_wfu_3_1 R>>L EYES OPEN   epfid2d1_56    70    56    43    81  4.000   11.00       False                False
15  17-pcasl_wfu_3_1 L>>R (COPY SLICES FROM R>L   epfid2d1_56    70    56    43     3  4.000   11.00       False                False
19                        21-DTI_30dir_1b0 A>>P        *ep_b0   112   112    60    31  8.500   82.00       False                False
24                        27-DTI_30dir_1b0 P>>A        *ep_b0   112   112    60     1  8.500   82.00       False                False
"""

def protocol():

    criteria = define_sequence_criteria()
    sequences = OrderedDict()

    sequences['t1w'] = criteria(key='sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w.{item:01d}',
                                series_description='MPRAGE_GRAPPA2',  
                                )

    sequences['flair'] = criteria(key='sub-{subject}/{session}/anat/sub-{subject}_{session}_FLAIR.{item:01d}',
                                series_description='T2 FLAIR SPACE',
                                sequence_name='spcir_192ns',
                                )

    sequences['rest_mbepi_topup_rl'] = criteria(key='sub-{subject}/{session}//fmap/sub-{subject}_{session}_acq-mbepi_dir-rl_epi.{item:01d}',
                                series_description='mbep2d_bold 3mm R>>L',
                                sequence_name='epfid2d1_64',
                                dim4=[500,500]
                                )

    sequences['rest_mbepi_topup_lr'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-mbepi_dir-lr_epi.{item:01d}',
                                series_description='mbep2d_bold 3mm L>>R',
                                sequence_name='epfid2d1_64',
                                dim4=[10,10]
                                )

#    sequences['rest_mbepi_sbref_lr'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-mbepi_sbref.{item:01d}',
#                                series_description='mbep2d_bold 3mm L>>R',
#                                sequence_name='epfid2d1_64',
#                                dim4=[1,1]
#                                )


    sequences['rest_mbepi'] = criteria(key='sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-mbepi_bold.{item:01d}',
                                series_description='mbep2d_bold 3mm R>>L',
                                sequence_name='epfid2d1_64',
                                dim4=[500,500]
                                )

    sequences['rest_mbepi_sbref'] = criteria(key='sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-mbepi_sbref.{item:01d}',
                                series_description='mbep2d_bold 3mm R>>L',
                                sequence_name='epfid2d1_64',
                                dim4=[1,1]
                                )


    sequences['rest'] = criteria(key='sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-epi_bold.{item:01d}',
                                series_description='BOLD_resting',
                                sequence_name='epfid2d1_64',
                                dim4=[190,190]
                                )

    sequences['rest_topup_ap'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-epse_dir-ap_epi.{item:01d}',
                                series_description='rest_topup_A>>P',
                                sequence_name='epse2d1_64',
                                dim3=[140,140],
                                dim4=[1,1]
                                )

    sequences['rest_topup_pa'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-epse_dir-pa_epi.{item:01d}',
                                series_description='rest_topup_P>>A',
                                sequence_name='epse2d1_64',
                                dim3=[140,140],
                                dim4=[1,1]
                                )

    sequences['fmap_magnitude1'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-bold_magnitude1.{item:01d}',
                                      series_description='Field_mapping',
                                      sequence_name='fm2d2r',
                                      TE=[4.92,4.92]
                                     )

    sequences['fmap_phasediff'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-bold_phasediff.{item:01d}',
                                      series_description='Field_mapping',
                                      sequence_name='fm2d2r',
                                      TE=[7.38,7.38]
                                     )

    sequences['pcasl_rl'] = criteria(key='sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-pcasl_bold.{item:01d}',
                                series_description='pcasl_wfu_3_1 R>>L',
                                sequence_name='epfid2d1_56',
                                dim4=[81,81],
                                )

    # Convert this twice to create the JSON file.  This file will then be modified later to match pcasl_topup_rl
    sequences['pcasl_topup_lr'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-pcasl_dir-lr_epi.{item:01d}',
                                series_description='pcasl_wfu_3_1 L>>R',
                                sequence_name='epfid2d1_56',
                                dim4=[3,3],
                                )

    sequences['pcasl_topup_rl'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-pcasl_dir-rl_epi.{item:01d}',
                                series_description='pcasl_wfu_3_1 R>>L',
                                sequence_name='epfid2d1_56',
                                dim4=[81,81]
                                )



    sequences['dti_30dir_ap'] = criteria(key='sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-30ap_dwi.{item:01d}',
                                series_description='DTI_30dir',
                                sequence_name='ep_b0',
                                dim4=[31,31],
                                is_derived=False
                                )

    # Convert this twice to create the JSON file.  This file will then be modified later to match dti_30dir_topup_pa
    sequences['dti_30dir_topup_ap'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-30ap_dir-ap_epi.{item:01d}',
                                              series_description='DTI_30dir',
                                              sequence_name='ep_b0',
                                              dim4=[31,31],
                                              is_derived=False
                                              )             

    sequences['dti_30dir_topup_pa'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-30ap_dir-pa_epi.{item:01d}',
                                               series_description='DTI_30dir',
                                               sequence_name='ep_b0',
                                               dim4=[1,1],
                                               is_derived=False
                                               )              

    print(sequences)

    return sequences



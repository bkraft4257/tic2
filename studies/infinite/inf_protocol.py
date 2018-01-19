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
INFINITE Protocol

              series_id    sequence_name  dim1  dim2  dim3  dim4      TR      TE  is_derived  is_motion_corrected
      2-MPRAGE_GRAPPA2     *tfl3d1_16ns   256   240   176     1   2.300    2.95       False                False
  3-T2 SAG FLAIR SPACE  *spcir3d1_203ns   256   220   160     1   6.000  283.00       False                False
  4-DTI_30dir_1b0_run1           *ep_b0   112   112    60    31  11.300   82.00       False                False
        5-BOLD_resting     *epfid2d1_64    64    64    35   190   2.000   25.00       False                False
       6-Field_mapping          *fm2d2r    64    48    28     1   0.488    7.38       False                False
       7-ASL_PERFUSION     *epfid2d1_64    64    64    24   105   3.400   13.00       False                False
       8-ASL_PERFUSION     *epfid2d1_64    64    64    24   105   3.400   13.00        True                 True
       9-ASL_PERFUSION     *epfid2d1_64    64    64    24     1   3.400   13.00        True                 True
      10-ASL_PERFUSION     *epfid2d1_64    64    64    24     1   3.400   13.00        True                 True



"""




def protocol():

    criteria = define_sequence_criteria()
    sequences = OrderedDict()

    sequences['t1w'] = criteria(key='sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w.{item:01d}',
                                series_description='MPRAGE_GRAPPA2',  
                                )

    sequences['flair'] = criteria(key='sub-{subject}/{session}/anat/sub-{subject}_{session}_FLAIR.{item:01d}',
                                series_description='FLAIR SPACE',
                                sequence_name='spcir',
                                )

    sequences['rest'] = criteria(key='sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-epi_bold.{item:01d}',
                                series_description='BOLD_resting',  
                                sequence_name='epfid2d1_64',
                                dim4=[190,190]
                                )

    sequences['fmap_rest_phasediff'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-bold_phasediff.{item:01d}',
                                           series_description='Field_mapping',  
                                           sequence_name='fm2d2r',
                                           TE=[7.38, 7.38],
                                           )

    sequences['fmap_rest_magnitude'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-bold_magnitude1.{item:01d}',
                                      series_description='Field_mapping',  
                                      sequence_name='fm2d2r',
                                      TE=[4.92, 4.92],
                                     )


    sequences['cbf'] = criteria(key='sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-pcasl_bold.{item:01d}',
                                series_description='ASL_PERFUSION',  
                                sequence_name='epfid2d1_64',
                                is_derived=False,
                                dim4=[105,105]
                                )

    sequences['fmap_cbf_phasediff'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-pcasl_phasediff.{item:01d}',
                                      series_description='gre_field_mapping',  
                                      sequence_name='fm2d2r',
                                      TE=[7.38, 7.38],
                                     )

    sequences['fmap_cbf_magnitude1'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-pcasl_magnitude1.{item:01d}',
                                                series_description='gre_field_mapping',  
                                                sequence_name='fm2d2r',
                                                TE=[4.92, 4.92],
                                     )

    sequences['dti_30dir'] = criteria(key='sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-30dir_dwi.{item:01d}',
                                series_description='DTI_30dir',  
                                dim4=[31,31],
                                is_derived=False
                                )


    print(sequences)

    return sequences



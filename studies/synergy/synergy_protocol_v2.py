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
3-T1_MPRAGE_GRAPPA2,256,240,192,1,2.3,2.98,T1_MPRAGE_GRAPPA2,False,False

4-TOF_3D_multi-slab SHORT,512,464,72,1,0.021,3.43,TOF_3D_multi-slab SHORT,False,False
5-TOF_3D_multi-slab SHORT,184,512,1,1,0.021,3.43,TOF_3D_multi-slab SHORT,False,False
6-TOF_3D_multi-slab SHORT,184,464,1,1,0.021,3.43,TOF_3D_multi-slab SHORT,False,False
7-TOF_3D_multi-slab SHORT,512,464,1,1,0.021,3.43,TOF_3D_multi-slab SHORT,False,False

8-BOLD_resting 4X4X4 A>>P,64,64,35,190,2.0,25.0,BOLD_resting 4X4X4 A>>P,False,False

9-TOF_3D_multi-slab SHORT,184,464,1,1,0.021,3.43,TOF_3D_multi-slab SHORT,False,False

10-rest_topup_A>>P,64,64,140,1,2.0,25.0,rest_topup_A>>P,False,False
11-rest_topup_P>>A,64,64,140,1,2.0,25.0,rest_topup_P>>A,False,False

12-TOF_3D_multi-slab SHORT,512,464,1,1,0.021,3.43,TOF_3D_multi-slab SHORT,False,False
13-TOF_3D_multi-slab SHORT,512,464,1,1,0.021,3.43,TOF_3D_multi-slab SHORT,False,False

14-Brain 2D PhCon BILATERAL INT. CAROTIDS,192,144,20,1,0.03972,3.86,Brain 2D PhCon BILATERAL INT. CAROTIDS,False,False
15-Brain 2D PhCon BILATERAL INT. CAROTIDS,192,144,20,1,0.03972,3.86,Brain 2D PhCon BILATERAL INT. CAROTIDS,False,True

16-Brain 2D PhCon RT MCA,192,144,20,1,0.03972,3.86,Brain 2D PhCon RT MCA,False,False
17-Brain 2D PhCon RT MCA,192,144,20,1,0.03972,3.86,Brain 2D PhCon RT MCA,False,True
18-Brain 2D PhCon LT MCA,192,144,20,1,0.03972,3.86,Brain 2D PhCon LT MCA,False,False
19-Brain 2D PhCon LT MCA,192,144,20,1,0.03972,3.86,Brain 2D PhCon LT MCA,False,True
"""



"""
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

def protocol():

    criteria = define_sequence_criteria()
    sequences = OrderedDict()

    sequences['t1w'] = criteria(key='sub-{subject}/{session}/anat/sub-{subject}_mod-mprage_{session}_T1w',
                                series_description='MPRAGE',  
                                )

    sequences['tof'] = criteria(key='sub-{subject}/{session}/anat/sub-{subject}_{session}_mod-3dtof_angio',
                                series_description='TOF_3D',
                                sequence_name='fl3d1r_t70',
                                dim3=[64,128]
                                )

    sequences['pc_bilateral'] = criteria(key='sub-{subject}/{session}/anat/sub-{subject}_{session}_run-both_angio',
                                series_description='2D PhCon BILATERAL',
                                sequence_name='fl3d1r_t70',
                                is_derived=False
                                )

    sequences['pc_right_mca'] = criteria(key='sub-{subject}/{session}/anat/sub-{subject}_{session}_run-right_angio',
                                series_description='2D PhCon RT MCA',
                                sequence_name='fl2d1r3',
                                is_derived=False
                                )

    sequences['pc_left_mca'] = criteria(key='sub-{subject}/{session}/anat/sub-{subject}_{session}_run-left_angio',
                                series_description='2D PhCon LT MCA',
                                sequence_name='fl2d1r3',
                                is_derived=False
                                )

    sequences['rest_ap'] = criteria(key='sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-epi_bold',
                                series_description='BOLD_resting',  
                                )

    sequences['rest_topup_ap'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-topup_dir-ap_epi',
                                series_description='rest_topup_A>>P',  
                                )

    sequences['rest_topup_pa'] = criteria(key='sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-topup_dir-pa_epi',
                                series_description='rest_topup_P>>A',  
                                )

    print(sequences)

    return sequences


verbose=True

regex_criteria = ['total_files_till_now',
                  'example_dcm_file',
                  'series_id',
                  'unspecified1',
                  'unspecified2',
                  'unspecified3',
                  'protocol_name',
                  'patient_id',
                  'study_description',
                  'referring_physician_name',
                  'series_description',
                  'sequence_name',
                  'image_type',
                  'accession_number',
                  'patient_age',
                  'patient_sex',
                  'date'
                  ]

boolean_criteria = [ 'is_motion_corrected',
                     'is_derived']

range_criteria = ['dim1',
                  'dim2',
                  'dim3',
                  'dim4',
                  'TR',
                  'TE']

def define_sequence_criteria(verbose=False):

    # Define protocol
    criteria = namedtuple(
        'criteria',
        ['key',
         'total_files_till_now',
         'example_dcm_file',
         'series_id',  # series_id   special regex
         'unspecified1',
         'unspecified2',
         'unspecified3',
         'dim1',  # range
         'dim2',  # range
         'dim3',  # range
         'dim4',  # range
         'TR',  # range
         'TE',  # range
         'protocol_name',  # regex
         'is_motion_corrected',
         'is_derived',  # boolean
         'patient_id',
         'study_description',
         'referring_physician_name',
         'series_description',  # regex
         'sequence_name',       # regex
         'image_type',
         'accession_number',
         'patient_age',
         'patient_sex',
         'date'
    ],
        verbose=False
    )

    criteria.__new__.__defaults__ = (None,) * len(criteria._fields)

    return criteria


def _condition_regex(name, measured, criteria, verbose=False):

    criteria_value = getattr(criteria, name)

    if criteria_value is not None:

        try:
            re.compile(criteria_value)
        except re.error:
            print('{0} must be a valid regular expression.'.format(criteria_value))
            raise ValueError

        measured_value = getattr(measured, name)

        criteria_met = bool(re.search(criteria_value, measured_value))

        if verbose:
            print('{0}: re.search({1},{2}) is {3}'.format(name, criteria_value,
                                                                                 measured_value, criteria_met ))

    else:
        criteria_met = True

    return criteria_met

def _print_criteria(criteria):
    print('\n')
    print(criteria)

#    for k in acquired._fields:
#        print('{0}={1}'.format(k, getattr(acquired, k)))

    print('\n')

    return


def _print_protocol(acquired):
    print('\n')

    for k in acquired._fields:
        print('{0}={1}'.format(k, getattr(acquired, k)))

    print('\n')

    return


def _condition_boolean(name, measured, criteria, verbose=False):

    criteria_value = getattr(criteria, name)

    if criteria_value is not None:

        if (type(criteria_value) != bool):
            print('{0} is a boolean criteria. It must be a boolean.')
            raise TypeError

        measured_value = getattr(measured, name)
        criteria_met =  (measured_value == criteria_value)

        if verbose:
            print("{0}: {1} == {2} is {3}".format(name, measured_value, criteria_value, criteria_met ))

    else:
        criteria_met = True   # If the condition set by the user is None then ignore this condition and force it to be
                              # met.

    return criteria_met



def _condition_range(name, measured, criteria, verbose=False):

    criteria_value = getattr(criteria, name)

    if criteria_value is not None:

        if (type(criteria_value) != list):
            print('{0} range criteria must be a list with 2 elements (minimum, maximum).'.format(name))
            raise TypeError

        if (len(criteria_value) != 2):
            print('{0} range criteria must be a list with 2 elements (minimum, maximum).'.format(name))
            raise ValueError

        measured_value = getattr(measured, name)
        criteria_met = (criteria_value[0] <= measured_value <= criteria_value[1])

        if verbose:
            print("{0}: {1} <= {2} <= {3} is {4}".format(name, criteria_value[0], measured_value, criteria_value[1],
                                                     criteria_met ))

    else:
        criteria_met = True   # If the condition set by the user is None then ignore this condition and force it to be
                              # met.

    return criteria_met


def _convert(acquired, criteria, verbose=True):

    if verbose:
        print('\n\n=======================================================\n')

        _print_protocol(acquired)
        _print_criteria(criteria)

    regex_conditions = [ _condition_regex(ii, acquired, criteria, verbose=verbose) for ii in regex_criteria ]
    range_conditions = [ _condition_range(ii, acquired, criteria, verbose=verbose) for ii in range_criteria]
    boolean_conditions = [_condition_boolean(ii, acquired, criteria, verbose=verbose) for ii in boolean_criteria]

    all_conditions = regex_conditions + range_conditions + boolean_conditions
    convert = numpy.asarray(all_conditions).all() & bool(all_conditions) # An empty list is false.
                                                                             # —PEP-8 style guides

    if verbose:
       if convert:
           print('\n!!!! Converting ...\n')
       else:
           print('\n!!!! Skipping ...\n')

    return convert


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo, verbose=True):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    criteria = protocol()

    keys = { key:create_key( value.key ) for key, value in criteria.items()}
    info = { value:[]  for _, value in keys.items() }

    for acquired in seqinfo:
        for ii_keys in criteria.keys():
            if _convert(acquired, criteria[ii_keys], verbose=True):
                info[ keys[ii_keys] ].append(acquired.series_id)

    return info





#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script for gathering inputs for CONN
"""

import os
import glob
import pprint
import sys
import pandas
from collections import namedtuple

from IPython.display import display

import shutil

SUBJECT = 'mfc902'
SESSION = 1

IMAGE_PROCESSING_PATH = os.getenv('ACTIVE_IMAGE_PROCESSING_PATH')
FMRIPREP_PATH = os.getenv('ACTIVE_FMRIPREP_PATH')
CONN_PATH = os.path.join(IMAGE_PROCESSING_PATH, 'conn')

SUBJECT_SESSION_PATH = os.path.join(FMRIPREP_PATH, f'sub-{SUBJECT}', f'ses-{SESSION}')

ANAT_PATH = os.path.join(SUBJECT_SESSION_PATH, 'anat')
FUNC_PATH = os.path.join(SUBJECT_SESSION_PATH, 'func')

TASKS = ['preRest', 'preHeat1', 'preHeat2', 'postHeat3', 'postHeat4', 'postRest']

CONFOUNDS = ['X', 'Y', 'Z', 'RotX', 'RotY', 'RotZ']

GATHER = namedtuple('Gather', ['name', 'type', 'glob_string', 'copy_to_filename', ])


GATHER_DICT = dict()

GATHER_DICT['csf'] = GATHER('csf', 'anat', '/anat/*_T1w_space-MNI152NLin2009cAsym_class-CSF_probtissue.nii.gz',  'csf.nii.gz')
GATHER_DICT['wm'] = GATHER('wm', 'anat', '/anat/*_T1w_space-MNI152NLin2009cAsym_class-WM_probtissue.nii.gz',  'wm.nii.gz')
GATHER_DICT['gm'] = GATHER('gm', 'anat', '/anat/*_T1w_space-MNI152NLin2009cAsym_class-GM_probtissue.nii.gz', 'gm.nii.gz')
GATHER_DICT['t1'] = GATHER('t1', 'anat', '/anat/*_T1w_space-MNI152NLin2009cAsym_preproc.nii.gz', 't1w.nii.gz')


GATHER_DICT['pre_neutral_1'] = GATHER('pre_neutral_1',
                                      'fmri',
                                      '_task-preNeutral1_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz',
                                      'pre_neutral_1.nii.gz')

GATHER_DICT['pre_neutral_1_confounds'] = GATHER('pre_neutral_1',
                                                'confounds',
                                                '_task-preNeutral1_acq-epi_rec-topup_bold_confounds.csv',
                                                'pre_neutral_1.csv')

GATHER_DICT['pre_heat_1'] = GATHER('pre_heat_1',
                                   'fmri',
                                   '_task-preHeat1_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz',
                                   'pre_heat_1.nii.gz')

GATHER_DICT['pre_heat_1_confounds'] = GATHER('pre_heat_1',
                                             'confounds',
                                             '_task-preHeat1_acq-epi_rec-topup_bold_confounds.csv',
                                             'pre_heat_1.csv')


def _read_confounds(filename, confounds):
    df_confounds = pandas.read_csv(filename, sep='\t', usecols=confounds)
    return df_confounds


def _write_confounds(in_df, filename):
    in_df.to_csv(filename, index=False, float_format='%.6f')


def _make_conn_directory(directory=CONN_PATH):
    """
    Make CONN directory if it doesn't exist

    :return:
    """

    if not os.path.exists(directory):
        os.makedirs(directory)


def _pre_allocate_2d_list(dim1, dim2):
    return [[0 for jj in range(dim2)] for ii in range(dim1)]


def _find_functional_images(subject, func_path=FUNC_PATH):
    """

    :param func_path:
    :return:

     1	sub-mfc902_ses-1_task-postHeat3_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz
     2	sub-mfc902_ses-1_task-postHeat4_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz
     3	sub-mfc902_ses-1_task-postRest_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz
     4	sub-mfc902_ses-1_task-preHeat1_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz
     5	sub-mfc902_ses-1_task-preHeat2_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz
     6	sub-mfc902_ses-1_task-preRest_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz

    """

    func_files = _pre_allocate_2d_list(6,3)

    for jj, jj_bold in enumerate(['space-MNI152NLin2009cAsym_preproc.nii.gz', 'confounds.tsv'], 1):
        for ii, ii_task in enumerate(TASKS):

            func_files[ii][0] = f'{subject}_{ii_task}'

            search_string = f'{func_path}/*task-{ii_task}_acq-epi_rec-topup_bold_{jj_bold}'

            tmp = glob.glob(search_string)

            if len(tmp) == 1:
                func_files[ii][jj] = tmp[0]

    return func_files


def _find_file(glob_string, directory):

    file_found = glob.glob(f'{directory}/{glob_string}')

    if len(file_found) > 1:
        sys.exit('Found more than 1 file. Revise glob string.')

    return file_found[0]


def _copy_file(gather, search_directory, copy_to_directory=CONN_PATH):
    found_file = _find_file(gather.glob_string, search_directory)
    shutil.copy(found_file, os.path.join(copy_to_directory, gather.copy_to_filename))

    print(found_file)

    return


def _find_structural_images(subject, anat_path):
    """

    :param anat_path:
    :return:
    """

    anat_files = [0]*5
    anat_files[0] = f'{subject}'

    anat_files[1] = glob.glob(f'{anat_path}/*_T1w_space-MNI152NLin2009cAsym_preproc.nii.gz')[0]

    for ii, ii_tissue_type in enumerate(['CSF', 'GM', 'WM'],2):
        anat_files[ii] = glob.glob(f'{anat_path}/*T1w_space-MNI152NLin2009cAsym_class-{ii_tissue_type}_probtissue.nii.gz')[0]

    return anat_files


def main():
    _make_conn_directory()

    for ii in ['csf', 'wm', 'gm', 'csf']:
        _copy_file(GATHER_DICT[ii], SUBJECT_SESSION_PATH)


if __name__ == '__main__':
    sys.exit(main())

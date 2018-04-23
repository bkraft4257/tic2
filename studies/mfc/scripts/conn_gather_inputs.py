#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script for gathering inputs for CONN
"""

import os
import glob
import pprint
import sys
import shutil

SUBJECT = 'mfc902'
SESSION = 1

IMAGE_PROCESSING_PATH = os.getenv('ACTIVE_IMAGE_PROCESSING_PATH')
FMRIPREP_PATH = os.getenv('ACTIVE_FMRIPREP_PATH')
CONN_PATH = os.path.join(IMAGE_PROCESSING_PATH, 'conn')

SUBJECT_SESSION_PATH = os.path.join(FMRIPREP_PATH, f'sub-{SUBJECT}', f'ses-{SESSION}')

ANAT_PATH = os.path.join(SUBJECT_SESSION_PATH, 'anat')
FUNC_PATH = os.path.join(SUBJECT_SESSION_PATH, 'func')

TASKS = ['preRest', 'preHeat1', 'preHeat2', 'postRest', 'postHeat3', 'postHeat4' ]


def _make_conn_directory(directory=CONN_PATH):
    """
    Make CONN directory if it doesn't exist

    :return:
    """

    if not os.path.exists(directory):
        os.makedirs(directory)

# sub-mcf901_ses-1_T1w_space-MNI152NLin2009cAsym_preproc.nii.gz
# sub-mcf901_ses-1_T1w_space-MNI152NLin2009cAsym_class-CSF_probtissue.nii.gz
# sub-mcf901_ses-1_T1w_space-MNI152NLin2009cAsym_class-GM_probtissue.nii.gz
# sub-mcf901_ses-1_T1w_space-MNI152NLin2009cAsym_class-WM_probtissue.nii.gz

# sub-mcf901_ses-1_task-postRest_acq-mbepi_bold_confounds.txt~
# sub-mcf901_ses-1_task-postRest_acq-mbepi_bold_space-MNI152NLin2009cAsym_preproc.nii.gz


def _pre_allocate_2d_list(dim1, dim2):
    return [[ 0 for jj in range(dim2)] for ii in range(dim1)]


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
    print(func_files)

    for jj, jj_bold in enumerate(['space-MNI152NLin2009cAsym_preproc.nii.gz', 'confounds.tsv'], 1):
        for ii, ii_task in enumerate(TASKS):

            func_files[ii][0] = f'{subject}_{ii_task}'

            search_string = f'{func_path}/*task-{ii_task}_acq-epi_rec-topup_bold_{jj_bold}'

            tmp = glob.glob(search_string)

            if len(tmp) == 1:
                func_files[ii][jj] = tmp[0]

    return func_files


def _find_structural_images(subject, anat_path):
    """

    :param anat_path:
    :return:
    """

    anat_files = _pre_allocate_2d_list(2, 4)

    t1w = glob.glob(f'{anat_path}/*_T1w_space-MNI152NLin2009cAsym_preproc.nii.gz')

    tissue_maps = []

    for ii in ['CSF', 'GM', 'WM']:
        tissue_maps.append(glob.glob(f'{anat_path}/*T1w_space-MNI152NLin2009cAsym_class-{ii}_probtissue.nii.gz'))

    return t1w, tissue_maps


def main():
    _make_conn_directory()

    t1w, tissue_maps = _find_structural_images(SUBJECT, ANAT_PATH)
    func_files = _find_functional_images(SUBJECT, FUNC_PATH)

    pprint.pprint(func_files)


if __name__ == '__main__':
    sys.exit(main())

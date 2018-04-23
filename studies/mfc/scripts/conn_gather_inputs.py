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


def _find_functional_images(func_path):
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

    func_files = [[ 0 for ii in range(6)] for jj in range(2)]
    print(func_files)
    print(func_files.size)

    for jj, jj_bold in enumerate(['space-MNI152NLin2009cAsym_preproc.nii.gz', 'confounds.tsv']):
        for ii, ii_task in enumerate(TASKS):

            search_string = f'{func_path}/*task-{ii_task}_acq-epi_rec-topup_bold_{jj_bold}'
            print(search_string)

            tmp = glob.glob(search_string)
            print(tmp)

            if len(tmp) == 1:
                func_files[ii,jj] = tmp[0]

    return func_files


def _find_bold_confounds():
    """

    :return:

     1	sub-mfc902_ses-1_task-postHeat3_acq-epi_rec-topup_bold_confounds.tsv
     2	sub-mfc902_ses-1_task-postHeat4_acq-epi_rec-topup_bold_confounds.tsv
     3	sub-mfc902_ses-1_task-postRest_acq-epi_rec-topup_bold_confounds.tsv
     4	sub-mfc902_ses-1_task-preHeat1_acq-epi_rec-topup_bold_confounds.tsv
     5	sub-mfc902_ses-1_task-preHeat2_acq-epi_rec-topup_bold_confounds.tsv
     6	sub-mfc902_ses-1_task-preRest_acq-epi_rec-topup_bold_confounds.tsv
    """

    pass


def _find_structural_images(anat_path):
    """

    :param anat_path:
    :return:
    """

    t1w = glob.glob(f'{anat_path}/*_T1w_space-MNI152NLin2009cAsym_preproc.nii.gz')

    tissue_maps = []

    for ii in ['CSF', 'GM', 'WM']:
        tissue_maps.append(glob.glob(f'{anat_path}/*T1w_space-MNI152NLin2009cAsym_class-{ii}_probtissue.nii.gz'))

    return t1w, tissue_maps


def main():
    _make_conn_directory()

    t1w, tissue_maps = _find_structural_images(ANAT_PATH)
    func_files = _find_functional_images(FUNC_PATH)

    pprint.pprint(func_files)


if __name__ == '__main__':
    sys.exit(main())

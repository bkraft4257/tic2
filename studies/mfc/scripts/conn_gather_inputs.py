#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script for gathering inputs for CONN
"""

import os
import glob
import shutil

SUBJECT = 'mfc902'
SESSION = 1

IMAGE_PROCESSING_PATH = os.getenv('ACTIVE_IMAGE_PROCESSING_PATH')
FMRIPREP_PATH = os.getenv('ACTIVE_FMRIPREP_PATH')
CONN_PATH = os.path.join(IMAGE_PROCESSING_PATH, 'conn')

SUBJECT_SESSION_PATH = os.path.join(FMRIPREP_PATH, f'sub-{SUBJECT}', f'ses-{SESSION}')

ANAT_PATH = os.path.join(SUBJECT_SESSION_PATH, 'anat')
FMRI_PATH = os.path.join(SUBJECT_SESSION_PATH, 'fmri')


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


def _find_functional_images(fmri_path):
    pass


def _find_bold_confounds():
    pass


def _find_structural_images(anat_path):

    t1w = glob.glob(f'{anat_path}/*_T1w_space-MNI152NLin2009cAsym_preproc.nii.gz')

    tissue_maps = []

    for ii in ['CSF', 'GM', 'WM']:
        tissue_maps.append(glob.glob(f'{anat_path}/*T1w_space-MNI152NLin2009cAsym_class-{ii}_probtissue.nii.gz'))

    return t1w, tissue_maps


if __name__ == '__main__':

    _make_conn_directory()

    t1w, tissue_maps = _find_structural_images(ANAT_PATH)

    print(t1w)
    print(tissue_maps)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script for gathering inputs for CONN
"""

import argparse
import os
import glob
import pprint
import sys
import pandas
from collections import namedtuple

from IPython.display import display

import shutil
import nipype.interfaces.fsl as fsl          # fsl


IMAGE_PROCESSING_PATH = os.getenv('ACTIVE_IMAGE_PROCESSING_PATH')
FMRIPREP_PATH = os.getenv('ACTIVE_FMRIPREP_PATH')
CONN_PATH = os.path.join(IMAGE_PROCESSING_PATH, 'conn')



TASKS = ['preRest', 'preHeat1', 'preHeat2', 'postHeat3', 'postHeat4', 'postRest']

CONFOUNDS = ['X', 'Y', 'Z', 'RotX', 'RotY', 'RotZ']

ANAT_NT = namedtuple('ANAT_NT', ['name', 'type', 'glob_string', 'out_filename'])
FUNC_NT = namedtuple('FUNC_NT', ['name', 'type', 'func_glob_string', 'mask_glob_string', 'out_filename',])
CONFOUNDS_NT = namedtuple('CONFOUNDS_NT', ['name', 'type', 'glob_string', 'out_filename',])

ANAT_DICT = dict()
ANAT_DICT['csf'] = ANAT_NT('csf', 'anat', '/anat/*_T1w_space-MNI152NLin2009cAsym_class-CSF_probtissue.nii.gz',  'csf.nii.gz')
ANAT_DICT['wm'] = ANAT_NT('wm', 'anat', '/anat/*_T1w_space-MNI152NLin2009cAsym_class-WM_probtissue.nii.gz',  'wm.nii.gz')
ANAT_DICT['gm'] = ANAT_NT('gm', 'anat', '/anat/*_T1w_space-MNI152NLin2009cAsym_class-GM_probtissue.nii.gz', 'gm.nii.gz')
ANAT_DICT['t1'] = ANAT_NT('t1', 'anat', '/anat/*_T1w_space-MNI152NLin2009cAsym_preproc.nii.gz', 't1w.nii.gz')


FUNC_DICT = dict()
FUNC_DICT['pre_neutral_1'] = FUNC_NT('pre_neutral_1',
                                     'fmri',
                                     '/func/*_task-preRest_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz',
                                     '/func/*_task-preRest_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz',
                                     'pre_neutral_1.nii.gz')

FUNC_DICT = dict()
FUNC_DICT['pre_neutral_2'] = FUNC_NT('pre_neutral_2',
                                     'fmri',
                                     '/func/*_task-preRest_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz',
                                     '/func/*_task-preRest_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz',
                                     'pre_neutral_2.nii.gz')

FUNC_DICT = dict()
FUNC_DICT['post_neutral_3'] = FUNC_NT('post_neutral_3',
                                     'fmri',
                                     '/func/*_task-postRest_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz',
                                     '/func/*_task-postRest_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz',
                                     'pre_neutral_2.nii.gz')

FUNC_DICT = dict()
FUNC_DICT['post_neutral_4'] = FUNC_NT('post_neutral_4',
                                     'fmri',
                                     '/func/*_task-postRest_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz',
                                     '/func/*_task-postRest_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz',
                                     'pre_neutral_2.nii.gz')

FUNC_DICT = dict()
FUNC_DICT['pre_heat_1'] = FUNC_NT('pre_heat_1',
                                  'fmri',
                                  '/func/*_task-preHeat1_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz',
                                  '/func/*_task-preHeat1_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz',
                                  'pre_heat_1.nii.gz')

FUNC_DICT = dict()
FUNC_DICT['pre_heat_2'] = FUNC_NT('pre_heat_2',
                                  'fmri',
                                  '/func/*_task-preHeat2_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz',
                                  '/func/*_task-preHeat2_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz',
                                  'pre_heat_2.nii.gz')

FUNC_DICT = dict()
FUNC_DICT['post_heat_3'] = FUNC_NT('post_heat_3',
                                   'fmri',
                                   '/func/*_task-postHeat3_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz',
                                   '/func/*_task-postHeat3_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz',
                                   'post_heat_3.nii.gz')

FUNC_DICT = dict()
FUNC_DICT['post_heat_4'] = FUNC_NT('post_heat_4',
                                   'fmri',
                                   '/func/*_task-postHeat4_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_preproc.nii.gz',
                                   '/func/*_task-postHeat4_acq-epi_rec-topup_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz',
                                   'post_heat_4.nii.gz')


CONFOUNDS_DICT = dict()
CONFOUNDS_DICT['pre_neutral_1'] = CONFOUNDS_NT('pre_neutral_1',
                                               'confounds',
                                               '/func/*_task-preRest_acq-epi_rec-topup_bold_confounds.tsv',
                                               'pre_neutral_1_confounds.csv')

CONFOUNDS_DICT = dict()
CONFOUNDS_DICT['pre_neutral_2'] = CONFOUNDS_NT('pre_neutral_2',
                                               'confounds',
                                               '/func/*_task-preRest_acq-epi_rec-topup_bold_confounds.tsv',
                                               'pre_neutral_2_confounds.csv')
CONFOUNDS_DICT = dict()
CONFOUNDS_DICT['post_neutral_3'] = CONFOUNDS_NT('post_neutral_3',
                                               'confounds',
                                               '/func/*_task-postRest_acq-epi_rec-topup_bold_confounds.tsv',
                                               'pre_neutral_3_confounds.csv')
CONFOUNDS_DICT = dict()
CONFOUNDS_DICT['post_neutral_4'] = CONFOUNDS_NT('post_neutral_4',
                                               'confounds',
                                               '/func/*_task-postRest_acq-epi_rec-topup_bold_confounds.tsv',
                                               'pre_neutral_4_confounds.csv')


CONFOUNDS_DICT = dict()
CONFOUNDS_DICT['pre_heat_1'] = CONFOUNDS_NT('pre_heat_1',
                                               'confounds',
                                               '/func/*_task-preHeat1_acq-epi_rec-topup_bold_confounds.tsv',
                                               'pre_heat_1_confounds.csv')

CONFOUNDS_DICT = dict()
CONFOUNDS_DICT['pre_heat_2'] = CONFOUNDS_NT('pre_heat_2',
                                               'confounds',
                                               '/func/*_task-preHeat2_acq-epi_rec-topup_bold_confounds.tsv',
                                               'pre_heat_2_confounds.csv')
CONFOUNDS_DICT = dict()
CONFOUNDS_DICT['post_heat_3'] = CONFOUNDS_NT('post_heat_3',
                                               'confounds',
                                               '/func/*_task-postHeat3_acq-epi_rec-topup_bold_confounds.tsv',
                                               'post_heat_3_confounds.csv')
CONFOUNDS_DICT = dict()
CONFOUNDS_DICT['post_heat_4'] = CONFOUNDS_NT('post_heat_4',
                                               'confounds',
                                               '/func/*_task-postHeat4_acq-epi_rec-topup_bold_confounds.tsv',
                                               'post_heat_4_confounds.csv')


def _extract_confounds(in_filename, out_filename, confounds):
    """

    :param in_filename:
    :param out_filename:
    :param confounds:
    :return:
    """

    df_confounds = _read_confounds(in_filename, confounds)
    _write_confounds(df_confounds, out_filename)


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


def _find_file(glob_string, directory):

    glob_full_string = f'{directory}/{glob_string}'
    file_found = glob.glob(glob_full_string)

    if len(file_found) == 0:
        sys.exit(f'File not found. Revise glob string. \n {glob_full_string}')

    elif len(file_found) > 1:
        sys.exit(f'Found more than 1 file. Revise glob string. \n {glob_full_string}')

    return file_found[0]


def _create_full_output_filename(copy_to_directory, subject, session, out_filename):
    return os.path.join(copy_to_directory, f'sub-{subject}_ses-{session}_{out_filename}')


def _gather_confounds_file(gather,
                           subject,
                           session,
                           search_directory,
                           copy_to_directory=CONN_PATH,
                           confounds=CONFOUNDS):
    """

    :param gather:
    :param subject:
    :param session:
    :param search_directory:
    :param copy_to_directory:
    :param confounds:
    :return:
    """

    found_file = _find_file(gather.glob_string, search_directory)
    _extract_confounds(found_file, _create_full_output_filename(copy_to_directory, subject, session, gather.out_filename), confounds)

    return


def _gather_anat_file(gather,
                      subject,
                      session,
                      search_directory,
                      copy_to_directory=CONN_PATH,
                      ):
    """

    :param gather:
    :param search_directory:
    :param copy_to_directory:
    :param confounds:
    :return:
    """

    found_file = _find_file(gather.glob_string, search_directory)
    shutil.copy(found_file, _create_full_output_filename(copy_to_directory, subject, session, gather.out_filename))


def _gather_func_file(gather,
                      subject,
                      session,
                      search_directory,
                      copy_to_directory=CONN_PATH,
                      ):
    """

    :param gather:
    :param search_directory:
    :param copy_to_directory:
    :param confounds:
    :return:
    """

    func_found_file = _find_file(gather.func_glob_string, search_directory)
    mask_found_file = _find_file(gather.mask_glob_string, search_directory)
    output_file = _create_full_output_filename(copy_to_directory, subject, session, gather.out_filename)

    print('\n')
    print(func_found_file)
    print(mask_found_file)
    print(output_file)
    print('\n')

    masker = fsl.ApplyMask(in_file=func_found_file,
                           mask_file=mask_found_file,
                           out_file=output_file,
                           ignore_exception=True)

    masker.run()


def gather_anat_files(subject, session):

    for ii in ANAT_DICT.keys():
        print(ii)

        try:
            _gather_anat_file(ANAT_DICT[ii],
                              subject,
                              session,
                              SUBJECT_SESSION_PATH)

        except ValueError:
            print(f'Unknown key {ii}')


def gather_func_files(subject, session):
    for ii in FUNC_DICT.keys():
        try:
            _gather_func_file(FUNC_DICT[ii],
                              subject,
                              session,
                              SUBJECT_SESSION_PATH)

        except ValueError:
            print(f'Unknown key {ii}')


def gather_confounds_files(subject, session):
    for ii in CONFOUNDS_DICT.keys():
        try:
            _gather_confounds_file(CONFOUNDS_DICT[ii],
                                   subject,
                                   session,
                                   SUBJECT_SESSION_PATH)

        except ValueError:
            print(f'Unknown key {ii}')


def main():

    global SUBJECT_SESSION_PATH, ANAT_PATH, FUNC_PATH

    in_args = _argparse()

    SUBJECT_SESSION_PATH = os.path.join(FMRIPREP_PATH, f'sub-{in_args.subject}', f'ses-{in_args.session}')
    ANAT_PATH = os.path.join(SUBJECT_SESSION_PATH, 'anat')
    FUNC_PATH = os.path.join(SUBJECT_SESSION_PATH, 'func')

    _make_conn_directory()
    gather_anat_files(in_args.subject, in_args.session)
    gather_func_files(in_args.subject, in_args.session)
    gather_confounds_files(in_args.subject, in_args.session)



def _argparse():
    """ Get command line arguments.
    """

    parser = argparse.ArgumentParser(prog='processing_status')

    parser.add_argument('subject', help='Regular expression subject acrostic')

    parser.add_argument('-ss', '--session',
                        help='Regular expression session ',
                        type=str,
                        default='1')

    parser.add_argument('-v', '--verbose', help='Turn on verbose mode.',
                        action='store_true',
                        default=False)

    in_args = parser.parse_args()

    if in_args.session.lower() == 'none':
        in_args.session = None

    return in_args


if __name__ == '__main__':
    sys.exit(main())

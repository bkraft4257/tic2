#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script for gathering inputs for CONN
"""

import argparse
import os
import glob
import sys
import pandas
import tic_io
from tic_core import  operations
import pprint
from collections import namedtuple

import shutil
import nipype.interfaces.fsl as fsl  # fsl

YAML_CONFIG_FILENAME_DEFAULT = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'netprep_gather_inputs.yaml')

IMAGE_PROCESSING_PATH = os.path.join(os.getenv('ACTIVE_IMAGE_PROCESSING_PATH'))
FMRIPREP_PATH = os.path.join(os.getenv('ACTIVE_FMRIPREP_PATH'))
NETPREP_PATH = os.path.join(os.getenv('ACTIVE_NETPREP_PATH'))


def _make_directory(directory=NETPREP_PATH):
    """
    Make directory if it doesn't exist

    :param directory: A string or list of strings to create directory.  Each string must be an absolute or relative path.
    :return:
    """

    for ii in  operations.force_type_to_list(directory):

        try:
            if not os.path.exists(ii):
                os.makedirs(ii)

        except:
            sys.exit(f'Unable to make directory {ii}')

def _make_netprep_subject_input_directory(directory=NETPREP_PATH):
    """
    Make NETPREP directory if it doesn't exist

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


def _gather_confounds_file(func_dict,
                           search_directory,
                           output_filename,
                           confounds):
    """

    :param gather:
    :param subject:
    :param session:
    :param search_directory:
    :param copy_to_directory:
    :param confounds:
    :return:
    """

    found_file = _find_file(func_dict['base_glob_string'] + func_dict['confounds_glob_string'],
                                 search_directory)

    _extract_confounds(found_file, output_filename, confounds)

    return


def _gather_anat_file(gather,
                      search_directory,
                      out_filename,
                      ):
    """

    :param gather:
    :param search_directory:
    :param copy_to_directory:
    :param confounds:
    :return:
    """

    found_file = _find_file(gather['glob_string'], search_directory)
    shutil.copy(found_file, out_filename)


def _gather_func_file(func_dict,
                      search_directory,
                      output_file,
                      ):
    """

    :param func_dict:
    :param search_directory:
    :param output_file:
    :return:
    """
    func_found_file = _find_file(func_dict['base_glob_string'] + func_dict['func_glob_string'],
                                 search_directory)

    func_dict['mask_glob_string']

    if func_dict['mask_glob_string'] is not None:

        func_dict['mask_glob_string']

        mask_glob_string = func_dict['base_glob_string'] + func_dict['mask_glob_string']

        mask_found_file = _find_file(mask_glob_string, search_directory)

        masker = fsl.ApplyMask(in_file=func_found_file,
                               mask_file=mask_found_file,
                               out_file=output_file,
                               ignore_exception=True)
        print(masker.cmdline)

        masker.run()

    else:
        shutil.copy(func_found_file, _create_full_output_filename(copy_to_directory, subject, session, gather.out_filename, ))


def gather_anat_files(anat_dict, subject, session):
    """
    Search for files matching glob_string and copy to a directory with a different name
    :param anat_dict:
    :param subject:
    :param session:
    :return:
    """

    for ii in anat_dict.keys():
        try:
            _gather_anat_file(anat_dict[ii],
                              SUBJECT_SESSION_PATH,
                              _create_full_output_filename(CONN_PATH, subject, session, f'{ii}.nii.gz')
                              )
        except ValueError:
            print(f'Unknown key {ii}')


def gather_func_files(func_dict, subject, session, confounds):
    for ii in func_dict.keys():
        try:
            _gather_func_file(func_dict[ii],
                              SUBJECT_SESSION_PATH,
                              _create_full_output_filename(CONN_PATH, subject, session, f'{ii}.nii.gz')
                              )

        except ValueError:
            print(f'Unknown key {ii}')


        try:
            _gather_confounds_file(func_dict[ii],
                                   SUBJECT_SESSION_PATH,
                                   _create_full_output_filename(CONN_PATH, subject, session, f'{ii}.csv'),
                                   confounds
                                   )

        except ValueError:
            print(f'Unknown key {ii}')


def gather_confounds_files(func_dict,
                           search_directory,
                           output_file,
                           confounds):

    for ii in func_dict.keys():
        try:
            _gather_confounds_file(func_dict[ii],
                                   search_directory,
                                   output_file,
                                   confounds,)

        except ValueError:
            print(f'Unknown key {ii}')


def main():
    global SUBJECT_SESSION_PATH, ANAT_PATH, FUNC_PATH

    in_args = _argparse()

    SUBJECT_SESSION_PATH = os.path.join(FMRIPREP_PATH, f'sub-{in_args.subject}', f'ses-{in_args.session}')
    NETPREP_INPUT_PATH = os.path.join(SUBJECT_SESSION_PATH, 'netprep', f'sub-{in_args.subject}', f'ses-{in_args.session}', 'input')

    ANAT_PATH = os.path.join(SUBJECT_SESSION_PATH, 'anat')
    FUNC_PATH = os.path.join(SUBJECT_SESSION_PATH, 'func')

    _make_directory(NETPREP_INPUT_PATH)

    netprep_config = tic_io.read_yaml(in_args.yaml_filename, in_args.verbose)

    return


def _argparse():
    """ Get command line arguments.
    """

    parser = argparse.ArgumentParser(prog='netprep_gather_inputs')

    parser.add_argument('subject', help='BIDS subject value')

    parser.add_argument('-ss', '--session',
                        help='BIDS session value',
                        type=str,
                        default='1')

    parser.add_argument('--yaml_filename', help='YAML configuration file',
                        default=YAML_CONFIG_FILENAME_DEFAULT)

    parser.add_argument('-v', '--verbose', help='Turn on verbose mode.',
                        action='store_true',
                        default=False)

    in_args = parser.parse_args()

    if in_args.session.lower() == 'none':
        in_args.session = None

    return in_args


if __name__ == '__main__':
    sys.exit(main())

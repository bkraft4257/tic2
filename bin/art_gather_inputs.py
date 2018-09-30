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

    for ii in operations.force_type_to_list(directory):

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


def gather_func_file(func_dict,
                     fmriprep_subject_session_func_path,
                     art_input_path,
                     ):
    """

    :param func_dict:
    :param fmriprep_subject_session_func_path:
    :param art_input_path:
    :return:
    """

    func_found_file = _find_file(func_dict['func_glob_string'], fmriprep_subject_session_func_path)
    output_file = os.path.join(art_input_path, func_dict['func_out_filename'])

    _copy_files(func_found_file, output_file)

    return


def _copy_files(source_file, target_file):

    #print(source_file)
    #print(target_file)

    shutil.copy(source_file,target_file)


def main():

    in_args = _argparse()

    fmriprep_subject_session_path = os.path.join(FMRIPREP_PATH, f'sub-{in_args.subject}', f'ses-{in_args.session}')
    art_subject_session_path = os.path.join(NETPREP_PATH, f'sub-{in_args.subject}', f'ses-{in_args.session}')

    _make_directory(art_subject_session_path)

    config = tic_io.read_yaml(in_args.yaml_filename)

    if in_args.verbose:
        print('\n\n')

    for keys, func_config in config.items():

        netprep_input_path = os.path.join(art_subject_session_path, func_config['input_dir'])
        _make_directory(netprep_input_path)

        # Copy functional files and apply mask when mask is found
        gather_func_file(func_config,
                         fmriprep_subject_session_path,
                         netprep_input_path,)

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

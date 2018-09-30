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


def _extract_confounds(found_file, output_filename, confounds_to_extract):
    """

    :param found_file:
    :param output_filename:
    :param confounds_to_extract:
    :return:
    """

    shutil.copy(found_file, output_filename)


KEEP_COLUMNS = ['tCompCor00', 'tCompCor01', 'tCompCor02', 'tCompCor03', 'tCompCor04', 'tCompCor05',
                'X', 'Y', 'Z', 'RotX', 'RotY', 'RotZ']


def _extract_confounds(in_filename, out_filename, keep_columns=KEEP_COLUMNS):
    in_df = pandas.read_csv(in_filename, sep='\t')
    out_df = in_df[keep_columns]
    out_df.to_csv(out_filename)

    return out_df


def _gather_confounds_file(func_dict,
                           fmriprep_subject_session_path,
                           netprep_input_path,
                           confounds_to_be_extracted):
    """

    :param func_dict:
    :param fmriprep_subject_session_path:
    :param netprep_input_path:
    :return:
    """

    found_file = _find_file(func_dict['base_glob_string'] + func_dict['confounds_glob_string'],
                            fmriprep_subject_session_path)

    output_filename = os.path.join(netprep_input_path, func_dict['confounds_out_filename'])

    _extract_confounds(found_file, output_filename, confounds_to_be_extracted)

    return


def _gather_anat_file(gather,
                       fmriprep_subject_session_anat_path,
                       netprep_input_path
                      ):
    """

    :param gather:
    :param fmriprep_subject_session_anat_path:
    :param netprep_input_path:
    :return:
    """

    found_file = _find_file(gather['glob_string'], fmriprep_subject_session_anat_path)
    out_file = os.path.join(netprep_input_path, gather['out_filename'])

    print(found_file)
    print(gather['out_filename'])

    shutil.copy(found_file, out_file)


def gather_func_file(func_dict,
                      fmriprep_subject_session_func_path,
                      netprep_input_path,
                      ):
    """

    :param func_dict:
    :param search_directory:
    :param output_file:
    :return:
    """
    func_found_file = _find_file(func_dict['base_glob_string'] + func_dict['func_glob_string'],
                                 fmriprep_subject_session_func_path)

    output_file = os.path.join(netprep_input_path, func_dict['func_out_filename'])

    if func_dict['mask_glob_string'] is not None:

        mask_glob_string = func_dict['base_glob_string'] + func_dict['mask_glob_string']

        mask_found_file = _find_file(mask_glob_string, fmriprep_subject_session_func_path)

        masker = fsl.ApplyMask(in_file=func_found_file,
                               mask_file=mask_found_file,
                               out_file=output_file,
                               ignore_exception=True)
        print(masker.cmdline)

        masker.run()

    else:
        shutil.copy(func_found_file, output_file)


def gather_anat_files(anat_dict, fmriprep_subject_session_path, netprep_input_path,):
    """
    Search for files matching glob_string and copy to a directory with a different name
    :param anat_dict:
    :param fmriprep_subject_session_path:
    :param netprep_input_path:
    :return:
    """

    for key, value in anat_dict.items():
        try:
            _gather_anat_file(value, fmriprep_subject_session_path, netprep_input_path)
        except ValueError:
            print(f'Unknown key {ii}')



def main():
    global SUBJECT_SESSION_PATH, FMRIPREP_ANAT_PATH, FMRIPREP_FUNC_PATH, NETPREP_SUBJECT_SESSION_INPUT_PATH

    in_args = _argparse()

    fmriprep_subject_session_path = os.path.join(FMRIPREP_PATH, f'sub-{in_args.subject}', f'ses-{in_args.session}')
    netprep_subject_session_path = os.path.join(NETPREP_PATH, f'sub-{in_args.subject}', f'ses-{in_args.session}')

    FMRIPREP_ANAT_PATH = os.path.join(fmriprep_subject_session_path, 'anat')
    FMRIPREP_FUNC_PATH = os.path.join(fmriprep_subject_session_path, 'func')

    SUBJECT_SESSION_PATH = fmriprep_subject_session_path

    _make_directory(netprep_subject_session_path)

    netprep_config = tic_io.read_yaml(in_args.yaml_filename, in_args.verbose)

    for keys, func_config in netprep_config['func'].items():

        netprep_input_path = os.path.join(netprep_subject_session_path, func_config['input_dir'])
        _make_directory(netprep_input_path)

        # Copy T1w and MNI GM Tissue Probability to each func input directory.
        # This is insufficient but provides the greatest flexibility and easiest to program. Thes
        # could be replaced with
        gather_anat_files(netprep_config['anat'],
                          fmriprep_subject_session_path,
                          netprep_input_path)

        # Copy functional files and apply mask when mask is found
        gather_func_file(func_config,
                         fmriprep_subject_session_path,
                         netprep_input_path)

        # Extract confounds calculated wth fmriprep and copy to netprep input.

        _gather_confounds_file(func_config,
                               fmriprep_subject_session_path,
                               netprep_input_path,
                               netprep_config['func_confounds'])


    # Copy netprep template

    input_file = os.path.join()
    output_file = os.path.join(netprep_input_path, netprep_config['netprep_template'])
    shutil.copy(netprep_input_path)

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

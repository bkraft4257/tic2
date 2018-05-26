#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Clean bids directory.
"""

import argparse
import glob
import os
import sys

ACTIVE_BIDS_PATH = os.environ['ACTIVE_BIDS_PATH']


def _argparse():
    """ Get command line arguments.
    """

    parser = argparse.ArgumentParser(prog='clean_bids')

    parser.add_argument('subject', help='BIDS subject value')

    parser.add_argument('-ss', '--session',
                        help='BIDS session value',
                        type=str,
                        default='1')

    parser.add_argument('-v', '--verbose', help='Turn on verbose mode.',
                        action='store_true',
                        default=False)

    in_args = parser.parse_args()

    if in_args.session.lower() == 'none':
        in_args.session = None

    return in_args


def _list_hdc_item_number_2(start_directory=None):

    if start_directory is None:
        start_directory = '.'

    files = []
    for ext in ('nii.gz', 'json'):
        glob_string = os.path.join(f'{start_directory}', '**', '**', f'*.[0-9].{ext}')
        files.extend(glob.glob(glob_string, recursive=True))

    if len(files) > 0:
        print('\nList of repeated scans.')
        print('If repeated scans are found you must CHOOSE which files you want to use for processing.')
        print('-------------------------------------------------------------------------------------\n')

        for ii, ii_file in enumerate(files):
            print(f'{ii}) {ii_file}')

        print('\n')


def _rename_hdc_item_number_1(start_directory=None):
    """

    :param start_directory:
    :return:
    """

    if start_directory is None:
        start_directory = '.'

    files = []
    for ext in ('nii.gz', 'json'):
        glob_string = os.path.join(f'{start_directory}', '**', '**', f'*.1.{ext}')
        files.extend(glob.glob(glob_string, recursive=True))

    for ii, ii_file in enumerate(files):
        try:
            os.rename(ii_file,
                      ii_file.replace('.1.', '.')
                      )
        except FileNotFoundError:
            pass  # Ignore file not found errors


def _rename_hdc_item_number_1(start_directory=None):
    """

    :param start_directory:
    :return:
    """

    if start_directory is None:
        start_directory = '.'

    files = []
    for ext in ('nii.gz', 'json'):
        glob_string = os.path.join(f'{start_directory}', '**', '**', f'*.1.{ext}')
        files.extend(glob.glob(glob_string, recursive=True))

    for ii, ii_file in enumerate(files):
        try:
            os.rename(ii_file,
                      ii_file.replace('.1.', '.')
                      )
        except FileNotFoundError:
            pass  # Ignore file not found errors


def _remove_backup_files(start_directory=None):

    if start_directory is None:
        start_directory = '.'

    files = []
    for ii_glob_pattern in ['*~']:
        glob_string = os.path.join(f'{start_directory}', '**', ii_glob_pattern)
        files.extend(glob.glob(glob_string, recursive=True))

    for ii, ii_file in enumerate(files):
        os.remove(ii_file)


def main():

    in_args = _argparse()

    start_directory = os.path.abspath(os.path.join(ACTIVE_BIDS_PATH,
                                                   f'sub-{in_args}',
                                                   f'ses-{in_args.session}'
                                                   )
                                      )

    print(start_directory)

    _rename_hdc_item_number_1(start_directory)
    _remove_backup_files(start_directory)
    _list_hdc_item_number_2(start_directory)


if __name__ == '__main__':
    sys.exit(main())

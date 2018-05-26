#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Clean bids directory.
"""

import argparse
import glob
import os
import sys
import stat

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

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-l', '--lock', help='Disable write permission to *.nii.gz and *.json files',
                       action='store_true',
                       default=False)

    group.add_argument('-u', '--unlock', help='Enable write permission to *.nii.gz and *.json files',
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


def _remove_files(start_directory=None):

    if start_directory is None:
        start_directory = '.'

    files = []
    for ii_glob_pattern in ['*~', '*magnitude1.json']:
        glob_string = os.path.join(f'{start_directory}', '**', ii_glob_pattern)
        files.extend(glob.glob(glob_string, recursive=True))

    for ii, ii_file in enumerate(files):
        os.remove(ii_file)


def _set_write_permissions_of_file(file, lock=True):
    """Remove write permissions from this path, while keeping all other permissions intact.

    Params:
        path:  The path whose permissions to alter.
    """

    current_permissions = stat.S_IMODE(os.lstat(file).st_mode)

    if lock:
        set_writing = ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH
        os.chmod(file, current_permissions & set_writing)

    else:
        set_writing = stat.S_IWUSR & stat.S_IWGRP & stat.S_IWOTH
        os.chmod(file, current_permissions | set_writing)

    print(f'{file}: {current_permissions}, {set_writing}, {current_permissions & set_writing}')




def get_files(start_directory, file_glob_strings):
    files = []
    for ext in file_glob_strings:
        glob_string = os.path.join(f'{start_directory}', '**',  ext)
        files.extend(glob.glob(glob_string, recursive=True))

    return files


def set_write_permissions(start_directory, lock=True):

    files = get_files(start_directory, ['*.nii.gz', '*.json'])

    for ii_file in files:
        _set_write_permissions_of_file(ii_file, lock=lock)


def main():

    in_args = _argparse()

    start_directory = os.path.abspath(os.path.join(ACTIVE_BIDS_PATH,
                                                   f'sub-{in_args.subject}',
                                                   f'ses-{in_args.session}'
                                                   )
                                      )

    print(in_args)

    _rename_hdc_item_number_1(start_directory)
    _remove_files(start_directory)
    _list_hdc_item_number_2(start_directory)

    if in_args.lock:
        set_write_permissions(start_directory, lock=True)

    if in_args.unlock:
        set_write_permissions(start_directory, lock=False)


if __name__ == '__main__':
    sys.exit(main())

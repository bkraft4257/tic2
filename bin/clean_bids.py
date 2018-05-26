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

from collections import Iterable


ACTIVE_BIDS_PATH = os.environ['ACTIVE_BIDS_PATH']


def force_to_list(inp, basetype=int):
    """

    :param inp:
    :param basetype:
    :return:

    https://stackoverflow.com/questions/20095244/how-do-i-check-if-input-is-a-number-in-python
    """

    if not isinstance(inp, Iterable) or isinstance(inp, basetype):
        out_list = [inp]  # use just `str` in py3.x
    else:
        out_list = [x for x in inp]

#    for item in inp:  # use `yield from inp` in py3.x
#        yield item

    return out_list

def _argparse():
    """ Get command line arguments.
    """

    parser = argparse.ArgumentParser(prog='clean_bids')

    parser.add_argument('-s', '--subject', help='BIDS subject value',
                        nargs='*',
                        type=str,
                        default=None)

    parser.add_argument('-ss', '--session',
                        help='BIDS session value',
                        nargs='*',
                        type=str,
                        default=['1'])

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
        glob_string = os.path.join(f'{start_directory}', '**', f'*.1.{ext}')
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
        set_writing = ~stat.S_IWUSR & ~stat.S_IWGRP
        os.chmod(file, current_permissions & set_writing)

    else:
        set_writing = stat.S_IWUSR | stat.S_IWGRP
        os.chmod(file, current_permissions | set_writing)


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


def _clean_bids(start_directory, lock, unlock):

    print(start_directory)
    _rename_hdc_item_number_1(start_directory)
    _remove_files(start_directory)
    _list_hdc_item_number_2(start_directory)

    if lock:
        set_write_permissions(start_directory, lock=True)

    if unlock:
        set_write_permissions(start_directory, lock=False)


def main():

    in_args = _argparse()

    print(in_args.subject)
    print(in_args.sessions)

    subjects = force_to_list(in_args.subject, 'str')
    sessions = force_to_list(in_args.sessions, 'str')

    for ii_subject in subjects:

        if ii_subject is None:
            start_directory = ACTIVE_BIDS_PATH
            _clean_bids(start_directory, in_args.lock, in_args.unlock)

        else:
            for ii_session in sessions:
                start_directory = os.path.abspath(os.path.join(ACTIVE_BIDS_PATH,
                                                               f'sub-{ii_subject}',
                                                               f'ses-{ii_session}'
                                                               )
                                                  )
                _clean_bids(start_directory, in_args.lock, in_args.unlock)


if __name__ == '__main__':
    sys.exit(main())

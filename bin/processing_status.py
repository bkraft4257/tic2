#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Check for the existence of a file and report if it is found or not found by study acrostic.
"""

import glob
import os
import argparse
import sys
import pandas

# TODO Study Choices should be a common variable that is imported.


def get_active_study_bids_path():
    return os.getenv('ACTIVE_BIDS_PATH')


ACROSTIC_LIST_FILENAME = 'acrostic.list'
ACTIVE_BIDS_PATH = get_active_study_bids_path()


def get_acrostic_study_list_full_filename(active_study_bids_path=ACTIVE_BIDS_PATH,
                                          acrostic_list_name=ACROSTIC_LIST_FILENAME):

    return os.path.abspath(os.path.join(active_study_bids_path, acrostic_list_name))


def get_acrostic_list():
    acrostic_list_filename = get_acrostic_study_list_full_filename()

    print(acrostic_list_filename)

    df_acrostic_list = pandas.read_csv(acrostic_list_filename)

    print(df_acrostic_list)

    return df_acrostic_list

def _argparse():
    """ Get command line arguments.

    """
    parser = argparse.ArgumentParser(prog='processing_status')

    parser.add_argument('file_pattern', help='String file pattern to glob')

    parser.add_argument("-r", "--recursive", help="Recursive boolean flag for glob",
                        action="store_true",
                        default=False)

    return parser.parse_args()


def main():

    in_args = _argparse()

    files = glob.glob(in_args.file_pattern,
                      recursive=in_args.recursive)

    print(get_acrostic_study_list_full_filename())

    get_acrostic_list()

    for ii,ii_files in enumerate(files):
        print(f'{ii}) {ii_files}')

    return


# ====================================================================================================================
# region Command Line Interface

if __name__ == '__main__':
    sys.exit(main())

# endregion

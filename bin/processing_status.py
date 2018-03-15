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
import re

pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
pandas.set_option('display.max_colwidth',200)

# TODO Study Choices should be a common variable that is imported.


def get_active_study_bids_path():
    return os.getenv('ACTIVE_BIDS_PATH')


ACROSTIC_LIST_FILENAME = 'acrostic.list'
ACTIVE_BIDS_PATH = get_active_study_bids_path()


def get_acrostic_study_list_full_filename(active_study_bids_path=ACTIVE_BIDS_PATH,
                                          acrostic_list_name=ACROSTIC_LIST_FILENAME):

    return os.path.abspath(os.path.join(active_study_bids_path, acrostic_list_name))


def get_acrostic_list(acrostic_list_filename = get_acrostic_study_list_full_filename()):
    df_acrostic_list = pandas.read_csv(acrostic_list_filename, header=None)
    df_acrostic_list.columns = ['subject']
    return df_acrostic_list


def get_key_value_from_string(string, acrostic_regex, key_value_split_on='-'):

    m = re.search(acrostic_regex, string)

    if m:
        key,value =m.group(0).split(key_value_split_on)
    else:
        key = None
        value = None

    return key, value


def _argparse():
    """ Get command line arguments.

    """
    parser = argparse.ArgumentParser(prog='processing_status')

    parser.add_argument('file_pattern', help='String file pattern to glob')

    parser.add_argument("-s", "--subject", help="Regular expression subject acrostic",
                        default='sub-imove[0-9]{4}')

    parser.add_argument("-ss", "--session", help="Regular expression session ",
                        default='ses-[0-9]')

    parser.add_argument("-a", "--acrostic_list", help="Acrostic List",
                        default=get_acrostic_study_list_full_filename())

    parser.add_argument("-r", "--recursive", help="Recursive boolean flag for glob",
                        action="store_true",
                        default=False)

    return parser.parse_args()


def display(in_df):

    print(in_df)
    print(f'subject,session,file')

    for row in in_df.itertuples():
        print(row)
        #print(f'{row[0]}, {row[1]} ,{row[2]}')


def main():

    in_args = _argparse()

    files = glob.glob(in_args.file_pattern,
                      recursive=in_args.recursive)

    df_acrostic_list = get_acrostic_list(in_args.acrostic_list)

    df_files = pandas.DataFrame(columns=["subject", "session", "file"])

    for ii, ii_file in enumerate(files):
        _, subject_value = get_key_value_from_string(ii_file, in_args.subject)
        _, session_value = get_key_value_from_string(ii_file, in_args.session)

        df_files = df_files.append({"subject": subject_value,
                                    "session": session_value,
                                    "file": ii_file
                                    }, ignore_index=True)

    df_full_list = df_acrostic_list.merge(df_files, how='left', on='subject')

    display(df_full_list)

    return


# ====================================================================================================================
# region Command Line Interface

if __name__ == '__main__':
    sys.exit(main())

# endregion

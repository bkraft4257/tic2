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
from colorama import Fore

pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
pandas.set_option('display.max_colwidth',200)

# TODO Study Choices should be a common variable that is imported.


ACROSTIC_LIST_FILENAME = 'acrostic.csv'
ACTIVE_BIDS_PATH = os.getenv('ACTIVE_BIDS_PATH')


def get_acrostic_study_list_full_filename(active_study_bids_path=ACTIVE_BIDS_PATH,
                                          acrostic_list_name=ACROSTIC_LIST_FILENAME):

    return os.path.abspath(os.path.join(active_study_bids_path, acrostic_list_name))


def get_acrostic_list(acrostic_list_filename = get_acrostic_study_list_full_filename()):
    df_acrostic_list = (pandas.read_csv(acrostic_list_filename)
                        .rename(columns={'participant_id': 'subject'})
                        .set_index('subject')
                        )

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

    parser.add_argument("--acrostic_session",
                        help="Acrostic Session",
                        default=1
                        )

    parser.add_argument("-a", "--acrostic_list", help="Acrostic List",
                        default=get_acrostic_study_list_full_filename())

    parser.add_argument("--glob_current_directory_only", help="Recursive boolean flag for glob",
                        action="store_true",
                        default=False)

    parser.add_argument("-H", "--noheader", help="Remove header from output",
                        action="store_true",
                        default=False)

    parser.add_argument("--subject_only", help="Only display subject",
                        action="store_true",
                        default=False)

    parser.add_argument("--summary", help="Display summary stats",
                        action="store_true",
                        default=False)

    parser.add_argument("--nan", help="Remove NaNs from output",
                        choices=['drop', 'only', 'ignore'],
                        default='ignore')

    return parser.parse_args()


def display(in_df, subject_only=False, noheader=False):

    if not noheader and not subject_only:
        print(f'index,subject,session,file')

    for row in in_df.itertuples():

        if subject_only:
            print(f'{row[1]}')
        else:
            print(f'{row[0]},{row[1]},{row[2]},{row[3]}')


def _clean_nan(in_df, nan_option, nan_fill='not_found'):

    if nan_option == 'drop':
        out_df = in_df.dropna(axis=0).copy()

    elif nan_option == 'only':
        out_df = in_df[in_df.isna().any(axis=1)].copy()

    else:
        out_df = in_df.fillna(nan_fill).copy()

    return out_df


def main():

    in_args = _argparse()

    files = glob.glob(in_args.file_pattern,
                      recursive=not in_args.glob_current_directory_only)

    df_acrostic_list = get_acrostic_list(in_args.acrostic_list)

    print(df_acrostic_list)

    df_files = pandas.DataFrame(columns=["subject", "session", "file"])

    for ii, ii_file in enumerate(files):
        _, subject_value = get_key_value_from_string(ii_file, in_args.subject)
        _, session_value = get_key_value_from_string(ii_file, in_args.session)

        df_files = df_files.append({"subject": subject_value,
                                    "session": session_value,
                                    "file": ii_file
                                    }, ignore_index=True)

    df_full_list = df_acrostic_list.reset_index().merge(df_files, how='left', on='subject')

    print(df_full_list)

    display(df_full_list.pipe(_clean_nan, nan_option=in_args.nan),
            subject_only=in_args.subject_only,
            noheader=in_args.noheader)

    if in_args.summary:

        n_acrostics = len(df_acrostic_list)
        n_rows = len(df_full_list)
        n_rows_with_na = len(df_full_list.dropna())

        if n_rows_with_na < n_rows:
            print(f'{Fore.RED}\nMissing files {n_acrostics-n_rows_with_na}.\n')

        elif n_acrostics < n_rows:
            print(f'{Fore.RED}\nAdditional file(s) found {n_rows-n_acrostics}.\n')

        else:
            print(f'{Fore.GREEN}\nOne file found for each acrostic.\n')

    return


# ====================================================================================================================
# region Command Line Interface


if __name__ == '__main__':
    sys.exit(main())

# endregion

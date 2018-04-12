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

import tic_core.ops as ops

pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
pandas.set_option('display.max_colwidth',200)


# TODO Study Choices should be a common variable that is imported.


ACROSTIC_LIST_FILENAME = 'acrostic.csv'
ACTIVE_BIDS_PATH = os.getenv('ACTIVE_BIDS_PATH')
ACTIVE_ACROSTIC_REGEX = os.getenv('ACTIVE_ACROSTIC_REGEX')


def get_acrostic_study_list_full_filename(active_study_bids_path=ACTIVE_BIDS_PATH,
                                          acrostic_list_name=ACROSTIC_LIST_FILENAME):

    return os.path.abspath(os.path.join(active_study_bids_path, acrostic_list_name))


def get_acrostic_list(acrostic_list_filename = get_acrostic_study_list_full_filename()):

    try:
        df_acrostic_list = (pandas.read_csv(acrostic_list_filename)
                            .rename(columns={'participant_id': 'subject'})
                            .set_index('subject')
                            )
    except FileNotFoundError:
        print('File Not Found Error')

    return df_acrostic_list


def get_key_value_from_string(string,
                              acrostic_regex,
                              key_value_split_on=ops.BIDS_KEY_VALUE_SPLIT_ON):

    m = re.search(acrostic_regex, string)

    if m:
        key,value =m.group(0).split(key_value_split_on)
    else:
        key = None
        value = None

    return key, value


def _add_prefix_to_bids_key_value_if_necessary(in_key_value, bids_key, bids_delimiter='-'):
    """
    Add BIDS KEY if it doesn't exist.  Key should not contain the BIDS delimiter.

    :param in_key_value:
    :param bids_key:
    :return:

    """

    if in_key_value[0:4] == bids_key + bids_delimiter:
        out_key_value = in_key_value

    else:
        out_key_value = bids_key + bids_delimiter + in_key_value

    return out_key_value


def _argparse():
    """ Get command line arguments.

    """
    parser = argparse.ArgumentParser(prog='processing_status')

    parser.add_argument('file_pattern', help='String file pattern to glob')

    parser.add_argument('-s', '--subject', help='Regular expression subject acrostic',
                        default='sub-imove[0-9]{4}')

    parser.add_argument('-ss', '--session', help='Regular expression session ',
                        default='ses-[0-9]')

    parser.add_argument('-a', '--acrostic_list', help='Acrostic List',
                        default=get_acrostic_study_list_full_filename())

    parser.add_argument('--glob_current_directory_only', help='Recursive boolean flag for glob',
                        action='store_true',
                        default=False)

    parser.add_argument('-v', '--verbose', help='Turn on verbose mode.',
                        action='store_true',
                        default=False)

    parser.add_argument('-H', '--noheader', help='Remove header from output',
                        action='store_true',
                        default=False)

    parser.add_argument('--subject_only', help='Only display subject',
                        action='store_true',
                        default=False)

    parser.add_argument('--summary', help='Display summary stats',
                        action='store_true',
                        default=False)

    parser.add_argument('--nan', help='Remove NaNs from output',
                        choices=['drop', 'only', 'ignore'],
                        default='ignore')

    parser.add_argument('--display_group', help='Display files that were found, missing, or both. Default is both.',
                        choices=['found', 'missing', 'both'],
                        default='both')

    parser.add_argument('--drop_missing', help='Drop files that were found from list.',
                        action='store_true',
                        default=False)

    return parser.parse_args()


def filter_rows(in_df, display_group='both'):

    all_columns = list(in_df.columns.values)
    r = re.compile('.*_processed$')
    search_columns = list(filter(r.match, all_columns))
    
    keep_rows= in_df[search_columns].any(axis=1)

    if display_group == 'found':
        out_df = in_df[ keep_rows ].copy()

    elif display_group == 'missing':
        out_df = in_df[ ~keep_rows ].copy()

    else:
        out_df = in_df.copy()

    return out_df


def _display(in_df,
             display_group='both',
             subject_only=False,
             noheader=False,
             ):

    out_df = filter_rows(in_df, display_group=display_group)

    if subject_only:
        out_df = out_df['subject'].copy()

    print(out_df.to_string(index=False,
                           header=(not noheader)))


def _clean_nan(in_df, nan_option, nan_fill='not_found'):

    if nan_option == 'drop':
        out_df = in_df.dropna(axis=0).copy()

    elif nan_option == 'only':
        out_df = in_df[in_df.isna().any(axis=1)].copy()

    else:
        out_df = in_df.fillna(nan_fill).copy()

    return out_df


def _rename_acrostic_list(in_df):
    return in_df.rename(columns=lambda x: re.sub(r'(ses-\d)',r'\1_scanned',x))


def _get_subject_and_session_from_filenames(files, 
                                            subject_acrostic_regex, 
                                            session_acrostic_regex, 
                                            verbose=False):

    df_files = pandas.DataFrame(columns=['subject', 'session', 'file'])

    for ii, ii_file in enumerate(files):
        _, subject_value = get_key_value_from_string(ii_file, subject_acrostic_regex)
        _, session_value = get_key_value_from_string(ii_file, session_acrostic_regex)

        df_files = df_files.append({'subject': subject_value,
                                    'session': session_value,
                                    'file': ii_file
                                    }, ignore_index=True)

    # If a person is not careful with their regular expression a file can be found that does 
    # not contain the subject and session in the filename.  When this happens discard those
    # files.  It would be nice if a warning was issues. 

    if verbose:
        print('\n List of files found with subject and session information before cleaning.\n')
        print(df_files)
        print('\n\n')

    # Remove files that do not have a subject_value or session value.  There is no need to save
    # these because they are not the files you are looking for.   If they are you shouldn't be 
    # using this function.

    df_files = df_files.dropna(subset=['subject', 'session'],axis=0)

    return df_files


def main():

    in_args = _argparse()

    files = glob.glob(in_args.file_pattern,
                      recursive=not in_args.glob_current_directory_only)

    if len(files) == 0:
        print(f'No files were found given with your glob string {in_args.file_pattern}')
        sys.exit()

    df_acrostic_list = get_acrostic_list(in_args.acrostic_list)

    subject_key_value = _add_prefix_to_bids_key_value_if_necessary(in_args.subject, 'sub')
    session_key_value = _add_prefix_to_bids_key_value_if_necessary(in_args.session, 'ses')

    df_files = _get_subject_and_session_from_filenames(files,
                                                       subject_key_value,
                                                       session_key_value,
                                                       in_args.verbose)

    try:
        df_files_2 = df_files.set_index(['subject', 'session']).unstack()
        df_files_2.columns = [f'ses-{x+1}_processed' for x in range(len(df_files_2.columns))]

    print(df_files_2)

    except ValueError:
        print(f'\n{Fore.RED}Unable to stack. {Fore.WHITE}\n')
        print(df_files)
        print('\n\n')

        print(df_files.groupby(['subject', 'session']).file.count())
        print('\n\n')
        sys.exit()

    df_full_list = (_rename_acrostic_list(df_acrostic_list)
                    .reset_index()
                    .merge(df_files_2.reset_index(), how='left', on='subject')
                    .fillna(False)
                    )

    _display(df_full_list.pipe(_clean_nan,
                               nan_option=in_args.nan),
             display_group=in_args.display_group,
             subject_only=in_args.subject_only,
             noheader=in_args.noheader,
             )

    if in_args.summary:

        n_acrostics = len(df_acrostic_list)
        n_rows = len(df_full_list)
        n_rows_with_na = len(df_full_list.dropna())

        if n_rows_with_na < n_rows:
            print(f'{Fore.RED}\nFAIL: {Fore.WHITE}Missing files {n_acrostics-n_rows_with_na}.\n')

        elif n_acrostics < n_rows:
            print(f'{Fore.RED}\n FAIL: {Fore.WHITE}Additional file(s) found {n_rows-n_acrostics}.\n')

        else:
            print(f'{Fore.GREEN}\nPASS: {Fore.WHITE}One file found for each acrostic.\n')

    return


# ====================================================================================================================
# region Command Line Interface


if __name__ == '__main__':
    sys.exit(main())

# endregion

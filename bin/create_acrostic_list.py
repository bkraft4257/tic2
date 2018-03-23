#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create an acrostic list. Row is the acrostic.  Column is the session.
"""

import os
import pandas
import glob
import argparse
import sys

ACTIVE_BIDS_PATH = os.getenv('ACTIVE_BIDS_PATH')
ACROSTIC_BASE_FILENAME = 'acrostic'


def _argparse():
    """ Get command line arguments.

    """
    parser = argparse.ArgumentParser(prog='processing_status')

    parser.add_argument("-v", "--verbose", help="Display acrostic list",
                        action="store_true",
                        default=False)

    parser.add_argument("-s", "--summary", help="Display acrostic summary by session.",
                        action="store_true",
                        default=False)

    parser.add_argument('-o', '--out_base_filename',
                        help=f'Output filename.  default={ACROSTIC_BASE_FILENAME}',
                        default=ACROSTIC_BASE_FILENAME,
                        )

    return parser.parse_args()


def main():

    in_args = _argparse()

    df0 = pandas.DataFrame({'directory': glob.glob(os.path.join(ACTIVE_BIDS_PATH, 'sub-*', 'ses-*'))})
    df0.directory = df0.directory.str.replace(ACTIVE_BIDS_PATH, '')
    df = df0.directory.str.split('/', expand=True).copy()

    df.columns = ['index', 'subject', 'session']
    df.subject = df.subject.str.replace('sub-', '')
    # df.session = df.session.str.replace('ses-', '')

    df = df.drop('index', axis=1)
    df['acquired'] = True

    df = df.set_index(['subject', 'session']).unstack().fillna(False)
    df.columns = df.columns.get_level_values(1)

    acrostic_csv_default_filename = os.path.join(ACTIVE_BIDS_PATH, f'{in_args.out_base_filename}.csv')
    acrostic_list_default_filename = os.path.join(ACTIVE_BIDS_PATH, f'{in_args.out_base_filename}.list')

    df.to_csv(acrostic_csv_default_filename)
    df.reset_index()['subject'].to_csv(acrostic_list_default_filename, header=False, index=False)

    if in_args.verbose:
        print(df)

        if in_args.summary:
            print('\n\nSummary of Subjects by Session\n')
            print(df.apply(pandas.value_counts).fillna(0).astype(int))

# ====================================================================================================================
# region Command Line Interface


if __name__ == '__main__':

    sys.exit(main())

# endregion

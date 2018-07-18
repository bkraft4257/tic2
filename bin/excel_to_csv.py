#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Converts an Excel file to a CSV file.
"""

import pandas
import argparse
import sys


def excel_to_csv(in_filename, verbose=False):

    out_filename = in_filename.replace('xlsx', 'csv')

    if verbose:
        print(f'Converting {in_filename} to {out_filename}')

    df_xlsx = pandas.read_excel(in_filename)
    df_csv = df_xlsx.copy()

    for ii in [1, 2]:
        df_csv.iloc[ii, 0:11] = df_csv.iloc[0, 0:11]

    df_csv.to_csv(out_filename, index=False)


def _argparse():
    """ Get command line arguments.

    """
    parser = argparse.ArgumentParser(prog='excel_to_csv')

    parser.add_argument('excel_files', nargs='*',
                        help='Excel files to convert.')

    parser.add_argument("-v", "--verbose", help="Display acrostic list",
                        action="store_true",
                        default=False)

    return parser.parse_args()


def main():
    in_args = _argparse()

    for ii_input_file in in_args.excel_files:

        try:
            excel_to_csv(ii_input_file, in_args.verbose)
        except:
            print(f'Unable to convert {ii_input_file}')
            raise

if __name__ == '__main__':
    sys.exit(main())

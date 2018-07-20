#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import argparse
import json
import os
import pandas
import sys
from IPython.display import display


columns = ('json_file', 'json_intended_for', 'exists')
json_intended_for_dataframe = []


def _argparse():

    """ Get command line arguments.
    """

    parser = argparse.ArgumentParser(prog='fmap_intended_for')

    parser.add_argument('fmap_json_files',
                        nargs='*',
                        help='BIDS functional files')

    parser.add_argument('-v', '--verbose', help='Verbose flag to display to stdout.',
                        action='store_true',
                        default=False)

    in_args = parser.parse_args()

    return in_args


def check_intended_for_files_exist(func_nii_gz):
    json_full_filename = os.path.abspath(os.path.join('..', '..', func_nii_gz))
    ii_func_nii_gz_filename = os.path.join('..', '..', json_full_filename)
    ii_func_nii_gz_exists = os.path.isfile(ii_func_nii_gz_filename)

    return  ii_func_nii_gz_filename,  json_full_filename,  ii_func_nii_gz_exists


def check_intended_for_files_exist(json_files, verbose= False):
    """

    :param json_files:
    :param verbose:
    :return:
    """

    for ii_fmap_json in json_files:
        json_file = json.load(open(ii_fmap_json))

        try:
            ii_func_intended_for = json_file['IntendedFor']

            for ii_func_nii_gz in ii_func_intended_for:
                json_intended_for_dataframe.append(check_intended_for_files_exist(ii_func_nii_gz))

        except:
            json_intended_for_dataframe.append(('', json_file, 'Missing IntendedFor'))


    df = pandas.DataFrame.from_records(json_intended_for_dataframe, columns=columns)
    df['relative_filename'] = df.json_intended_for.str.split('ses-[0-9]', 1, expand=True)[1]
    df['relative_filename'] = df.relative_filename.apply(lambda x: x[1:])

    df = df[['exists', 'relative_filename', ]]

    if verbose:
        with pandas.option_context('max_colwidth', 200):
            print('\n')
            display(df)
            print('\n')

    return df


def main():

    in_args = _argparse()
    check_intended_for_files_exist(in_args.fmap_json_files, verbose=in_args.verbose)


if __name__ == '__main__':
    sys.exit(main())

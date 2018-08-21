#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""
from collections import Iterable

import argparse
import json
import os
import pandas
import sys
import re
from IPython.display import display


columns = ('json_file', 'json_intended_for', 'exists')
json_intended_for_dataframe = []


def force_input_to_list(inp, basetype=int):
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

    return out_list


def _split_json_intended_for(x):

    try:
        return re.compile(r'ses-[0-9]').split(x,1)[1]
    except:
        return ''


def _argparse():

    """ Get command line arguments.
    """

    parser = argparse.ArgumentParser(prog='fmap_intended_for')

    parser.add_argument('fmap_json_files',
                        nargs='*',
                        help='BIDS functional files')

    parser.add_argument('-w', '--display_width', default=200, type=int)
    parser.add_argument('-v', '--verbose', help='Verbose flag to display to stdout.',
                        action='store_true',
                        default=False)

    in_args = parser.parse_args()

    return in_args


def _check_intended_for_files_exist(func_nii_gz):

    json_full_filename = os.path.abspath(os.path.join('..', '..', func_nii_gz))
    ii_func_nii_gz_filename = os.path.join('..', '..', json_full_filename)
    ii_func_nii_gz_exists = os.path.isfile(ii_func_nii_gz_filename)

    return ii_func_nii_gz_filename,  json_full_filename,  ii_func_nii_gz_exists


def check_intended_for_files_exist(json_files, verbose= False, display_width=200):
    """

    :param json_files:
    :param verbose:
    :return:
    """

    print(len(json_files))

    for ii_fmap_json in json_files:
        json_file = json.load(open(ii_fmap_json))

        try:
            ii_func_intended_for = json_file['IntendedFor']

            ii_func_intended_for = force_input_to_list(ii_func_intended_for, basetype=str)

            for ii_func_nii_gz in ii_func_intended_for:
                ii_func_nii_gz_filename,  json_full_filename,  ii_func_nii_gz_exists = _check_intended_for_files_exist(ii_func_nii_gz)
                json_intended_for_dataframe.append((ii_fmap_json, json_full_filename, ii_func_nii_gz_exists))

        except:
            json_intended_for_dataframe.append((ii_fmap_json, '', 'Missing'))

    df = pandas.DataFrame.from_records(json_intended_for_dataframe, columns=columns)

    df['intended_for_filename'] = df.json_intended_for.apply(lambda x: _split_json_intended_for(x))

    df = df[['json_file', 'intended_for_filename', 'exists']]

    if verbose:
        print('\n')
        with pandas.option_context('display.width', display_width, 'display.max_colwidth', 200):
            display(df)
        print('\n')

    return df


def main():

    in_args = _argparse()
    print(in_args.fmap_json_files)

    check_intended_for_files_exist(in_args.fmap_json_files, verbose=in_args.verbose, display_width=in_args.display_width)


if __name__ == '__main__':
    sys.exit(main())

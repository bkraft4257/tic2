#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create a list of functional files to be included in
"""

import sys
import glob
import argparse


def _argparse():
    """ Get command line arguments.
    """

    parser = argparse.ArgumentParser(prog='conn_gather_inputs')

    parser.add_argument('func_files', nargs='*',
                        help='BIDS functional files')

    in_args = parser.parse_args()

    return in_args


def _print_intended_for_from_list(files):

    print(f'"IntendedFor":["{files[0]}",')

    for ii_file in enumerate(files[1:-1]):
        print(f'"{ii_file}",')

    print(f'"{files[-1]}"],')


def main():

    in_args = _argparse()
    _print_intended_for_from_list(in_args.func_files)




    if __name__ == '__main__':
    sys.exit(main())
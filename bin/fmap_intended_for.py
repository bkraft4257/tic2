#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create a list of functional files to be included in
"""

import sys
import argparse

from tic_core import fmriprep_tools


def _argparse():

    """ Get command line arguments.
    """

    parser = argparse.ArgumentParser(prog='conn_gather_inputs')

    parser.add_argument('func_files', nargs='*',
                        help='BIDS functional files')

    in_args = parser.parse_args()

    return in_args


def main():

    in_args = _argparse()
    fmriprep_tools.print_intended_for_from_list(in_args.func_files)


if __name__ == '__main__':
    sys.exit(main())

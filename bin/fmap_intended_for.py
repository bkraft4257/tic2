#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create a list of functional files to be included in
"""

import sys
import argparse

import tic_core

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
    tic_core.print_intended_for_from_list(in_args.func_ifiles)


if __name__ == '__main__':
    sys.exit(main())

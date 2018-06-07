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

    parser = argparse.ArgumentParser(prog='fmap_intended_for')

    parser.add_argument('func_files', nargs='*',
                        help='BIDS functional files')

    parser.add_argument('-e', "--echo_times",
                        nargs='*',
                        type=float,
                        help="Echo Times",
                        default=[0.00492, 0.00738])

    parser.add_argument('-o', '--output', help='Output file')

    parser.add_argument("-f", "--fmap", help="Boolean flag to display EchoTime.",
                        action="store_true",
                        default=False)

    in_args = parser.parse_args()

    return in_args


def main():

    in_args = _argparse()
    stripped_files = fmriprep_tools.lstrip_to_ses_key(in_args.func_files)
    fmriprep_tools.print_intended_for_from_list(stripped_files)

    if in_args.fmap:
        fmriprep_tools.print_echo_times_from_list(in_args.echo_times)


if __name__ == '__main__':
    sys.exit(main())

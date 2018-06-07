#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create a list of functional files to be included in
"""

import sys
import argparse
import shutil

from tic_core import fmriprep_tools


def _write_intended_for(intended_for_string, input_file, output_file=None):

    if output_file is None:
        output_file = input_file + '.new'

    with open(input_file) as old, open(output_file, 'w') as new:

        for ii, ii_line in enumerate(old):

            if ii == 1:
                new.write(intended_for_string)
            else:
                new.write(ii_line)

    # shutil.move('newtest', 'test')

    return


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

    parser.add_argument('-i', '--input_file', help='BIDS fmap json file',  default=None)

    parser.add_argument('-o', '--output_file', help='Output file', default=None)

    parser.add_argument("-f", "--fmap", help="Boolean flag to display EchoTime.",
                        action="store_true",
                        default=False)

    in_args = parser.parse_args()

    return in_args


def main():

    in_args = _argparse()
    stripped_files = fmriprep_tools.lstrip_to_ses_key(in_args.func_files)

    insert_string = fmriprep_tools.print_intended_for_from_list(stripped_files)

    if in_args.fmap:
        insert_string += fmriprep_tools.print_echo_times_from_list(in_args.echo_times)

    if in_args.input_file is not None:
        _write_intended_for(insert_string,
                            input_file=in_args.input_file,
                            output_file=in_args.output_file)

    print(insert_string)


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Check for the existence of a file and report if it is found or not found by study acrostic.
"""

import glob
import os
import argparse
import sys

# TODO Study Choices should be a common variable that is imported.


def get_active_study():
    return os.getenv('ACTIVE_STUDY')


def _argparse():
    """ Get command line arguments.

    """
    parser = argparse.ArgumentParser(prog='processing_status')

    parser.add_argument('file_pattern', help='String file pattern to glob')

    parser.add_argument("-r", "--recursive", help="Recursive boolean flag for glob",
                        action="store_true",
                        default=False)

    return parser.parse_args()


def main():

    in_args = _argparse()

    files = glob.glob(in_args.file_pattern,
                      recursive=in_args.recursive)

    for ii,ii_files in enumerate(files):
        print(f'{ii}) {ii_files}\n')

    return


# ====================================================================================================================
# region Command Line Interface

if __name__ == '__main__':
    sys.exit(main())

# endregion

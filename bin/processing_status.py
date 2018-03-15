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

    return parser.parse_args()


def main():

    in_args = _argparse()

    print(in_args)

    files = glob.glob(in_args.file_pattern)

    print(get_active_study())
    print('\n')
    print(files)

    return


# ====================================================================================================================
# region Command Line Interface

if __name__ == '__main__':
    sys.exit(main())

# endregion

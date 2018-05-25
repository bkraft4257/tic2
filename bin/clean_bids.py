#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Clean bids directory.
"""

import argparse
import glob
import os
import sys



def _argparse():
    """ Get command line arguments.
    """

    parser = argparse.ArgumentParser(prog='conn_gather_inputs')


    parser.add_argument('subject', help='BIDS subject value')

    parser.add_argument('--yaml_filename', help='YAML configuration file',
                        default=YAML_CONFIG_FILENAME_DEFAULT)



    parser.add_argument('-ss', '--session',
                        help='BIDS session value',
                        type=str,
                        default='1')

    parser.add_argument('-v', '--verbose', help='Turn on verbose mode.',
                        action='store_true',
                        default=False)

    in_args = parser.parse_args()

    if in_args.session.lower() == 'none':
        in_args.session = None

    return in_args


def _rename_hdc_item__numbers(start_directory=None):

    if start_directory is None:
        start_directory = '**/'

    files = []
    for ext in ('.nii.gz', '*.json'):
        files.extend(glob.glob(os.path.join(f'{start_directory}', '**', f'*.1.{ext}')))

    print(files)


def main():

    in_args = _argparse()

    _rename_hdc_item__numbers()


if __name__ == '__main__':
    sys.exit(main())

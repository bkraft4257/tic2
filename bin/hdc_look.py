#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Looks at various files involved in the Heudiconv convert process.
"""

import pandas
import argparse
import os
import sys
from colorama import Fore

ACTIVE_ACROSTIC_REGEX = os.getenv('ACTIVE_ACROSTIC_REGEX')

HDC_FILES = ['edit', 'auto', 'dicominfo']
BIDS_PATH = os.path.abspath(os.getenv('ACTIVE_BIDS_PATH'))

DISPLAY_COLUMNS = ['series_id', 'sequence_name', 'series_description',
                   'dim1', 'dim2', 'dim3', 'dim4',
                   'TR', 'TE', 'is_derived', 'is_motion_corrected']


def _display_text_file(filename):

    try:

        print(f'\n\n{filename}\n')

        with open(filename, 'r') as fin:
            print(fin.read())

    except FileNotFoundError:
        print(f'{Fore.RED}File not found. {Fore.WHITE}{filename}')


def _read_dicominfo_tsv(tsv_filename):
    try:
        return pandas.read_csv(tsv_filename, sep='\t')

    except FileNotFoundError:
        print(f'{Fore.RED} File not found. {Fore.WHITE}{tsv_filename}')
        sys.exit()


def _add_header(df_dicominfo,
                display_columns=DISPLAY_COLUMNS,
                verbose=False):

    df_dicominfo.columns = ['total_files_till_now',            # 01
                            'example_dcm_file',                # 02
                            'series_id',                       # 03
                            'unspecified1',                    # 04
                            'unspecified2',                    # 05
                            'unspecified3',                    # 06
                            'dim1',                            # 07
                            'dim2',                            # 08
                            'dim3',                            # 09
                            'dim4',                            # 10
                            'TR',                              # 11
                            'TE',                              # 12
                            'protocol_name',                   # 13
                            'is_motion_corrected',             # 14
                            'is_derived',                      # 15
                            'patient_id',                      # 16
                            'study_description',               # 17
                            'referring_physician_name',        # 18
                            'series_description',              # 19
                            'sequence_name',                   # 20
                            'image_type',                      # 21
                            'accession_number',                # 22
                            'patient_age',                     # 23
                            'patient_sex',                     # 24
                            'date']                            # 25

    df_dicominfo['series_number'] = df_dicominfo['series_id'].str.split('-').str.get(0)

    if verbose:
        pandas.set_option('display.max_columns', 500)
        pandas.set_option('display.width', 1000)
        print(df_dicominfo[display_columns])

    return df_dicominfo


def _save_dicominfo_csv(df_dicominfo, csv_filename):

    if csv_filename is not None:
        df_dicominfo.to_csv(csv_filename)


if __name__ == '__main__':

    """
    Look at various files involved in the Heudiconv convert process
    """

    usage = 'usage: %prog [options] arg1 arg2'

    parser = argparse.ArgumentParser(prog='heudiconv_add_header')

    # parser.add_argument('tsv_filename', help='DICOM TSV info file created the heurdiconv.py')

    parser.add_argument('-s', '--subject', help='Participant Label', default=ACTIVE_ACROSTIC_REGEX)
    parser.add_argument('-ss', '--session', help='Session Label', default=1)

    parser.add_argument('-b', '--bids', help='BIDS path.  default=ACTIVE_BIDS_PATH', default=BIDS_PATH)

    parser.add_argument('-f', '--files',
                        nargs='*',
                        type=str,
                        help="Files to display", choices=['edit', 'auto', 'dicominfo'], default=['dicominfo', 'edit'])

    in_args = parser.parse_args()

    hdc_info_path = os.path.join(os.path.abspath(in_args.bids), '.heudiconv', in_args.subject, f'ses-{in_args.session}', 'info')

    if in_args.session.lower() == 'none':
        in_args.session = None

    if in_args.session is None:
        bids_session = ''
    else:
        bids_session = f'_ses-{in_args.session}'

    edit_text_filename = os.path.join(hdc_info_path, f'{in_args.subject}{bids_session}.edit.txt')
    auto_text_filename = os.path.join(hdc_info_path, f'{in_args.subject}{bids_session}.auto.txt')
    dicominfo_tsv_filename = os.path.join(hdc_info_path, f'dicominfo{bids_session}.tsv')

    try:
        if 'dicominfo' in HDC_FILES:
            dicominfo_tsv_filename = _read_dicominfo_tsv(dicominfo_tsv_filename)
            _add_header(dicominfo_tsv_filename, verbose=True)

        if 'auto' in in_args.files:
            _display_text_file(auto_text_filename)

        if 'edit' in in_args.files:
            _display_text_file(edit_text_filename)

            print(f'{Fore.YELLOW}\n\tIf {edit_text_filename}'
                  f'\n\tis incorrect, you may edit it in any text editor directly and then rerun hdc.sh\n\n{Fore.WHITE}')
    except:

        print(Fore.RED + '\nFailed to run ... \n\n' + Fore.WHITE +
                         'heudiconv_add_header  -subject {0} --session {1} --bids {2}  \n\n'
              .format(in_args.subject,
                      in_args.session,
                      in_args.bids,
                      ))
        raise

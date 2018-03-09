#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Looks at various files involved in the Heudiconv convert process.
"""

import pandas
import argparse
import os

HDC_FILES = ['edit', 'auto', 'dicominfo']
BIDS_PATH = os.getenv('ACTIVE_BIDS_PATH')

DISPLAY_COLUMNS = ['series_number', 'sequence_name', 'series_description',
                   'dim1', 'dim2', 'dim3', 'dim4',
                   'TR', 'TE', 'is_derived', 'is_motion_corrected']


def _display_text_file(filename):

    try:

        print(f'\n\n{filename}\n')

        with open(filename, 'r') as fin:
            print(fin.read())

    except FileNotFoundError:
        print(f'File not found. {filename}')


def _read_dicominfo_tsv(tsv_filename):
    print(f'\n\n{tsv_filename}\n')
    return pandas.read_csv(tsv_filename, sep='\t')


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

    parser.add_argument('-s', '--subject', help='Participant Label')
    parser.add_argument('-ss', '--session', help='Session Label', default=1)

    parser.add_argument('-b', '--bids', help='BIDS path.  default=ACTIVE_BIDS_PATH', default=BIDS_PATH)

    parser.add_argument('-f', '--files',
                        nargs='*',
                        type=str,
                        help="Verbose flag", choices=['edit', 'auto', 'dicominfo'], default=['dicominfo', 'edit'])

    parser.add_argument('-v', '--verbose', help="Verbose flag", action="store_true", default=False)

    in_args = parser.parse_args()

    hdc_info_path = os.path.join(in_args.bids, '.heudiconv', in_args.subject, f'ses-{in_args.session}', 'info')

    edit_text_filename = os.path.join(hdc_info_path, f'{in_args.subject}_ses-{in_args.session}.edit.txt')
    auto_text_filename = os.path.join(hdc_info_path, f'{in_args.subject}_ses-{in_args.session}.auto.txt')
    dicominfo_tsv_filename = os.path.join(hdc_info_path, f'dicominfo_ses-{in_args.session}.tsv')

    try:
        if 'dicominfo' in HDC_FILES:
            dicominfo_tsv_filename = _read_dicominfo_tsv(dicominfo_tsv_filename)
            _add_header(dicominfo_tsv_filename, verbose=True)

        if 'auto' in in_args.files:
            _display_text_file(auto_text_filename)

        if 'edit' in in_args.files:
            _display_text_file(edit_text_filename)

    except:

        print('\nFailed to run ... \n\n'
              'heudiconv_add_header  {0} --out_filename {1} --verbose {2} \n\n'
              .format(in_args.tsv_filename,
                      in_args.out_filename,
                      in_args.verbose))
        raise

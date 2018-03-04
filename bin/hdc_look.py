#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Looks at various files involved in the Heudiconv convert process.
"""

import pandas
import argparse
import os

HDC_FILES = ['edit.txt', 'auto.txt']
BIDS_PATH = os.getenv('ACTIVE_BIDS_PATH')

def _display_text_file(filename):

    try:
        with open(filename, 'r') as fin:
            print(fin.read())
    except FileNotFoundError:
        print(f'File not found. {filename}')

def _read_dicominfo_tsv(tsv_filename):
    return pandas.read_csv(tsv_filename, sep='\t')


def _add_header(df_dicominfo, verbose=False):

    verbose_columns = ['series_id', 'sequence_name', 'series_description',
                       'dim1', 'dim2', 'dim3', 'dim4',
                       'TR', 'TE', 'is_derived', 'is_motion_corrected']

    df_dicominfo.columns = ['total_files_till_now',            #  1
                            'example_dcm_file',                #  2
                            'series_id',                       #  3
                            'unspecified1',                    #  4
                            'unspecified2',                    #  5
                            'unspecified3',                    #  6
                            'dim1',                            #  7
                            'dim2',                            #  8
                            'dim3',                            #  9
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

    if verbose:
        pandas.set_option('display.max_columns', 500)
        pandas.set_option('display.width', 1000)
        print(df_dicominfo[verbose_columns])

    return df_dicominfo


def _save_dicominfo_csv(df_dicominfo, csv_filename):

    if csv_filename is not None:
        df_dicominfo.to_csv(csv_filename)


def add_header(tsv_filename, verbose=False):

    df_tsv = _read_dicominfo_tsv(tsv_filename)
    df_dicominfo = _add_header(df_tsv, verbose=verbose)

    if verbose:



    return



if __name__ == '__main__':

    """
    Look at various files involved in the Heudiconv convert process
    """

    usage = 'usage: %prog [options] arg1 arg2'

    parser = argparse.ArgumentParser(prog='heudiconv_add_header')

    parser.add_argument('tsv_filename', help='DICOM TSV info file created the heurdiconv.py')

    parser.add_argument('-s', '--subject', help='Participant Label')
    parser.add_argument('-ss' '--session', help='Session Label')

    parser.add_argument('-f', '--files', help="Verbose flag", choices=['edit.txt', 'auto.txt'], default ='edit.txt')

    parser.add_argument('-v', '--verbose', help="Verbose flag", action="store_true", default=False)

    in_args = parser.parse_args()



    edit_text_filename = os.path.join(BIDS_PATH, '.heudiconv', in_args.subject, f'ses-{in_args.session}',
                                      'info', f'{in_args.subject}_ses-{in_args.session}.edit.txt')

    print(edit_text_filename)

    try:
        if in_args.files in HDC_FILES:
            _display_text_file(edit_text_filename)


    except:

        print('\nFailed to run ... \n\n'
              'heudiconv_add_header  {0} --out_filename {1} --verbose {2} \n\n'
              .format(in_args.tsv_filename,
                      in_args.out_filename,
                      in_args.verbose))
        raise
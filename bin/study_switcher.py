#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Writes a bash script to TIC_INIT_PATH.  This function is often called with an alias that calls this function
and then sources the bash script.  For example,

alias swh='study_switcher.py -s hfpef; source $TIC_INIT_PATH/tic_study_switcher.sh'

"""

import os
import argparse
import sys

STUDY_CHOICES = ['hfpef', 'synergy', 'infinite', 'cenc', 'imove']
DEFAULT_STUDY_CHOICE = 'hfpef'

STUDY_SWITCHER_OUTPUT_FILENAME = os.path.abspath(os.path.join(os.getenv('TIC_INIT_PATH'),
                                           'tic_study_switcher.sh'))

DEFAULT_STUDY_SWITCHER_OUTPUT_FILENAME = os.path.abspath(os.path.join(os.getenv('TIC_INIT_PATH'),
                                          'tic_default_study.sh'))


def _write_study_switcher_script(active_study,
                                 out_filename=STUDY_SWITCHER_OUTPUT_FILENAME,
                                 ):

    active_study = active_study.upper()

    with open(out_filename, 'w') as file:  # Use file to refer to the file object

        file.write(f'#!/bin/env bash\n\n')

        file.write(f'# TIC Study Switcher Script\n')
        file.write(f'# =========================\n\n')

        file.write(f"echo 'Previous active study' = $ACTIVE_STUDY\n\n")

        file.write(f'export ACTIVE_STUDY={active_study}\n')
        file.write(f'export ACTIVE_ACROSTIC_REGEX={active_study}_ACROSTIC_REGEX\n')
        file.write(f'export ACTIVE_SCRIPTS_PATH=${active_study}_SCRIPTS_PATH \n')
        file.write(f'export ACTIVE_PATH=${active_study}_PATH\n')
        file.write(f'export ACTIVE_BIDS_PATH=${active_study}_BIDS_PATH\n')
        file.write(f'export ACTIVE_IMAGE_ANALYSIS_PATH=${active_study}_IMAGE_ANALYSIS_PATH\n')
        file.write(f'export ACTIVE_IMAGE_PROCESSING_PATH=${active_study}_IMAGE_PROCESSING_PATH\n')
        file.write(f'export ACTIVE_IMAGE_PROCESSING_LOG_PATH=${active_study}_IMAGE_PROCESSING_LOG_PATH\n')
        file.write(f'export ACTIVE_MRIQC_PATH=${active_study}_MRIQC_PATH\n')
        file.write(f'export ACTIVE_FMRIPREP_PATH=${active_study}_FMRIPREP_PATH\n')
        file.write(f'export ACTIVE_NETPREP_PATH=${active_study}_NETPREP_PATH\n')

        file.write(f'export ACTIVE_BIDS_CONFIG_FILE=${active_study}_BIDS_CONFIG_FILE\n')
        file.write(f'export ACTIVE_HEUDICONV_PROTOCOL=${active_study}_HEUDICONV_PROTOCOL\n')
        file.write(f'export ACTIVE_CLEAN_BIDS=${active_study}_CLEAN_BIDS\n')
        file.write(f'export ACTIVE_SINGULARITY_USER_BIND_PATHS=${active_study}_SINGULARITY_USER_BIND_PATHS\n')

        # SUBJECTS_DIR for FreeSurfer
        file.write(f'export ACTIVE_SUBJECTS_DIR=${active_study}_SUBJECTS_DIR\n')
        file.write(f'export SUBJECTS_DIR=${active_study}_SUBJECTS_DIR\n\n')

        # BIDS APPS output directories
        file.write(f'export ACTIVE_ACT_PATH=${active_study}_ACT_PATH\n')
        file.write(f'export ACTIVE_FMRIPREP_PATH=${active_study}_FMRIPREP_PATH\n')
        file.write(f'export ACTIVE_NETPREP_PATH=${active_study}_NETPREP_PATH\n')

        file.write(f"echo 'Current active study' = $ACTIVE_STUDY\n\n")


def _argparse():
    # Parsing Arguments
    # TODO: Improve documentation.

    parser = argparse.ArgumentParser(prog='study_switcher')

    parser.add_argument('-s','--study',
                        help='Switch to a different study.',
                        choices=STUDY_CHOICES,
                        type=str,
                        default=None,
                        )

    parser.add_argument("-d", "--default", help="Set selected study as default.",
                        action="store_true",
                        default=False)

    parser.add_argument("-v", "--verbose", help="Display contents of study_switcher output_file.",
                        action="store_true",
                        default=False)

    return parser.parse_args()

def _select_output_file(default_flag):

    if default_flag:
        output_file = DEFAULT_STUDY_SWITCHER_OUTPUT_FILENAME;
    else:
        output_file = STUDY_SWITCHER_OUTPUT_FILENAME;

    return output_file

def main():

    in_args = _argparse()

    output_filename = _select_output_file(in_args.default)

    if in_args.study is not None:
        _write_study_switcher_script(in_args.study,
                                     output_filename)

    if in_args.verbose or in_args.study is None:

        print(f'\n\n{output_filename} .... \n\n')

        with open(output_filename, 'r') as file:
            print(file.read())

    return


# ====================================================================================================================
# region Command Line Interface

if __name__ == '__main__':
    sys.exit(main())

# endregion

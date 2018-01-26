#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__version__ = "0.0.0"

import os
import argparse
import sys

STUDY_CHOICES = ['hfpef', 'synergy', 'infinite']
DEFAULT_STUDY_CHOICE = 'hfpef'

output_file = os.path.abspath(os.path.join(os.getenv('TIC_INIT_PATH'),
                                           'tic_study_switcher.sh'))

default_file = os.path.abspath(os.path.join(os.getenv('TIC_INIT_PATH'),
                                           'tic_default_study.sh'))


def _write_study_switcher_script(active_study, out_filename=output_file):

    active_study = active_study.upper()

    with open(output_file, 'w') as file:  # Use file to refer to the file object

        file.write(f'#!/bin/env bash\n\n')

        file.write(f'# TIC Study Switcher Script\n')
        file.write(f'# =========================\n\n')
        file.write(f'# You should never see this file. It should be created, sourced, and then deleted. \n')
        file.write(f'# If you see it you should just delete it.\n\n')

        file.write(f"echo 'Previous active study' = $ACTIVE_STUDY\n\n")

        file.write(f'export ACTIVE_STUDY={active_study}\n')
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

    parser.add_argument('active_study',
                        help='Switch to a different study.',
                        choices=['hfpef', 'synergy', 'infinite'],
                        type=str,
                        default='hfpef',
                        )

    parser.add_argument("-d", "--default", help="Set select study as default.",
                        action="store_true",
                        default=False)

    return parser.parse_args()


def main():

    in_args = _argparse()

    if in_args.default:
        _write_study_switcher_script(in_args.active_study,
                                     out_filename=default_file)
    else:
        _write_study_switcher_script(in_args.active_study,
                                     out_filename=output_file)

    return


# ====================================================================================================================
# region Command Line Interface

if __name__ == '__main__':
    sys.exit(main())

# endregion

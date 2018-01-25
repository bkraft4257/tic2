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

output_file = 'tic_study_switcher.txt'


def _write_study_switcher_script(active_study):

    active_study = active_study.upper()

    with open(output_file, 'w') as file:  # Use file to refer to the file object

        file.write(f'#/bin/env bash\n\n')

        file.write(f'# TIC Study Switcher Script\n')
        file.write(f'# =========================\n\n')
        file.write(f'# You should never see this file. It should be created, sourced, and then deleted. \n')
        file.write(f'# If you see it you should just delete it.\n\n')

        file.write(f'export ACTIVE_STUDY_SCRIPTS_PATH=${active_study}_INFINITE_SCRIPTS_PATH \n')

        file.write(f'export ACTIVE_STUDY_PATH=${active_study}_PATH\n')
        file.write(f'export ACTIVE_STUDY_BIDS_PATH=${active_study}_BIDS_PATH\n')
        file.write(f'export ACTIVE_STUDY_IMAGE_ANALYSIS_PATH=${active_study}_IMAGE_ANALYSIS_PATH\n')
        file.write(f'export ACTIVE_STUDY_IMAGE_PROCESSING_PATH=${active_study}_IMAGE_PROCESSING_PATH\n')
        file.write(f'export ACTIVE_STUDY_MRIQC_PATH=${active_study}_MRIQC_PATH\n')
        file.write(f'export ACTIVE_STUDY_FMRIPREP_PATH=${active_study}_FMRIPREP_PATH\n')
        file.write(f'export ACTIVE_STUDY_NETPREP_PATH=${active_study}_NETPREP_PATH\n')

        file.write(f'export ACTIVE_STUDY_BIDS_CONFIG_FILE=${active_study}_BIDS_CONFIG_FILE\n')

        # BIDS APPS output directories
        file.write(f'export ACTIVE_STUDY_ACT_PATH=${active_study}_ACT_PATH\n')
        file.write(f'export ACTIVE_STUDY_FMRIPREP_PATH=${active_study}_FMRIPREP_PATH\n')
        file.write(f'export ACTIVE_STUDY_NETPREP_PATH=${active_study}_NETPREP_PATH\n\n')


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

#    parser.add_argument("-d", "--debug", help="Switch to help with debugging.", action="store_true",
#                        default=False)



    return parser.parse_args()


def main():

    in_args = _argparse()

    previous_active_study = os.getenv('ACTIVE_STUDY')
    print(f'Previous active study = {previous_active_study}\n')

    _write_study_switcher_script(in_args.active_study)

    current_active_study = os.getenv('ACTIVE_STUDY')
    print(f'Current active study = {current_active_study}\n')

    return


# ====================================================================================================================
# region Command Line Interface

if __name__ == '__main__':
    sys.exit(main())

# endregion

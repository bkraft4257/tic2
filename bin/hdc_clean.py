#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Looks at various files involved in the Heudiconv convert process.
"""

import argparse
import os
import shutil
from colorama import Fore, Back, Style

BIDS_PATH = os.getenv('ACTIVE_BIDS_PATH')


if __name__ == '__main__':

    """
    Remove specific subject and session of from .heudiconv directory
    """

    parser = argparse.ArgumentParser(prog='hdc_clean')

    parser.add_argument('-s', '--subject', help='Participant Label')
    parser.add_argument('-ss', '--session', help='Session Label', default=1)

    in_args = parser.parse_args()

    bids_subject_session_path = os.path.join(BIDS_PATH, f'sub-{in_args.subject}_ses-{in_args.session}')
    heudiconv_subject_session_path = os.path.join(BIDS_PATH, '.heudiconv', in_args.subject, f'ses-{in_args.session}')

    for ii in [bids_subject_session_path, heudiconv_subject_session_path]:
        try:
            shutil.rmtree(ii)
            print(Fore.GREEN + f'\nSuccessfully removed {ii}\n\n')

        except:
            print(Fore.RED + f'\nFailed to remove {ii}\n\n')

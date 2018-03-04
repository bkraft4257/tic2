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

    subject_session_path = os.path.join(BIDS_PATH, '.heudiconv', in_args.subject, f'ses-{in_args.session}')

    try:
        shutil.rmtree(subject_session_path)
        print(Fore.GREEN + f'\nSuccessfully removed {subject_session_path}\n\n')

    except:

        print(Fore.RED + f'\nFailed to remove {subject_session_path}\n\n')
        raise

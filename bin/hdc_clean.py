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

    bids_subject_session_path = os.path.join(BIDS_PATH, f'sub-{in_args.subject}', f'ses-{in_args.session}')
    heudiconv_subject_session_path = os.path.join(BIDS_PATH, '.heudiconv', in_args.subject, f'ses-{in_args.session}')

    print('\n')

    for ii in [bids_subject_session_path, heudiconv_subject_session_path]:
        try:

            # We want to remove these directories. If the directory doesn't exist just assume that it was deleted.  After all
            # the result is the same if the directory was successfully deleted. This is why I don't catch the exception.

            if os.path.isdir(ii):
                shutil.rmtree(ii)

            print(Fore.GREEN + f'Successfully removed {ii}')

        except:
            print(Fore.RED + f'Failed to remove {ii}')

    print('\n')

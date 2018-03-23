#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple function to link study init files to init_<study>.sh in $TIC_PATH/studies/study/.  This script should be called
when a new study has been added to the TIC_PATH has changed.

"""

import sys
import os
import errno

STUDY_LIST = ('cenc', 'hfpef', 'imove', 'infinite', 'mcf', 'synergy',)
TIC_PATH = os.getenv('TIC_PATH')
TIC_INIT_PATH = os.getenv('TIC_INIT_PATH')


def symlink_force(target, link_name):
    """
    https://stackoverflow.com/questions/8299386/modifying-a-symlink-in-python
    """

    try:

        if os.path.isfile(target):
            os.symlink(target, link_name)
        else:
            print(f'\nSource file does not exist. Skipping creating link. \n{target}\n')

    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(link_name)
            os.symlink(target, link_name)
        else:
            raise e

    return


def main():
    for ii in STUDY_LIST:

        ii_source = os.path.join(TIC_PATH, 'studies', ii, f'{ii}_init.sh')
        ii_link = os.path.join(TIC_INIT_PATH, f'{ii}_init.sh')

        print(f'ln -sf {ii_source} {ii_link}')

        symlink_force(ii_source, ii_link,)


if __name__ == '__main__':
    sys.exit(main())

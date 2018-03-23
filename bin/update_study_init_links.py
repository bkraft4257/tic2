#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import errno


STUDY_LIST = ('cenc', 'hfpef', 'imove', 'infinite',  'mcf', 'synergy', )
TIC_PATH = os.getenv('TIC_PATH')
TIC_INIT_PATH = os.getenv('TIC_INIT_PATH')


def symlink_force(target, link_name):
    """
    https://stackoverflow.com/questions/8299386/modifying-a-symlink-in-python
    """

    try:
        os.symlink(target, link_name)

    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(link_name)
            os.symlink(target, link_name)
        else:
            raise e

    return


def main():

    for ii in STUDY_LIST:
        symlink_force(os.path.join(TIC_PATH, 'studies', ii, f'{ii}_init.sh'),
                      os.path.join(TIC_INIT_PATH,  f'{ii}_init.sh'),
                      )


if __name__ == '__main__':
   sys.exit(main())

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__version__ = "0.0.0"

import os
import shutil


# --- Helper functions
def _absjoin(*path):
    return os.path.abspath(os.path.join(*path))


def _copy_file(source, target):
    try:
        shutil.copy(source, target)

    except FileExistsError:
        print('{0} already exists. File was not copied.'.format(target))

    except FileNotFoundError:
        print('{0} not found. File was not copied.'.format(source))


def _check_shell():

    shell = os.getenv('SHELL')

    if not (('zsh' in shell) | ('bash' in shell)):
        print('TIC requires that you use the bash or zsh. '
              'Setup your Unix environment to run one of these shells \n'
              ' before continuing.')


# --- Grab environment variables and filenames

os.environ['TIC_PATH'] = '/gandg/tic2/'

tic_path = os.getenv('TIC_PATH')
home_tic_path = _absjoin(os.getenv('HOME'), '.tic2')

tic_zshrc_filename = 'tic_zshrc.sh'
tic_environment_filename = 'tic_wake_aging1a_environment.sh'

tic_zshrc = _absjoin(tic_path, 'init', tic_zshrc_filename)
tic_environment = _absjoin(tic_path, 'init', tic_environment_filename)


# --- Perform setup

_check_shell()

if not os.path.isdir(home_tic_path):
    os.makedirs(home_tic_path)

_copy_file(tic_zshrc, _absjoin(home_tic_path, tic_zshrc_filename))
_copy_file(tic_environment, _absjoin(home_tic_path, tic_environment))

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


def _link_file(source, target):
    try:
        os.link(source, target)

    except FileExistsError:
        print('{0} already exists. File was not copied.'.format(target))

    except FileNotFoundError:
        print('{0} not found. File was not copied.'.format(source))


def _link_studies(tic_path, tic_home_init):

    for ii in ['hfpef', 'infinite', 'synergy']:
        _link_file( _absjoin(tic_path, 'studies', ii, f'{ii}_init.sh'),
                    _absjoin(tic_home_init, 'studies', ii, f'{ii}_init.sh'))


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


# This is done here to facilitate a user setting up their environment.  This
# environment variable is set properly in tic_zshrc.sh

tic_path = os.getenv('TIC_PATH')
home_tic_path = _absjoin(os.getenv('HOME'), '.tic')

tic_zshrc_filename = 'tic_zshrc.sh'
tic_environment_filename = 'tic_wake_aging1a_environment.sh'

tic_zshrc = _absjoin(tic_path, 'init', tic_zshrc_filename)
tic_environment = _absjoin(tic_path, 'init', tic_environment_filename)

# --- Perform setup

_check_shell()

if not os.path.isdir(home_tic_path):
    os.makedirs(home_tic_path)

_copy_file(tic_zshrc, _absjoin(home_tic_path, tic_zshrc_filename))
_copy_file(tic_environment, _absjoin(home_tic_path, tic_environment_filename))

_link_studies(tic_path, home_tic_path)
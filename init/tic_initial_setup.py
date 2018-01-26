#!/opt/anaconda3-4.4.0/bin/python
# -*- coding: utf-8 -*-

"""
"""

__version__ = "0.0.0"

import os
import shutil
import time


# --- Helper functions
def _absjoin(*path):
    return os.path.abspath(os.path.realpath(os.path.join(*path)))


def _link_file(source, target):

    print()
    print(source)
    print(target)
    print()

    try:
        os.symlink(source, target)

    except FileExistsError:
        print('{0} already exists. File was not copied.'.format(target))

    except FileNotFoundError:
        print('{0} not found. File was not copied.'.format(source))


def _link_studies(tic_path, tic_home_init):

    for ii in ['hfpef', 'infinite', 'synergy']:
        _link_file( _absjoin(tic_path, 'studies', ii, f'{ii}_init.sh'),
                    _absjoin(tic_home_init, f'{ii}_init.sh'))


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

def _add_timestamp(in_filename):

    timestamp = time.strftime("_%d_%m_%y_%H:%M:%S")
    return f'{in_filename}.{timestamp}'


def _backup_shell(in_filename):

    home_path = os.getenv('HOME')

    source_file = _absjoin(home_path, in_filename)
    backup_file = _absjoin(home_path, _add_timestamp(in_filename))

    _copy_file(source_file, backup_file)


def _update_shell(in_filename):

    _backup_shell(in_filename)

    # Create backup

    with open(in_filename, 'a') as file:  # Use file to refer to the file object

        file.write(f'\n\n\n')
        file.write(f'## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
        file.write(f'## TIC Setup\n\n')

        file.write(f'#export TIC_PATH =/gandg/tic/\n')
        file.write(f'#export TIC_INIT_PATH =$HOME /.tic\n')
        file.write(f'#source $TIC_INIT_PATH/tic_zshrc.sh\n\n')

        file.write(f'## Add Studies to my environment\n\n')

        file.write(f'#source $TIC_INIT_PATH/hfpef_init.sh\n')
        file.write(f'#source $TIC_INIT_PATH/synergy_init.sh\n')
        file.write(f'#source $TIC_INIT_PATH/infinite_init.sh\n')
        file.write(f'#source $TIC_INIT_PATH/tic_default_study.sh\n\n')

        file.write(f'## <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n')


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

# Copy files

_copy_file(tic_zshrc, _absjoin(home_tic_path, tic_zshrc_filename))
_copy_file(tic_environment, _absjoin(home_tic_path, tic_environment_filename))

_link_studies(tic_path, home_tic_path)

_update_shell('.zshrc')
_update_shell('.bashrc')
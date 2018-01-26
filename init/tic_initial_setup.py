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


TIC_PATH = os.getenv('TIC_PATH')
HOME_TIC_PATH = _absjoin(os.getenv('HOME'), '.tic')


def _link_file(source, target):

    try:
        os.symlink(source, target)

    except FileExistsError:
        print('{0} already exists. File was not copied.'.format(target))

    except FileNotFoundError:
        print('{0} not found. File was not copied.'.format(source))


def _link_studies(studies=['hfpef', 'infinite', 'synergy']):

    for ii in studies:
        _link_file( _absjoin(TIC_PATH, 'studies', ii, f'{ii}_init.sh'),
                    _absjoin(HOME_TIC_PATH, f'{ii}_init.sh'))


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

    timestamp = time.strftime("%m_%d_%y_%H:%M:%S")
    return f'{in_filename}.{timestamp}'


def _backup_shell(in_filename):

    home_path = os.getenv('HOME')

    source_file = _absjoin(home_path, in_filename)
    backup_file = _absjoin(home_path, _add_timestamp(in_filename))

    _copy_file(source_file, backup_file)


def copy_tic_init_file(filename):

    _copy_file(_absjoin(TIC_PATH, 'init', filename),
               _absjoin(HOME_TIC_PATH, filename))


def _update_shell(in_filename):

    _backup_shell(in_filename)

    # Create backup

    with open(in_filename, 'a') as file:  # Use file to refer to the file object

        file.write(f'\n\n\n')
        file.write(f'## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
        file.write(f'## TIC Setup\n\n')
        file.write(f'#export TIC_PATH=/gandg/tic/\n')
        file.write(f'#export TIC_INIT_PATH =$HOME/.tic\n')
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


# --- Perform setup

_check_shell()

if not os.path.isdir(HOME_TIC_PATH):
    os.makedirs(HOME_TIC_PATH)

# Copy files

copy_tic_init_file('tic_zshrc.sh')
copy_tic_init_file('tic_wake_aging1a_environment.sh')
copy_tic_init_file('tic_default_study.sh')

_link_studies()

_update_shell('.zshrc')
_update_shell('.bashrc')

print('\n\nTIC Initial Setup Completed. \n')
print('The next step is to uncomment TIC lines added to your .zshrc/.bashrc file.')
print('After commenting out the files please logout and log back in again.')
print('If you have successfully installed TIC on your aging1a account your when')
print('when you log back your terminal should look something like this:\n')
print('   -------- freesurfer-Linux-centos6_x86_64-stable-pub-v5.3.0 --------')
print('   Setting up environment for FreeSurfer/FS-FAST (and FSL)')
print('   FREESURFER_HOME   /aging1/software//freesurfer')
print('   FSFAST_HOME       /aging1/software//freesurfer/fsfast')
print('   FSF_OUTPUT_FORMAT nii.gz')
print('   SUBJECTS_DIR      /aging1/software//freesurfer/subjects')
print('   MNI_DIR           /aging1/software//freesurfer/mni')
print('   FSL_DIR           /aging1/software//fsl5.09')
print('   TIC_PATH     : /gandg/tic/')
print('   SUBJECTS_DIR : /aging1/software/freesurfer/subjects')
print('   umask        : 002')
print('   Current active study = HFPEF\n\n')



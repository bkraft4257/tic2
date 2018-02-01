#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates the skeleton for a new study
"""

__version__ = "0.0.0"

import argparse
import os
import logging

import shutil

logging.basicConfig(filename='create_new_study.log',level=logging.INFO)


def _get_command_line_args():
    """
    Get input arguments from command line.

    :return: argparse object
    """

    # Parsing Arguments

    usage = 'usage: %prog [options] arg1 arg2'

    parser = argparse.ArgumentParser(prog='create_new_study')

    parser.add_argument('study_name', help=('The name of the study you are creating. Ideally, this should be a single '
                                            'short word all in lower case letters.')
                        )

    parser.add_argument('study_path', help=('This is the parent directory of your study (absolute path) of your '
                                            'study containing data processing, analysis, etc.')
                        )

    parser.add_argument('tic_path', help='This is the absolute path of your TIC project.'
                        )

    parser.add_argument("-v", "--verbose", help="Verbose flag", action="store_true", default=False)

    in_args = parser.parse_args()

    return in_args


def _create_directory(directory):
    """ Creates a directory

    :param directory:
    :return:
    """

    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        logging.debug('%s was not created.', directory)


def _create_directories_for_new_study_in_tic(study_name, tic_path):
    """Creates directories for new study in TIC"""

    directories = (os.path.abspath(os.path.join(tic_path, 'studies', study_name)),
                   os.path.abspath(os.path.join(tic_path, 'studies', study_name, 'scripts'))
                   )

    for x in directories:
        _create_directory(x)

    return


def _create_directories_for_new_study(study_name, study_path):
    """Creates directories for new study in TIC"""

    directories = (os.path.abspath(study_path),
                   os.path.abspath(os.path.join(study_path, study_name)),
                   os.path.abspath(os.path.join(study_path, study_name, 'bids')),
                   os.path.abspath(os.path.join(study_path, study_name, 'image_processing')),
                   os.path.abspath(os.path.join(study_path, study_name, 'image_processing', 'logs')),
                   os.path.abspath(os.path.join(study_path, study_name, 'image_analysis')),
                   os.path.abspath(os.path.join(study_path, study_name, 'qc')),
                   os.path.abspath(os.path.join(study_path, study_name, 'qc', 'mriqc')),
                   os.path.abspath(os.path.join(study_path, study_name, 'scripts')),
                   )

    for x in directories:
        _create_directory(x)

    return


def _copy_files(source, destination):
    """
    Copy files from source to target.

    :param source:
    :param destination:
    :return:
    """

    try:
        logging.info('cp %s %s', source, destination)
        shutil.copyfile(source, destination)

    except FileNotFoundError:

        logging.debug('%s source file not found.', source)

    except FileExistsError:
        logging.debug('%s target file already exists.', destination)


def _copy_files_from_newstudy_template(study_name, tic_path):
    """
    Copy files from TIC new study template to new study

    :param study_name:
    :param tic_path:
    :return:
    """

    tic_new_study_path = os.path.abspath(os.path.join(tic_path, 'studies', study_name))
    tic_new_study_template_path = os.path.abspath(os.path.join(tic_path, 'studies', '_new_study_template'))

    _files_to_copy = ((os.path.join(tic_new_study_template_path, 'aliases.sh'),
                       os.path.join(tic_new_study_path, 'aliases.sh')),

                      (os.path.join(tic_new_study_template_path, 'environment.sh'),
                       os.path.join(tic_new_study_path, 'environment.sh')),

                      (os.path.join(tic_new_study_template_path, 'newstudy_init.sh',
                                    os.path.join(tic_new_study_path, f'{study_name}_init.sh'))),
                      )

    for ii in _files_to_copy:
        _copy_files(ii[0], ii[1])


def main():
    """ Initializes a new study"""

    in_args = _get_command_line_args()

    _create_directories_for_new_study_in_tic(in_args.study_name, in_args.tic_path)
    _create_directories_for_new_study(in_args.study_name, in_args.study_path)

    _copy_files_from_newstudy_template(in_args.study_name,
                                       in_args.tic_path
                                       )

    return


# ====================================================================================================================


if __name__ == '__main__':

    try:
        main()
    except Exception as e:
        logging.debug('\n\n%s failed to run. \n\n', __name__)
        raise

#!/usr/bin/env python3

import sys
import os 
import re
import shutil
import argparse

def _get_bids_subject(in_string):
    subject_keyvalue = _get_bids_keyvalue(in_string, 'sub')[0]
    return subject_keyvalue, _get_bids_key(subject_keyvalue)


def _get_bids_session(in_string):
    session_keyvalue = _get_bids_keyvalue(in_string, 'ses')[0]
    return session_keyvalue, _get_bids_key(session_keyvalue)


def _get_bids_keyvalue(in_string, key):
    return re.findall(r'[/_]?({0}-.*?)[/_]'.format(key),in_string)


def _split_bids_keyvalue(key_value_pair):
    return re.split('-', key_value_pair)


def _get_bids_key(key_value_pair):
    return _split_bids_keyvalue(key_value_pair)[1]


def _assemble_directory(in_path, subject, session, dir_name='func'):
    new_dir = os.path.abspath( os.path.join(in_path, subject, session, dir_name))
    return new_dir
 

def _assemble_filename(in_path, subject, session, file_body, file_ext, file_insert=''):
    return os.path.abspath( os.path.join(in_path,  subject + '_' + session + '_' + file_body + file_insert + file_ext))


def _copy_file(source_file, target_file):

    try:
        shutil.copy2(source_file, target_file)
#        print('cp {0} \n {1}'.format(source_file, target_file))
    except FileNotFoundError:
        print('{0} \n file not found'.format(source_file))

    return


def _check_if_file_exist(in_files):

    status = True

    for ii in in_files:
         if not  os.path.isfile(ii):
            status = False

    return status


def _remove_file(source_file, target_files):

    if _check_if_file_exist(target_files):
        print('\nRemoving source file \n {0}'.format(source_file))
        os.remove(source_file)
    else:
        print('Unable to find all files')
        raise FileNotFoundError
    return


file_recon_rename_inserts = ['_rec-fmap', '_rec-topup']

def main_func( in_args ):

    func_working_directory = _assemble_directory(in_args['bids_path'],
                                                 'sub-' + in_args['subject_value'],
                                                 'ses-' + in_args['session_value'], 'func')

    subject, subject_value = _get_bids_subject(func_working_directory)
    session, session_value = _get_bids_session(func_working_directory)

    file_suffix = 'task-rest_acq-epi'
    file_ext = ['_bold.json', '_bold.nii.gz', '_events.tsv']

    for ii, ii_ext in enumerate(file_ext):

        target_files = [0]*len(file_recon_rename_inserts)
        source_file = _assemble_filename(func_working_directory, subject, session, file_suffix, ii_ext)

        if _check_if_file_exist( [source_file ]):
            for jj, jj_recon_rename_inserts in enumerate(file_recon_rename_inserts):
                target_files[jj] = _assemble_filename(func_working_directory, subject, session, file_suffix, ii_ext, jj_recon_rename_inserts)
                _copy_file(source_file, target_files[jj])

            _remove_file(source_file, target_files)
        else:
            print('Source file does not exist. \n{0}\n'.format(source_file))
    return


def main(in_args):
    main_func( in_args)
    

def _get_parser():

    # Parsing Arguments
    # TODO: Improve documentation.

    usage = 'usage: %prog [options] arg1 arg2'

    parser = argparse.ArgumentParser(prog='hfpef_bids_clean_2')

    parser.add_argument('bids_path', help='BIDS PATH')
    parser.add_argument('subject_value', help='Subject acrostic (i.e. subject value, hfu068)')
    parser.add_argument('session_value', help='Session value (i.e. 1)')

    parser.add_argument("-v", "--verbose", help="Verbose flag", action="store_true", default=False)

    in_args = parser.parse_args()

    return in_args

# ====================================================================================================================

if __name__ == '__main__':

    in_args = vars(_get_parser())

    try:
        main(in_args)
    except:
        print('Files were not copied correctly')
        raise

#for ii in subject_keys
#subject_key_value, subject_value = _get_subject(cwd_path)

# sub-hfu073_ses-1_task-rest_acq-epi_bold.json
# sub-hfu073_ses-1_task-rest_acq-epi_bold.nii.gz
# sub-hfu073_ses-1_task-rest_acq-epi_events.tsv



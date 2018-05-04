#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A set of functions to facilitate the use of fmriprep.py from
Russ Poldrack's group.  https://fmriprep.readthedocs.io/en/latest/
"""

from typing import List, Union

import json
import pprint
import re
import os

from tic_core import operations


def read_json(filename:str, verbose: bool=False) -> dict:

    try:
        json_data = json.load(open(filename))

    except TypeError:
        print('TIC_PRIVATE_CONFIG_JSON configuration file not found \n {0} \n.'.format(filename))
        raise

    if verbose:
        pprint.pprint(json_data)

    return json_data


def create_echo_times_dict(echo_times: List[float] = [0.00492, 0.00738]):
    """
    Add Echo
    :param echo_times: A list of echo times in seconds.
    :return:
    """

    echo_time_dict = dict()

    for ii, ii_echo_time in enumerate(echo_times,1):
        echo_time_dict[f'EchoTime{ii}'] = ii_echo_time

    return echo_time_dict


def merge_dict_to_dict(a: dict, b: dict):
    """Merge two dictionaries."""
    c = dict(a)
    c.update(b)

    return c


def delete_key_from_dict(in_dict: dict, key_to_delete: Union[List[str], str]):

    assert isinstance(in_dict, dict)

    key_to_delete = operations.force_type_to_list(key_to_delete)

    for ii in key_to_delete:
        in_dict.pop(ii, None)

    return in_dict


def dict_to_json(in_dict: dict):
    """
    Converts dict to a json object
    :param in_dict:
    :return:

    https://stackoverflow.com/questions/26745519/converting-dictionary-to-json-in-python

    """

    return json.dumps(r)


def write_json_to_file_from_dict(in_dict, filename):
    """

    :param in_dict:
    :param filename:
    :return:

    This function is not doing what it is supposed to do.

    >> cat test_output.json

    "{\"Key1\": 1, \"Key2\": 2, \"Key3\": 3}"

    https://stackoverflow.com/questions/43823000/how-to-save-to-a-json-file-with-each-key-on-a-different-line
    https://stackoverflow.com/questions/12943819/how-to-prettyprint-a-json-file
    """

    parsed = json.dumps(in_dict)

    pprint.pprint(parsed)

    with open(filename, 'w') as outfile:
        outfile.write(json.dumps(parsed, indent=4, sort_keys=True, separators=(',', ': ')))


# ---------------------------------------------------------------------------------------------------------------------------------------------

def extract_confounds(in_filename, out_filename, confounds):
    """

    :param in_filename:
    :param out_filename:
    :param confounds:
    :return:
    """

    df_confounds = read_confounds(in_filename, confounds)
    write_confounds(df_confounds, out_filename)


def read_confounds(filename, confounds):
    """
    Read fmriprep confound file.

    :param filename:
    :param confounds:
    :return:
    """
    df_confounds = pandas.read_csv(filename, sep='\t', usecols=confounds)
    return df_confounds


def write_confounds(in_df, filename):

    in_df.to_csv(filename, index=False, float_format='%.6f')


def lstrip_to_ses_key(files):
    return [re.sub('^.+?ses-', 'ses-', os.path.abspath(x), 1) for x in files]


def print_intended_for_from_list(files):

    print(f'\n\n  "IntendedFor": ["{files[0]}",')

    for ii_file in files[1:-1]:
        print(f'                  "{ii_file}",')

    print(f'                 "{files[-1]}"],\n')


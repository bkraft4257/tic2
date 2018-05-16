#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""
import os
import json
import yaml
import pprint


def get_config(json_config=None):
    """
    Reads the TIC JSON Configuration file.

    :param json_config: The JSON configuration file which contains IP addresses, usernames, passwords,
    etc. necessary to connect to the databases and websites.  When json_config_file is None the environment variable
    TIC_CONFIG_JSON will be used for the json_config_file location.  Default is None.

    :return: dictionary containing the contents in the json_config_file.


    Example of the contents of JSON configuration file.

    {
     "sql_database_1": {"sql_server": "55.55.55.55",
                     "sql_port": 5555,
                     "sql_user": "user_john_doe",
                     "sql_password": "password_555",
                     "sql_database": "database_name"},

    "sql_database_1": {"sql_server": "152.11.202.184",
                       "sql_user": "user_john_doe",
                       "sql_password": "password_555",
                       "sql_instance": "sql_instance",
                       "sql_database": "database_name"},

    "website_1": {"user": "user_john_doe",
                 "password": "password_555"}
                 }

    """

    if json_config is None:
        json_config = os.environ.get('TIC_PRIVATE_CONFIG_JSON')
        print(json_config)

    else:
        if os.path.exists(json_config):
            json_config = json_config

        elif json_config in os.environ:
            json_config = os.environ.get(json_config)

    try:
        json_data = json.load(open(json_config))

    except TypeError:
        print('TIC_PRIVATE_CONFIG_JSON configuration file not found \n {0} \n.'.format(json_config))
        raise

    return json_data


def read_yaml(yaml_filename, verbose=False):
    """
    :param yaml_filename:  YAML input file for netprep workflow
    :param verbose:  boolean flag to dump out contents of YAML file to stdout.
    :return: cfg, a dictionary created from a safe_load of the specified YAML file.
    """
    with open(yaml_filename, 'r') as yaml_file:
        cfg = yaml.safe_load(yaml_file)

    if verbose:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(cfg)

    return cfg

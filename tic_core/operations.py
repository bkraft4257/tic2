#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A collection of functions for a variety of operations, which really didn't fit anywhere else.
"""

from collections import Iterable
import os
import sys
from typing import List


def force_type_to_list(parameter) -> List:
    """

    :param parameter: May be a scalar or a list.  If a scalar convert it to a list.
    :return:

    https://stackoverflow.com/questions/18864827/python-force-input-to-be-a-list
    """

    if not isinstance(parameter, Iterable) or isinstance(parameter, str):
        parameter = [parameter]

    return parameter


def make_directory(directory):
    """
    Make directories if they don't exist.

    :param directory: A string or list of strings to create directory.  Each string must be an absolute or relative path.
    :return:
    """

    for ii in force_type_to_list(directory):

        try:
            if not os.path.exists(ii):
                os.makedirs(ii)

        except:
            sys.exit(f'Unable to make directory {ii}')
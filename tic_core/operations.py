#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A collection of functions for a variety of operations, which really didn't fit anywhere else.
"""

from typing import List
from collections import Iterable


def force_type_to_list(parameter) -> List:
    """

    :param parameter: May be a scalar or a list.  If a scalar convert it to a list.
    :param basetype:
    :return:

    https://stackoverflow.com/questions/18864827/python-force-input-to-be-a-list
    """

    if not isinstance(parameter, Iterable) or isinstance(parameter, str):
        parameter = [parameter]

    return parameter

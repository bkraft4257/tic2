# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import os
import pytest

from tic_core import tic_io


TIC_PRIVATE_CONFIG_JSON = os.environ.get('TIC_PRIVATE_CONFIG_JSON')


def test_get_config_from_from():
    """
    Read the TIC private configuration file from a file. Filename is passed in as a string.
    Assume that if a dictionary is returned then assume that it was read in correctly.
    """
    json_config = tic_io.get_config(json_config=TIC_PRIVATE_CONFIG_JSON )
    assert isinstance(TIC_PRIVATE_CONFIG_JSON, str)
    assert isinstance(json_config, dict)


def test_get_config_from_environment_variable():
    """
    Read the TIC private configuration file from an environment variable passed in as a string.
    Assume that if a dictionary is returned then assume that it was read in correctly.
    """
    json_config = tic_io.get_config(json_config='TIC_PRIVATE_CONFIG_JSON')
    assert isinstance(json_config, dict)


def test_get_config_from_none():
    """
    """

    json_config = tic_io.get_config(json_config=None)
    assert isinstance(json_config, dict)


def test_get_config_file_does_not_exists():
    """
    """

    with pytest.raises(FileNotFoundError):
        tic_io.get_config(json_config='File_Does_Not_Exist')

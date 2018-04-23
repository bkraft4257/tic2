#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__version__ = "0.0.0"

from tic_core import tic_io


def get_webhook():
    """

    :return: Returns spot credentials for the individual user.
    """

    credentials = tic_io.get_config()
    print(credentials)

    return credentials['hfpef']['slack_webhook_url']
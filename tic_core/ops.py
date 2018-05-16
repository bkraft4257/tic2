#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""
import sys

BIDS_KEY_VALUE_SPLIT_ON = '-'


def clean_bids_key_value(key_value, key='sub', key_value_split_on=BIDS_KEY_VALUE_SPLIT_ON):

    n_split_characters = key_value.count(key_value_split_on)

    if n_split_characters == 0:
        out_key_value = f'{key}-{key_value}'

    elif n_split_characters == 1:
        out_key_value = key_value

    else:
        sys.exit(f'BIDS requires that there be only one {key_value_split_on}. \n Please check key-value pair {key_value}.')

    return out_key_value

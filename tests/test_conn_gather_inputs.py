# -*- coding: utf-8 -*-

"""
"""
import sys

from tic_core import tic_io
sys.path.append('/Users/bkraft/projects/tic_core/studies/mfc/scripts')

import conn_gather_inputs as conn_gi


def test_conn_gather_inputs_read_yaml():
    conn_inputs = tic_io.read_yaml('/Users/bkraft/projects/tic_core/tests/data/mfc/conn_gather_inputs_test.yaml', verbose=True)\

    print(conn_inputs['anat']['t1w'])


def test_conn_gather_inputs_read_yaml_from_main():
    conn_inputs = conn_gi.main()

    print(conn_inputs['anat']['t1w'])
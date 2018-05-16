
import pytest
import os
from tic_core import ops


def test_clean_bids_key_value_with_sub_key():
    """
    """

    returned_value = ops.clean_bids_key_value('sub-hfs001', key='sub')

    assert returned_value == 'sub-hfs001'


def test_clean_bids_key_value_without_sub_key():
    """
    """

    returned_value = ops.clean_bids_key_value('hfs001', key='sub')

    assert returned_value == 'sub-hfs001'


def test_clean_bids_key_value_with_two_key_value_splitters():
    """
    """

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        ops.clean_bids_key_value('sub-sub-hfs001', key='sub')
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 42


def test_clean_bids_key_value_without_ses_key():
    """
    """

    returned_value = ops.clean_bids_key_value('1', key='ses')

    assert returned_value == 'ses-1'


def test_clean_bids_key_value_with_ses_key():
    """
    """

    returned_value = ops.clean_bids_key_value('ses-1', key='ses')

    assert returned_value == 'ses-1'

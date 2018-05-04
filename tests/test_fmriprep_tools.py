#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import pytest
import pprint
import os

from tic_core import fmriprep_tools


def test_read_json():
    fmriprep_json = fmriprep_tools.read_json('./data/sub-mfc901_ses-1_acq-pre_phasediff.json', verbose=True)
    assert isinstance(fmriprep_json, dict)


def test_create_echo_times_dict():
    result = fmriprep_tools.create_echo_times_dict()
    assert {'EchoTime1': 0.00492, 'EchoTime2': 0.00738} == result


def test_merge_dict_to_dict():
    result = fmriprep_tools.merge_dict_to_dict({'Key1': 1, 'Key2': 2},
                                               {'Key3': 3, 'Key4': 4})

    assert {'Key1': 1, 'Key2': 2, 'Key3': 3, 'Key4': 4} == result


@pytest.mark.parametrize("test_input,expected", [('Key1', {'Key2': 2, 'Key3': 3}),
                                                 ('Key2', {'Key1': 1, 'Key3': 3}),
                                                 ('Key3', {'Key1': 1, 'Key2': 2}),
                                                 ('Unknown Key', {'Key1': 1, 'Key2': 2, 'Key3': 3})])
def test_delete_key_from_dict_existing_key(test_input, expected):

    in_dict = {'Key1':  1, 'Key2': 2, 'Key3': 3}

    out_dict = fmriprep_tools.delete_key_from_dict(in_dict, test_input)

    assert expected == out_dict


def test_delete_key_from_dict_not_a_dictionary():

    with pytest.raises(AssertionError):
        fmriprep_tools.delete_key_from_dict([1,2,3], 'Key 1')


def test_write_json_to_file_from_dict():
    fmriprep_tools.write_json_to_file_from_dict({'Key1':  1, 'Key2': 2, 'Key3': 3}, 'test_output.json')


def test_strip_func_from_string():

    files = ["/bkraft1/studies/mfc/bids/sub-mfc006/ses-1/fmap/../func/sub-mfc006_ses-1_task-preHeat2_acq-epi_rec-fmap_bold.nii.gz",
             "/bkraft1/studies/mfc/bids/sub-mfc006/ses-1/fmap/../func/sub-mfc006_ses-1_task-postHeat4_acq-epi_rec-fmap_bold.nii.gz",
             "/bkraft1/studies/mfc/bids/sub-mfc006/ses-1/fmap/../func/sub-mfc006_ses-1_task-postNeutral4_acq-epi_rec-fmap_bold.nii.gz",
             "/bkraft1/studies/mfc/bids/sub-mfc006/ses-1/fmap/../func/sub-mfc006_ses-1_task-preHeat1_acq-epi_rec-fmap_bold.nii.gz",
             "/bkraft1/studies/mfc/bids/sub-mfc006/ses-1/fmap/../func/sub-mfc006_ses-1_task-postHeat3_acq-epi_rec-fmap_bold.nii.gz",
             "/bkraft1/studies/mfc/bids/sub-mfc006/ses-1/fmap/../func/sub-mfc006_ses-1_task-preNeutral2_acq-epi_rec-fmap_bold.nii.gz",
             "/bkraft1/studies/mfc/bids/sub-mfc006/ses-1/fmap/../func/sub-mfc006_ses-1_task-preNeutral1_acq-epi_rec-fmap_bold.nii.gz",
             "/bkraft1/studies/mfc/bids/sub-mfc006/ses-1/fmap/../func/sub-mfc006_ses-1_task-postNeutral3_acq-epi_rec-fmap_bold.nii.gz"]

    stripped_files = fmriprep_tools.strip_func_from_string(files)

    print(stripped_files)

def test_print_intended_for_from_list():

    files = ["ses-1/func/sub-mfc006_ses-1_task-preHeat2_acq-epi_rec-fmap_bold.nii.gz",
             "ses-1/func/sub-mfc006_ses-1_task-postHeat4_acq-epi_rec-fmap_bold.nii.gz",
             "ses-1/func/sub-mfc006_ses-1_task-postNeutral4_acq-epi_rec-fmap_bold.nii.gz",
             "ses-1/func/sub-mfc006_ses-1_task-preHeat1_acq-epi_rec-fmap_bold.nii.gz",
             "ses-1/func/sub-mfc006_ses-1_task-postHeat3_acq-epi_rec-fmap_bold.nii.gz",
             "ses-1/func/sub-mfc006_ses-1_task-preNeutral2_acq-epi_rec-fmap_bold.nii.gz",
             "ses-1/func/sub-mfc006_ses-1_task-preNeutral1_acq-epi_rec-fmap_bold.nii.gz",
             "ses-1/func/sub-mfc006_ses-1_task-postNeutral3_acq-epi_rec-fmap_bold.nii.gz"]

    fmriprep_tools.print_intended_for_from_list(files)


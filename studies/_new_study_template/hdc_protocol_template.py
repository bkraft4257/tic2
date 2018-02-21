import os

"""
heudiconv template protocol file. 

This template file can be used as an example and starting point for creating your own protocol files.  


"""

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    """
    Create key for HDC DICOM to NIFTI conversion

    DO NOT MODIFY

    :param template:
    :param outtype:
    :param annotation_classes:
    :return:
    """

    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group


    The namedtuple `s` contains the following fields:

    * total_files_till_now
    * example_dcm_file
    * series_id
    * dcm_dir_name
    * unspecified2
    * unspecified3
    * dim1
    * dim2
    * dim3
    * dim4
    * TR
    * TE
    * protocol_name
    * is_motion_corrected
    * is_derived
    * patient_id
    * study_description
    * referring_physician_name
    * series_description
    * image_type

    Below is an example of the output from the iMove study

    >>> csvcut -c 4,21,8,9,10,11,12,13,15 dicominfo_ses-1.csv | csvlook

    | ----------------------------| ------------- | ---- | ---- | ---- | ---- | ----- | ------ | ------------------- |
    | series_id                   | sequence_name | dim1 | dim2 | dim3 | dim4 |    TR |     TE | is_motion_corrected |
    | 2-MPRAGE_GRAPPA2            | *tfl3d1_16ns  |  256 |  240 |  192 |    1 | 2.300 |   2.98 |               False |
    | 3-BOLD_resting 4X4X4 A>>P   | *epfid2d1_64  |   64 |   64 |   35 |  190 | 2.000 |  25.00 |               False |
    | 4-rest_topup_A>>P           | *epse2d1_64   |   64 |   64 |  140 |    1 | 2.400 |  38.00 |               False |
    | 5-rest_topup_P>>A           | *epse2d1_64   |   64 |   64 |  140 |    1 | 2.400 |  38.00 |               False |
    | 6-Field_mapping 4X4X4 A>>P  | *fm2d2r       |   64 |   64 |   35 |    1 | 0.488 |   4.92 |               False |
    | 7-Field_mapping 4X4X4 A>>P  | *fm2d2r       |   64 |   64 |   35 |    1 | 0.488 |   7.38 |               False |


    """

    # Create a key for each DICOM file to convert.  The key tells HDC where and how to name the converted DICOM file.
    # The naming convention is very strict. The rules are established by BIDS  http://bids.neuroimaging.io/
    #
    #  anat, func, fmap are established directories where the data can reside.
    #
    #  {subject} is the variable which will be replaced by the subject's acrostic
    #
    #  {acq} is the acquisition value
    #
    #  {item:02d} is the item counter padded by two zeros.  This allows HDC to create a unique name if it finds
    #             multiple images that meet your criteria.  We recommend that only one DICOM image should match your
    #             criteria for data conversion. However, this can not happen if the scan is repeated.
    #

    t1 = create_key('anat/sub-{subject}_run-{item:02d}_T1w')
    rest_fmri_ap = create_key('func/sub-{subject}_dir-ap_task-rest_run-{item:02d}_bold')
    rest_topup_ap = create_key('func/sub-{subject}_dir-ap_run-{item:02d}_bold')
    rest_topup_pa = create_key('func/sub-{subject}_dir-pa_run-{item:02d}_bold')
    fmap_rest_magnitude1 = create_key('fmap/sub-{subject}_run-{item:02d}_magnitude1')
    fmap_rest_phasediff = create_key('fmap/sub-{subject}_run-{item:02d}_phasediff')

    # Create an empty dictionary called info for each key

    info = {t1: [],
            rest_fmri_ap: [],
            rest_topup_ap: [],
            rest_topup_pa: [],
            fmap_rest_magnitude1: [],
            fmap_rest_phasediff: [],
            }

    # Loop over each sequence. Use if statements to determine which sequences should be linked to which key

    for idx, s in enumerate(seqinfo):

        if (('MPRAGE_GRAPPA2' in s.series_id) and
                ('tfl3d1_16ns' in s.sequence_name) and
                (s.dim3 == 192) and
                (s.dim4 == 1)):
                info[t1] = [s.series_id]

        if (('BOLD_resting 4X4X4 A>>P' in s.series_id) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim3 == 35) and
                (s.dim4 == 190)):
                info[rest_fmri_ap] = [s.series_id]

        if (('rest_topup_A>>P' in s.series_id) and
                ('epse2d1_64' in s.sequence_name) and
                (s.dim3 == 140) and
                (s.dim4 == 1)):
                info[rest_topup_ap] = [s.series_id]

        if (('rest_topup_P>>A' in s.series_id) and
                ('epse2d1_64' in s.sequence_name) and
                (s.dim3 == 140) and
                (s.dim4 == 1)):
                info[rest_topup_pa] = [s.series_id]

        if (('Field_mapping 4X4X4 A>>P' in s.series_id) and
                ('fm2d2r' in s.sequence_name) and
                (s.dim3 == 35) and
                (s.dim4 == 1) and
                (s.TE == 4.92)):
                info[fmap_rest_magnitude1] = [s.series_id]

        if (('Field_mapping 4X4X4 A>>P' in s.series_id) and
                ('fm2d2r' in s.sequence_name) and
                (s.dim3 == 35) and
                (s.dim4 == 1) and
                (s.TE == 7.38)):
                info[fmap_rest_phasediff] = [s.series_id]

    return info

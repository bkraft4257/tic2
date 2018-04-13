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


    key-value tags
    --------------

    BIDS uses a key-value pairs in the naming convention.  The sub-<participant_label> is a required field. It is used
    to create a subject specific directory in the BIDS directory.

    It must also be included in each and every filename. The ses-<session_label> is a bug the <session_label> includes
    the key.  This means that {session} translates to
    ses-<session-label>.

    Only certain keys are associated with each imaging modality.
    key-value pairs are in [] are optional.  If a key-value pair is not in [] then it must be included in the name.
    For example every filename must include sub-<participant_label> to be BIDS compliant.  The session key-value
    is optional. However, if you include session key-value in the path then you must also include it in the
    filename.

    Another example of required and optional key-value pairs is in the FUNC images.  Here is the key-value
    pairs taken from the BIDS documentation for images in the func directory.

     _task-<task_label>[_acq-<label>][_rec-<label>][_run-<index>][_echo-<index>]_bold

     You can see that task-<task_label> is not in [] so it is required. While _acq-<acq_label> is in [] and is
     therefore optional.

     Below I have included some notes for the key-value pairs for the different imaging modalities and BIDS
     sub-directories.


    common key-value tags:

        sub-<participant_label>/[ses-<session_label>/]/<dir>/sub-<participant_label>[_ses-<session_label>]

        <dir> = anat, func, fmap, dwi, swi

        {participant_label} is the variable which will be replaced by the subject's acrostic

        {session_label} is the variable which will be replaced by the session value key.  {session} is inconsistent
                        and is replaced by the key and it's value. An example, should help clarify this inconsistency
                        {session} is replaced by ses-{session_id}.

        {acq} is the acquisition value

        {item:01d} is the item counter padded by two zeros.  This allows HDC to create a unique name if it finds
                  multiple images that meet your criteria.  We recommend that only one DICOM image should match your
                  criteria for data conversion. However, this can not happen if the scan is repeated.

    anat key-value tags:

        [_acq-<label>][_ce-<label>][_rec-<label>][_run-<index>]<modality_label>.nii[.gz]
        [_acq-<label>][_ce-<label>][_rec-<label>][_run-<index>][_mod-<label>]_defacemask.nii[.gz]


        Imaging Type/Name,       modality_label
        T1 weighted              T1w
        T2 weighted              T2w
        T1 Rho map               T1rho
        T1 map                   T1map
        T2 map                   T2map
        T2*                      T2star
        FLAIR                    FLAIR
        FLASH                    FLASH
        Proton density           PD
        Proton density map       PDmap
        Combined PD/T2           PDT2
        Inplane T1               inplaneT1
        Inplane T2               inplaneT2
        Angiography              angio



    func/ _task-<task_label>[_acq-<label>][_rec-<label>][_run-<index>][_echo-<index>]_bold

    fmap/  [_acq-<label>][_run-<run_index>]_phasediff
           [_acq-<label>][_run-<run_index>]_magnitude1

           [_acq-<label>]_dir-<dir_label>[_run-<run_index>]_epi

    dwi/   [_acq-<label>][_run-<index>]_dwi
           [_acq-<label>][_run-<index>]_sbref

    swi/  [_acq-<label>][_rec-<label>]_part-<phase|mag>[_coil-<index>][_echo-<index>][_run-<index>]_GRE.nii[.gz]

        https://docs.google.com/document/d/1kyw9mGgacNqeMbp4xZet3RnDhcMmf4_BmRgKaOkO2Sc/edit


    asl/  _task-<task_label>[_acq-<label>][_rec-<label>][_run-<index>]_asl.nii[.gz]

        https://docs.google.com/document/d/15tnn5F10KpgHypaQJNNGiNKsni9035GtDqJzWqkkP6c/edit#heading=h.mqkmyp254xh6

    """
    
    """
    MCF Pilot Protocol acquired on Friday April 13th
    
                                   series_id sequence_name          series_description  dim1  dim2  dim3  dim4     TR     TE  is_derived  is_motion_corrected
        0                    1-localizer        *fl2d1                   localizer   192   192     3     1  0.020   5.00       False                False
        1           2-pre_epi_A>>P 4X4X4  *epfid2d1_64          pre_epi_A>>P 4X4X4    64    64    35   177  2.000  25.00       False                False
        2     3-pre+heat1_epi_A>>P 4X4X4  *epfid2d1_64    pre+heat1_epi_A>>P 4X4X4    64    64    35   177  2.000  25.00       False                False
        3     4-pre+heat2_epi_A>>P 4X4X4  *epfid2d1_64    pre+heat2_epi_A>>P 4X4X4    64    64    35   177  2.000  25.00       False                False
        4               5-pre_topup_A>>P   *epse2d1_64              pre_topup_A>>P    64    64   140     1  2.400  38.00       False                False
        5               6-pre_topup_P>>A   *epse2d1_64              pre_topup_P>>A    64    64   140     1  2.400  38.00       False                False
        6     7-Field_mapping 4X4X4 A>>P       *fm2d2r    Field_mapping 4X4X4 A>>P    64    64    35     1  0.488   4.92       False                False
        7     8-Field_mapping 4X4X4 A>>P       *fm2d2r    Field_mapping 4X4X4 A>>P    64    64    35     1  0.488   7.38       False                False
        8               9-MPRAGE_GRAPPA2  *tfl3d1_16ns              MPRAGE_GRAPPA2   256   240   192     1  2.300   2.98       False                False
        9   10-post+heat3_epi_A>>P 4X4X4  *epfid2d1_64   post+heat3_epi_A>>P 4X4X4    64    64    35   144  2.000  25.00       False                False
        10  11-post+heat4_epi_A>>P 4X4X4  *epfid2d1_64   post+heat4_epi_A>>P 4X4X4    64    64    35   144  2.000  25.00       False                False
        11        12-post_epi_A>>P 4X4X4  *epfid2d1_64         post_epi_A>>P 4X4X4    64    64    35   144  2.000  25.00       False                False
        12            13-post_topup_A>>P   *epse2d1_64             post_topup_A>>P    64    64   140     1  2.400  38.00       False                False
        13            14-post_topup_P>>A   *epse2d1_64             post_topup_P>>A    64    64   140     1  2.400  38.00       False                False
        14       15-mbep2d_bold 3mm L>>R   epfid2d1_64  mbep2d_bold 3mm L>>R_SBRef    72    64    64     1  1.090  30.00       False                False
        15       16-mbep2d_bold 3mm L>>R   epfid2d1_64        mbep2d_bold 3mm L>>R    72    64    64   263  1.090  30.00       False                False
    """

    pre_rest_ap = create_key('func/sub-{subject}_{session}_task-preRest_run-{item:02d}_bold')
    pre_heat1_ap = create_key('func/sub-{subject}_{session}_task-preHeat1_run-{item:02d}_bold')
    pre_heat2_ap = create_key('func/sub-{subject}_{session}_task-preHeat2_run-{item:02d}_bold')

    pre_topup_ap = create_key('fmap/sub-{subject}_{session}_acq-pre_dir-ap_run-{item:02d}_bold')
    pre_topup_pa = create_key('fmap/sub-{subject}_{session}_acq-pre_dir-pa_run-{item:02d}_bold')
    
    pre_fmap_magnitude1 = create_key('fmap/sub-{subject}_{session}_run-{item:02d}_magnitude1')
    pre_fmap_phasediff = create_key('fmap/sub-{subject}_{session}_run-{item:02d}_phasediff')

    t1w = create_key('anat/sub-{subject}_{session}_run-{item:02d}_T1w')

    post_heat1_ap = create_key('func/sub-{subject}_{session}_task-postHeat3_run-{item:02d}_bold')
    post_heat2_ap = create_key('func/sub-{subject}_{session}_task-postHeat4_run-{item:02d}_bold')
    post_rest_ap = create_key('func/sub-{subject}_{session}_task-postRest_run-{item:02d}_bold')

    post_topup_ap = create_key('fmap/sub-{subject}_acq-post_dir-ap_run-{item:02d}_bold')
    post_topup_pa = create_key('fmap/sub-{subject}_acq-post_dir-pa_run-{item:02d}_bold')

    post_fmap_magnitude1 = create_key('fmap/sub-{subject}_{session}_acq-post_run-{item:02d}_magnitude1')
    post_fmap_phasediff = create_key('fmap/sub-{subject}_{session}_acq-post_run-{item:02d}_phasediff')

    post_rest_ap_mbepi = create_key('func/sub-{subject}_{session}_task-postRest_acq-mbepi_run-{item:02d}_bold')
    post_rest_ap_mbepi_sbref = create_key('func/sub-{subject}_{session}_task-postRest_acq-mbepi_run-{item:02d}_sbref')

    # Create an empty dictionary called info for each key

    info = {pre_rest_ap: [],
            pre_heat1_ap: [],
            pre_heat2_ap: [],

            pre_topup_ap: [],
            pre_topup_pa: [],

            pre_fmap_magnitude1: [],
            pre_fmap_phasediff: [],

            t1w: [],

            post_heat1_ap: [],
            post_heat2_ap: [],
            post_rest_ap: [],

            post_topup_ap: [],
            post_topup_pa: [],
            post_fmap_magnitude1: [],
            post_fmap_phasediff: [],
            
            post_rest_ap_mbepi: [],
            post_rest_ap_mbepi_sbref: []
            }

    # Loop over each sequence. Use if statements to determine which sequences should be linked to which key

    for idx, s in enumerate(seqinfo):

        if 'pre_epi' in s.series_id:
                info[pre_rest_ap] = [s.series_id]

        if 'pre+heat1' in s.series_id:
                info[pre_heat1_ap] = [s.series_id]

        if 'pre+heat2' in s.series_id:
                info[pre_heat2_ap] = [s.series_id]

        if 'pre_topup_A>>P' in s.series_id:
            info[pre_topup_ap] = [s.series_id]

        if 'pre_topup_P>>A' in s.series_id:
            info[pre_topup_pa] = [s.series_id]

        if (('Field_mapping 4X4X4 A>>P' in s.series_id) and
                (s.TE == 4.92)):
                info[pre_fmap_phasediff] = [s.series_id]
            
        if (('Field_mapping 4X4X4 P>>A' in s.series_id) and
                (s.TE == 7.38)):
                info[pre_fmap_phasediff] = [s.series_id]

        if 'MPRAGE_GRAPPA2' in s.series_id:
            info[t1w] = [s.series_id]

        if 'post_epi' in s.series_id:
                info[post_rest_ap] = [s.series_id]

        if 'post+heat1' in s.series_id:
                info[post_heat1_ap] = [s.series_id]

        if 'post+heat2' in s.series_id:
                info[post_heat2_ap] = [s.series_id]

        if 'post_topup_A>>P' in s.series_id:
            info[post_topup_ap] = [s.series_id]

        if 'post_topup_P>>A' in s.series_id:
            info[post_topup_pa] = [s.series_id]

        if 'mbep2d_bold 3mm L>>R_SBRef' in s.series_id:
            info[post_rest_ap_mbepi_sbref] = [s.series_id]

        if 'mbep2d_bold 3mm L>>R ' in s.series_id:
            info[post_rest_ap_mbepi] = [s.series_id]

    return info

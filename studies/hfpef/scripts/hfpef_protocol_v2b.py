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

    $> csvcut -c 4,20,21,8,9,10,11,12,13,15,16 dicominfo_ses-1.csv | csvlook

    | series_id | series_description                          | sequence_name | dim1 | dim2 | dim3 | dim4 |     TR |     TE | is_motion_corrected | is_derived |
    | ----------| ------------------------------------------- | ------------- | ---- | ---- | ---- | ---- | ------ | ------ | ------------------- | ---------- |
    |  2 - ...  | MPRAGE_GRAPPA2                              | *tfl3d1_16ns  |  256 |  240 |  192 |    1 |  2.300 |   2.98 |               False |      False |
    |  3 - ...  | pcasl_wfu_4_0C R>>L EYES OPEN               | epfid2d1_56   |   70 |   56 |   43 |   81 |  4.000 |  11.00 |               False |      False |
    |  4 - ...  | Perfusion_Weighted                          | epfid2d1_56   |   70 |   56 |   43 |    1 |  4.000 |  11.00 |               False |       True |
    |  5 - ...  | pcasl_wfu_4_0C L>>R (COPY SLICES FROM R>>L) | epfid2d1_56   |   70 |   56 |   43 |    3 |  4.000 |  11.00 |               False |      False |
    |  6 - ...  | Perfusion_Weighted                          | epfid2d1_56   |   70 |   56 |   43 |    1 |  4.000 |  11.00 |               False |       True |
    |  7 - ...  | T2 FLAIR SPACE NEW                          | *spcir_192ns  |  256 |  236 |  192 |    1 |  5.000 | 383.00 |               False |      False |
    |  8 - ...  | mbep2d_bold 3mm L>>R                        | epfid2d1_64   |   72 |   64 |   64 |   10 |  0.570 |  30.00 |               False |      False |
    |  9 - ...  | MoCoSeries                                  | epfid2d1_64   |   72 |   64 |   64 |   10 |  0.570 |  30.00 |                True |      False |
    | 10 - ...  | mbep2d_bold 3mm R>>L (copy from bold L>>R)  | epfid2d1_64   |   72 |   64 |   64 |  500 |  0.570 |  30.00 |               False |      False |
    | 11 - ...  | MoCoSeries                                  | epfid2d1_64   |   72 |   64 |   64 |  500 |  0.570 |  30.00 |                True |      False |
    | 12 - ...  | BOLD_resting 4X4X4 A>>P                     | *epfid2d1_64  |   64 |   64 |   35 |  190 |  2.000 |  25.00 |               False |      False |
    | 13 - ...  | rest_topup_A>>P                             | *epse2d1_64   |   64 |   64 |  140 |    1 |  2.000 |  25.00 |               False |      False |
    | 14 - ...  | rest_topup_P>>A                             | *epse2d1_64   |   64 |   64 |  140 |    1 |  2.000 |  25.00 |               False |      False |
    | 15 - ...  | Field_mapping 4X4X4 A>>P                    | *fm2d2r       |   64 |   64 |   35 |    1 |  0.488 |   4.92 |               False |      False |
    | 16 - ...  | Field_mapping 4X4X4 A>>P                    | *fm2d2r       |   64 |   64 |   35 |    1 |  0.488 |   7.38 |               False |      False |
    | 17 - ...  | DTI_30dir_1b0 A>>P                          | *ep_b0        |  112 |  112 |   60 |   31 |  8.500 |  82.00 |               False |      False |
    | 18 - ...  | DTI_30dir_1b0 A>>P_ADC                      | *ep_b0_1000   |  112 |  112 |   60 |    1 |  8.500 |  82.00 |               False |       True |
    | 19 - ...  | DTI_30dir_1b0 A>>P_TRACEW                   | *ep_b1000t    |  112 |  112 |   60 |    1 |  8.500 |  82.00 |               False |       True |
    | 20 - ...  | DTI_30dir_1b0 A>>P_FA                       | *ep_b0_1000   |  112 |  112 |   60 |    1 |  8.500 |  82.00 |               False |       True |
    | 21 - ...  | DTI_30dir_1b0 A>>P_ColFA                    | Not found     |  112 |  112 |   60 |    1 | -1.000 |  -1.00 |               False |       True |
    | 23 - ...  | DTI_30dir_1b0 P>>A                          | *ep_b0        |  112 |  112 |   60 |    1 |  8.500 |  82.00 |               False |      False |
    | 24 - ...  | pcasl_wfu_4_0C 3min highCO2                 | epfid2d1_64   |   64 |   64 |   28 |  107 |  4.000 |  12.00 |               False |      False |
    | 25 - ...  | Perfusion_Weighted                          | epfid2d1_64   |   64 |   64 |   28 |    1 |  4.000 |  12.00 |               False |       True |


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

    #    HFPEF Protocol Session 1
    #    ------------------------
    #                                          series_id sequence_name  dim1  dim2  dim3  dim4     TR      TE  is_derived  is_motion_corrected
    #    0                              2-MPRAGE_GRAPPA2  *tfl3d1_16ns   256   240   192     1  2.300    2.98       False                False
    #    1                        3-mbep2d_bold 3mm L>>R   epfid2d1_64    72    64    64     1  0.570   30.00       False                False
    #    2                        4-mbep2d_bold 3mm L>>R   epfid2d1_64    72    64    64    10  0.570   30.00       False                False
    #    3                        5-mbep2d_bold 3mm R>>L   epfid2d1_64    72    64    64     1  0.570   30.00       False                False
    #    4                        6-mbep2d_bold 3mm R>>L   epfid2d1_64    72    64    64   500  0.570   30.00       False                False
    #    5                          7-T2 FLAIR SPACE NEW  *spcir_192ns   256   236   192     1  5.000  395.00       False                False
    #    6                     8-BOLD_resting 4X4X4 A>>P  *epfid2d1_64    64    64    35   190  2.000   25.00       False                False
    #    7                             9-rest_topup_A>>P   *epse2d1_64    64    64   140     1  2.000   25.00       False                False
    #    8                            10-rest_topup_P>>A   *epse2d1_64    64    64   140     1  2.000   25.00       False                False
    #    9                   11-Field_mapping 4X4X4 A>>P       *fm2d2r    64    64    35     1  0.488    4.92       False                False
    #    10                  12-Field_mapping 4X4X4 A>>P       *fm2d2r    64    64    35     1  0.488    7.38       False                False
    #    11              13-pcasl_wfu_3_1 R>>L EYES OPEN   epfid2d1_56    70    56    43    81  4.000   11.00       False                False
    #    15  17-pcasl_wfu_3_1 L>>R (COPY SLICES FROM R>L   epfid2d1_56    70    56    43     3  4.000   11.00       False                False
    #    19                        21-DTI_30dir_1b0 A>>P        *ep_b0   112   112    60    31  8.500   82.00       False                False
    #    24                        27-DTI_30dir_1b0 P>>A        *ep_b0   112   112    60     1  8.500   82.00       False                False
    #
    #    HFPEF Protocol Session 2
    #    ------------------------
    #   | series_id | series_description                          | sequence_name | dim1 | dim2 | dim3 | dim4 |     TR |     TE | is_motion_corrected | is_derived |
    #   | ----------| ------------------------------------------- | ------------- | ---- | ---- | ---- | ---- | ------ | ------ | ------------------- | ---------- |
    #   |  2 - ...  | MPRAGE_GRAPPA2                              | *tfl3d1_16ns  |  256 |  240 |  192 |    1 |  2.300 |   2.98 |               False |      False |
    #
    #   |  3 - ...  | pcasl_wfu_4_0C R>>L EYES OPEN               | epfid2d1_56   |   70 |   56 |   43 |   81 |  4.000 |  11.00 |               False |      False |
    #   |  4 - ...  | Perfusion_Weighted                          | epfid2d1_56   |   70 |   56 |   43 |    1 |  4.000 |  11.00 |               False |       True |
    #   |  5 - ...  | pcasl_wfu_4_0C L>>R (COPY SLICES FROM R>>L) | epfid2d1_56   |   70 |   56 |   43 |    3 |  4.000 |  11.00 |               False |      False |
    #   |  6 - ...  | Perfusion_Weighted                          | epfid2d1_56   |   70 |   56 |   43 |    1 |  4.000 |  11.00 |               False |       True |
    #
    #   |  7 - ...  | T2 FLAIR SPACE NEW                          | *spcir_192ns  |  256 |  236 |  192 |    1 |  5.000 | 383.00 |               False |      False |
    #
    #   |  8 - ...  | mbep2d_bold 3mm L>>R                        | epfid2d1_64   |   72 |   64 |   64 |   10 |  0.570 |  30.00 |               False |      False |
    #   |  9 - ...  | MoCoSeries                                  | epfid2d1_64   |   72 |   64 |   64 |   10 |  0.570 |  30.00 |                True |      False |
    #   | 10 - ...  | mbep2d_bold 3mm R>>L (copy from bold L>>R)  | epfid2d1_64   |   72 |   64 |   64 |  500 |  0.570 |  30.00 |               False |      False |
    #   | 11 - ...  | MoCoSeries                                  | epfid2d1_64   |   72 |   64 |   64 |  500 |  0.570 |  30.00 |                True |      False |
    #
    #   | 12 - ...  | BOLD_resting 4X4X4 A>>P                     | *epfid2d1_64  |   64 |   64 |   35 |  190 |  2.000 |  25.00 |               False |      False |
    #   | 13 - ...  | rest_topup_A>>P                             | *epse2d1_64   |   64 |   64 |  140 |    1 |  2.000 |  25.00 |               False |      False |
    #   | 14 - ...  | rest_topup_P>>A                             | *epse2d1_64   |   64 |   64 |  140 |    1 |  2.000 |  25.00 |               False |      False |
    #
    #   | 15 - ...  | Field_mapping 4X4X4 A>>P                    | *fm2d2r       |   64 |   64 |   35 |    1 |  0.488 |   4.92 |               False |      False |
    #   | 16 - ...  | Field_mapping 4X4X4 A>>P                    | *fm2d2r       |   64 |   64 |   35 |    1 |  0.488 |   7.38 |               False |      False |
    #
    #   | 17 - ...  | DTI_30dir_1b0 A>>P                          | *ep_b0        |  112 |  112 |   60 |   31 |  8.500 |  82.00 |               False |      False |
    #   | 18 - ...  | DTI_30dir_1b0 A>>P_ADC                      | *ep_b0_1000   |  112 |  112 |   60 |    1 |  8.500 |  82.00 |               False |       True |
    #   | 19 - ...  | DTI_30dir_1b0 A>>P_TRACEW                   | *ep_b1000t    |  112 |  112 |   60 |    1 |  8.500 |  82.00 |               False |       True |
    #   | 20 - ...  | DTI_30dir_1b0 A>>P_FA                       | *ep_b0_1000   |  112 |  112 |   60 |    1 |  8.500 |  82.00 |               False |       True |
    #   | 21 - ...  | DTI_30dir_1b0 A>>P_ColFA                    | Not found     |  112 |  112 |   60 |    1 | -1.000 |  -1.00 |               False |       True |
    #   | 23 - ...  | DTI_30dir_1b0 P>>A                          | *ep_b0        |  112 |  112 |   60 |    1 |  8.500 |  82.00 |               False |      False |

    #   | 24 - ...  | pcasl_wfu_4_0C 3min highCO2                 | epfid2d1_64   |   64 |   64 |   28 |  107 |  4.000 |  12.00 |               False |      False |
    #   | 25 - ...  | Perfusion_Weighted                          | epfid2d1_64   |   64 |   64 |   28 |    1 |  4.000 |  12.00 |               False |       True |

    # region --- create_keys
    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w.{item:01d}')
    flair = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_FLAIR.{item:01d}')

    rest_mbepi = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-mbepi_bold.{item:01d}')
    rest_mbepi_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-mbepi_sbref.{item:01d}')

    rest_mbepi_topup_rl = create_key('sub-{subject}/{session}//fmap/sub-{subject}_{session}_'
                                     'acq-mbepi_dir-rl_epi.{item:01d}')

    rest_mbepi_topup_lr = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}'
                                     '_acq-mbepi_dir-lr_epi.{item:01d}')

    rest_epi_topup = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest'
                                '_acq-epi_rec-topup_bold.{item:01d}')

    rest_epi_topup_ap = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-epse_dir-ap_epi.{item:01d}')

    rest_epi_topup_pa = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest'
                                   '_acq-epi_rec-fmap_bold.{item:01d}')

    rest_epi_fmap = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest'
                               '_acq-epi_rec-fmap_bold.{item:01d}')

    fmap_magnitude1 = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-bold_magnitude1.{item:01d}')

    fmap_phasediff = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-bold_phasediff.{item:01d}')

    pcasl_lr_high_co2 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest'
                                   '_acq-pcasl_bold.{item:01d}')

    pcasl_rl_rest = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-pcasl_dir-rl_epi.{item:01d}')

    pcasl_topup_rl = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-pcasl_dir-rl_epi.{item:01d}')

    pcasl_topup_lr = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-pcasl_dir-lr_epi.{item:01d}')

    dti_30dir_ap = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-30ap_dwi.{item:01d}')

    dti_30dir_topup_ap = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}'
                                    '_acq-30ap_dir-ap_epi.{item:01d}')

    dti_30dir_topup_pa = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}'
                                    '_acq-30ap_dir-pa_epi.{item:01d}')

    # endregion

    # region --- create info dictionary
    # Create an empty dictionary called info for each key

    info = {t1: [],
            flair: [],

            rest_mbepi: [],
            rest_mbepi_sbref: [],

            rest_mbepi_topup_rl: [],
            rest_mbepi_topup_lr: [],

            rest_epi_topup: [],
            rest_epi_topup_ap: [],
            rest_epi_topup_pa: [],

            rest_epi_fmap: [],
            fmap_magnitude1: [],
            fmap_phasediff: [],

            pcasl_lr_high_co2: [],
            pcasl_rl_rest: [],
            pcasl_topup_rl: [],
            pcasl_topup_lr: [],

            dti_30dir_ap: [],
            dti_30dir_topup_ap: [],
            dti_30dir_topup_pa: [],
            }
    # endregion

    # Loop over each sequence. Use if statements to determine which sequences should be linked to which key

    for idx, s in enumerate(seqinfo):

        # Anat images

        if (('MPRAGE_GRAPPA2' in s.series_description) and
                ('tfl3d1_16ns' in s.sequence_name)):
            info[t1] = [s.series_id]

        if (('T2 FLAIR SPACE' in s.series_description) and
                ('spcir_192ns' in s.sequence_name)):
            info[flair] = [s.series_id]

        # Multiband EPI Rest

        if (('mbep2d_bold 3mm R>>L' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim4 == 500)):
            info[rest_mbepi] = [s.series_id]

        if (('mbep2d_bold 3mm L>>R_SBRef' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim4 == 1)):
            info[rest_mbepi_sbref] = [s.series_id]

        if (('mbep2d_bold 3mm L>>R' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim4 == 10)):
            info[rest_mbepi_topup_lr] = [s.series_id]

        if (('mbep2d_bold 3mm R>>L' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim4 == 500)):
            info[rest_mbepi_topup_rl] = [s.series_id]

        # EPI Rest with TOPUP correction

        if (('BOLD_resting 4X4X4 A>>P' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim4 == 190)):
            info[rest_epi_topup] = [s.series_id]

        if (('rest_topup_A>>P' in s.series_description) and
                ('epse2d1_64' in s.sequence_name) and
                (s.dim3 == 140) and
                (s.dim4 == 1)):
            info[rest_epi_topup_ap] = [s.series_id]

        if (('rest_topup_P>>A' in s.series_description) and
                ('epse2d1_64' in s.sequence_name) and
                (s.dim3 == 140) and
                (s.dim4 == 1)):
            info[rest_epi_topup_pa] = [s.series_id]

        # REST EPI with Field Map correction

        if (('BOLD_resting 4X4X4 A>>P' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim4 == 190)):
            info[rest_epi_fmap] = [s.series_id]

        if (('Field_mapping 4X4X4 A>>P' in s.series_description) and
                ('fm2d2r' in s.sequence_name) and
                (s.dim3 == 35) and
                (s.TE == 4.92)):
            info[fmap_magnitude1] = [s.series_id]

        if (('Field_mapping 4X4X4 A>>P' in s.series_description) and
                ('fm2d2r' in s.sequence_name) and
                (s.dim3 == 35) and
                (s.TE == 7.38)):
            info[fmap_phasediff] = [s.series_id]

        # DTI with TOPUP correction

        if (('DTI_30dir_1b0 A>>P' in s.series_description) and
                ('ep_b0' in s.sequence_name) and
                (s.dim4 == 31)):
            info[rest_epi_topup] = [s.series_id]

        if (('DTI_30dir_1b0 A>>P' in s.series_description) and
                ('ep_b0' in s.sequence_name) and
                (s.dim4 == 31)):
            info[rest_epi_topup_ap] = [s.series_id]

        if (('DTI_30dir_1b0 P>>A' in s.series_description) and
                ('ep_b0' in s.sequence_name) and
                (s.dim4 == 1)):
            info[rest_epi_topup_pa] = [s.series_id]

        # pCASL

        if (('pcasl_wfu_4_0C R>>L EYES OPEN' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim4 == 81)):
            info[rest_epi_topup] = [s.series_id]

        if (('pcasl_wfu_4_0C L>>R' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim4 == 3)):
            info[rest_epi_topup] = [s.series_id]

        # pCASL with high CO2

        if (('pcasl_wfu_4_0C 3min highCO2' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim4 == 107)):
            info[rest_epi_topup] = [s.series_id]

    return info

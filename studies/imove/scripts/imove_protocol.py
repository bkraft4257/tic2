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

    ->> csvcut -c 4,21,8,9,10,11,12,13,15,16 dicominfo.csv | csvlook

         | series_id                                      | sequence_name | series_description                               | dim1 | dim2 | dim3 | dim4 |    TR |     TE | is_motion_corrected | is_derived |
         | ---------------------------------------------- | ------------- | ------------------------------------------------ | ---- | ---- | ---- | ---- | ----- | ------ | ------------------- | ---------- |
         | 2-MPRAGE_GRAPPA2                               | *tfl3d1_16ns  | MPRAGE_GRAPPA2                                   |  256 |  240 |  192 |    1 | 2.300 |   2.98 |               False |      False |
         |                                                |               |                                                  |      |      |      |      |       |        |                     |            |
         | 3-BOLD_resting 4X4X4 A>>P                      | *epfid2d1_64  | BOLD_resting 4X4X4 A>>P                          |   64 |   64 |   35 |  190 | 2.000 |  25.00 |               False |      False |
         |                                                |               |                                                  |      |      |      |      |       |        |                     |            |
         | 4-rest_topup_A>>P                              | *epse2d1_64   | rest_topup_A>>P                                  |   64 |   64 |  140 |    1 | 2.400 |  38.00 |               False |      False |
         | 5-rest_topup_P>>A                              | *epse2d1_64   | rest_topup_P>>A                                  |   64 |   64 |  140 |    1 | 2.400 |  38.00 |               False |      False |
         |                                                |               |                                                  |      |      |      |      |       |        |                     |            |
         | 6-Field_mapping 4X4X4 A>>P                     | *fm2d2r       | Field_mapping 4X4X4 A>>P                         |   64 |   64 |   35 |    1 | 0.488 |   4.92 |               False |      False |
         | 7-Field_mapping 4X4X4 A>>P                     | *fm2d2r       | Field_mapping 4X4X4 A>>P                         |   64 |   64 |   35 |    1 | 0.488 |   7.38 |               False |      False |
         |                                                |               |                                                  |      |      |      |      |       |        |                     |            |
         | 8-mbep2d_bold 3mm L>>R                         | epfid2d1_64   | mbep2d_bold 3mm L>>R_SBRef                       |   72 |   64 |   64 |    1 | 0.570 |  30.00 |               False |      False |
         | 9-mbep2d_bold 3mm L>>R                         | epfid2d1_64   | mbep2d_bold 3mm L>>R                             |   72 |   64 |   64 |   10 | 0.570 |  30.00 |               False |      False |
         |                                                |               |                                                  |      |      |      |      |       |        |                     |            |
         | 10-mbep2d_bold 3mm R>>L (copy from bold L>>R)  | epfid2d1_64   | mbep2d_bold 3mm R>>L (copy from bold L>>R)_SBRef |   72 |   64 |   64 |    1 | 0.570 |  30.00 |               False |      False |
         | 11-mbep2d_bold 3mm R>>L (copy from bold L>>R)  | epfid2d1_64   | mbep2d_bold 3mm R>>L (copy from bold L>>R)       |   72 |   64 |   64 |  500 | 0.570 |  30.00 |               False |      False |
         |                                                |               |                                                  |      |      |      |      |       |        |                     |            |
         | 12-T2 FLAIR SPACE NEW                          | *spcir_192ns  | T2 FLAIR SPACE NEW                               |  256 |  236 |  192 |    1 | 5.000 | 383.00 |               False |      False |
         |                                                |               |                                                  |      |      |      |      |       |        |                     |            |
         | 13-NODDI_DTI_120dir_12b0_AF4                   | epse2d1_128   | NODDI_DTI_120dir_12b0_AF4_SBRef                  |  128 |  128 |   80 |    1 | 3.500 | 106.00 |               False |      False |
         | 14-NODDI_DTI_120dir_12b0_AF4                   | ep_b5#1       | NODDI_DTI_120dir_12b0_AF4                        |  128 |  128 |   80 |  132 | 3.500 | 106.00 |               False |      False |
         | 15-NODDI_DTI_120dir_12b0_AF4                   | ep_b5#1       | NODDI_DTI_120dir_12b0_AF4                        |  128 |  128 |   80 |  132 | 3.500 | 106.00 |               False |      False |
         |                                                |               |                                                  |      |      |      |      |       |        |                     |            |
         | 16-NODDI_DTI_120dir_12b0_AF4 P>>A              | epse2d1_128   | NODDI_DTI_120dir_12b0_AF4 P>>A_SBRef             |  128 |  128 |   80 |    1 | 3.500 | 106.00 |               False |      False |
         | 17-NODDI_DTI_120dir_12b0_AF4 P>>A              | ep_b5#1       | NODDI_DTI_120dir_12b0_AF4 P>>A                   |  128 |  128 |   80 |    1 | 3.500 | 106.00 |               False |      False |
         | 18-NODDI_DTI_120dir_12b0_AF4 P>>A              | ep_b5#1       | NODDI_DTI_120dir_12b0_AF4 P>>A                   |  128 |  128 |   80 |    1 | 3.500 | 106.00 |               False |      False |
         |                                                |               |                                                  |      |      |      |      |       |        |                     |            |
         | 19-QSM_e6_p2_2mm                               | *swi3d6r      | Mag_Images                                       |  416 |  312 |  384 |    1 | 0.051 |  44.15 |               False |      False |
         | 20-QSM_e6_p2_2mm                               | *swi3d6r      | Pha_Images                                       |  416 |  312 |  384 |    1 | 0.051 |  44.15 |               False |      False |
         | 21-QSM_e6_p2_2mm                               | *swi3d6r      | mIP_Images(SW)                                   |  416 |  312 |  342 |    1 | 0.051 |  44.15 |               False |      False |
         | 22-QSM_e6_p2_2mm                               | *swi3d6r      | SWI_Images                                       |  416 |  312 |  384 |    1 | 0.051 |  44.15 |               False |      False |
         |                                                |               |                                                  |      |      |      |      |       |        |                     |            |
         | 23-pcasl_wfu_4_0C R>>L EYES OPEN               | epfid2d1_56   | pcasl_wfu_4_0C R>>L EYES OPEN                    |   70 |   56 |   43 |   81 | 4.000 |  11.00 |               False |      False |
         | 24-pcasl_wfu_4_0C R>>L EYES OPEN               | epfid2d1_56   | Perfusion_Weighted                               |   70 |   56 |   43 |    1 | 4.000 |  11.00 |               False |       True |
         |                                                |               |                                                  |      |      |      |      |       |        |                     |            |
         | 25-pcasl_wfu_4_0C L>>R (COPY SLICES FROM R>>L) | epfid2d1_56   | pcasl_wfu_4_0C L>>R (COPY SLICES FROM R>>L)      |   70 |   56 |   43 |    3 | 4.000 |  11.00 |               False |      False |
         | 26-pcasl_wfu_4_0C L>>R (COPY SLICES FROM R>>L) | epfid2d1_56   | Perfusion_Weighted                               |   70 |   56 |   43 |    1 | 4.000 |  11.00 |               False |       True |


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

    # Create a key for each DICOM file to convert.  The key tells HDC where and how to name the converted DICOM file.
    # The naming convention is very strict. The rules are established by BIDS  http://bids.neuroimaging.io/
    #
    #  anat, func, fmap are established directories where the data can reside.
    #
    #  {subject} is the variable which will be replaced by the subject's acrostic
    #
    #  {session} is the variable which will be replaced by the session value key.  {session} is inconsistent
    #            and is replaced by the key and it's value. An example, should help clarify this inconsistency
    #            {session} is replaced by ses-{session_id}.
    #
    #  {acq} is the acquisition value
    #
    #  {item:01d} is the item counter padded by two zeros.  This allows HDC to create a unique name if it finds
    #             multiple images that meet your criteria.  We recommend that only one DICOM image should match your
    #             criteria for data conversion. However, this can not happen if the scan is repeated.
    #

    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')

    t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T2w')

    # BOLD Resting State with TOPUP and Fieldmap
    rest_fmri_ap_fmap = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-epi_rec-fmap_bold')
    rest_fmri_ap_topup = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-epi_rec-topup_bold')

    rest_topup_ap = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-epse_dir-ap_epi')
    rest_topup_pa = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-epse_dir-pa_epi')

    fmap_rest_magnitude1 = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-gre_magnitude1')
    fmap_rest_phasediff = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_aicq-gre_phasediff')

    # Multiband EPI Resting State with TOPUP
    mbep2d_topup_lr = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-mbepi_dir-lr_epi')
    mbep2d_topup_lr_sbref = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-mbepi_dir-lr_sbref')

    mbep2d_topup_rl = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-mbepi_dir-rl_epi')
    mbep2d_topup_rl_sbref = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-mbepi_dir-rl_sbref')

    mbep2d_bold = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-mbepi_bold')
    mbep2d_bold_sbref = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-mbepi_sbref')

    # NODDI DTI
    noddi_dti_ap = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-apNoddi_run-{item:01d}_dwi')
    noddi_dti_ap_sbref = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-apNoddi_run-{item:01d}_sbref')

    noddi_dti_pa_topup = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-paNoddi_run-{item:01d}_dwi')
    noddi_dti_pa_topup_sbref = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-paNoddi_run-{item:01d}_sbref')

    # Quantitative Susceptibility Mapping
    qsm_magnitude = create_key('sub-{subject}/{session}/swi/sub-{subject}_{session}_part-mag_GRE')
    qsm_phase = create_key('sub-{subject}/{session}/swi/sub-{subject}_{session}_part-phase_GRE')
    qsm_mip = create_key('sub-{subject}/{session}/swi/sub-{subject}_{session}_minIP')
    qsm_swi = create_key('sub-{subject}/{session}/swi/sub-{subject}_{session}_swi')

    # pseudo Continuous ASL
    pcasl_rl = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-pcasl_bold')
    pcasl_rl_topup = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-pcasl_dir-rl_epi')
    pcasl_lr_topup = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-pcasl_dir-lr_epi')

    # Create an empty dictionary called info for each key

    info = {t1: [],
            t2: [],
            rest_fmri_ap_fmap: [],
            rest_fmri_ap_topup: [],
            rest_topup_ap: [],
            rest_topup_pa: [],
            fmap_rest_magnitude1: [],
            fmap_rest_phasediff: [],
            mbep2d_bold: [],
            mbep2d_bold_sbref: [],
            mbep2d_topup_rl: [],
            mbep2d_topup_rl_sbref: [],
            mbep2d_topup_lr: [],
            mbep2d_topup_lr_sbref: [],
            noddi_dti_ap: [],
            noddi_dti_ap_sbref: [],
            noddi_dti_pa_topup: [],
            noddi_dti_pa_topup_sbref: [],
            qsm_magnitude: [],
            qsm_phase: [],
            qsm_mip: [],
            qsm_swi: [],
            pcasl_rl: [],
            pcasl_rl_topup: [],
            pcasl_lr_topup: [],
            }

    # Loop over each sequence. Use if statements to determine which sequences should be linked to which key

    for idx, s in enumerate(seqinfo):

        # --------------------------------------
        # anat - T1, FLAIR

        if (('MPRAGE_GRAPPA2' in s.series_description) and
                ('tfl3d1_16ns' in s.sequence_name) and
                (s.dim3 == 192) and
                (s.dim4 == 1)):
                info[t1].append([s.series_id])

        if (('T2 FLAIR SPACE NEW' in s.series_description) and
                ('spcir_192ns' in s.sequence_name) and
                (s.dim3 == 192) and
                (s.dim4 == 1)):
                info[t2].append([s.series_id])

        # --------------------------------------
        # bold and distortion correction data

        if (('BOLD_resting 4X4X4 A>>P' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim3 == 35) and
                (s.dim4 == 190)):
                info[rest_fmri_ap_fmap].append([s.series_id])

        if (('BOLD_resting 4X4X4 A>>P' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim3 == 35) and
                (s.dim4 == 190)):
                info[rest_fmri_ap_topup].append([s.series_id])

        if (('rest_topup_A>>P' in s.series_description) and
                ('epse2d1_64' in s.sequence_name) and
                (s.dim3 == 140) and
                (s.dim4 == 1)):
                info[rest_topup_ap].append([s.series_id])

        if (('rest_topup_P>>A' in s.series_description) and
                ('epse2d1_64' in s.sequence_name) and
                (s.dim3 == 140) and
                (s.dim4 == 1)):
                info[rest_topup_pa].append([s.series_id])

        if (('Field_mapping 4X4X4 A>>P' in s.series_description) and
                ('fm2d2r' in s.sequence_name) and
                (s.dim3 == 35) and
                (s.dim4 == 1) and
                (s.TE == 4.92)):
                info[fmap_rest_magnitude1].append([s.series_id])

        if (('Field_mapping 4X4X4 A>>P' in s.series_description) and
                ('fm2d2r' in s.sequence_name) and
                (s.dim3 == 35) and
                (s.dim4 == 1) and
                (s.TE == 7.38)):
                info[fmap_rest_phasediff].append([s.series_id])

        # --------------------------------------
        # Multiband EPI Resting State with TOPUP

        # fmap/ topup lr
        if (('mbep2d_bold 3mm L>>R_SBRef' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim3 == 64) and
                (s.dim4 == 1)):
                info[mbep2d_topup_lr_sbref].append([s.series_id])

        if (('mbep2d_bold 3mm L>>R' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim3 == 64) and
                (s.dim4 == 10)):
                info[mbep2d_topup_lr].append([s.series_id])

        # fmap/ topup rl (a copy of the mbepi resting data. NIFTI file will be truncated later)

        if (('mbep2d_bold 3mm R>>L (copy from bold L>>R)_SBRef' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim3 == 64) and
                (s.dim4 == 1)):
                info[mbep2d_topup_rl_sbref].append([s.series_id])

        if (('mbep2d_bold 3mm R>>L (copy from bold L>>R)' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim3 == 64) and
                (s.dim4 == 500)):
                info[mbep2d_topup_rl].append([s.series_id])

        # func/ bold data
        if (('mbep2d_bold 3mm R>>L (copy from bold L>>R)_SBRef' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim3 == 64) and
                (s.dim4 == 1)):
                info[mbep2d_bold_sbref].append([s.series_id])

        if (('mbep2d_bold 3mm R>>L (copy from bold L>>R)' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim3 == 64) and
                (s.dim4 == 500)):
                info[mbep2d_bold].append([s.series_id])

        # --------------------------------------
        # NODDI DWI

        if (('NODDI_DTI_120dir_12b0_AF4_SBRef' in s.series_description) and
                ('epse2d1_128' in s.sequence_name) and
                (s.dim3 == 80) and
                (s.dim4 == 1)):
                info[noddi_dti_ap_sbref].append([s.series_id])

        if (('NODDI_DTI_120dir_12b0_AF4' in s.series_description) and
                ('epse2d1_128' in s.sequence_name) and
                (s.dim3 == 80) and
                (s.dim4 == 132)):
                info[noddi_dti_ap].append([s.series_id])

        if (('NODDI_DTI_120dir_12b0_AF4 P>>A_SBRef' in s.series_description) and
                ('epse2d1_128' in s.sequence_name) and
                (s.dim3 == 80) and
                (s.dim4 == 1)):
                info[noddi_dti_pa_topup_sbref].append([s.series_id])

        if (('NODDI_DTI_120dir_12b0_AF4 P>>A' in s.series_description) and
                ('epse2d1_128' in s.sequence_name) and
                (s.dim3 == 80) and
                (s.dim4 == 132)):
                info[noddi_dti_pa_topup].append([s.series_id])

        # --------------------------------------
        # Quantitative Susceptibility Mapping

        if (('QSM_e6_p2_2mm' in s.series_id) and
                ('Mag_Images' in s.series_description) and
                ('swi3d6r' in s.sequence_name) and
                (s.dim3 == 384) and
                (s.dim4 == 1)):
                info[qsm_magnitude].append([s.series_id])

        if (('QSM_e6_p2_2mm' in s.series_id) and
                ('Pha_Images' in s.series_description) and
                ('swi3d6r' in s.sequence_name) and
                (s.dim3 == 384) and
                (s.dim4 == 1)):
                info[qsm_phase].append([s.series_id])

        if (('QSM_e6_p2_2mm' in s.series_id) and
                ('mIP_Images(SW)' in s.series_description) and
                ('swi3d6r' in s.sequence_name) and
                (s.dim3 == 342) and
                (s.dim4 == 1)):
                info[qsm_mip].append([s.series_id])

        if (('QSM_e6_p2_2mm' in s.series_id) and
                ('SWI_Images' in s.series_description) and
                ('swi3d6r' in s.sequence_name) and
                (s.dim3 == 384) and
                (s.dim4 == 1)):
                info[qsm_swi].append([s.series_id])

        # --------------------------------------
        # Arterial Spin Labeling

        if (('pcasl_wfu_4_0C R>>L EYES OPEN' in s.series_description) and
                ('epfid2d1_56' in s.sequence_name) and
                (s.dim3 == 43) and
                (s.dim4 == 81)):
                info[pcasl_rl].append([s.series_id])

        if (('pcasl_wfu_4_0C R>>L EYES OPEN' in s.series_description) and
                ('epfid2d1_56' in s.sequence_name) and
                (s.dim3 == 43) and
                (s.dim4 == 81)):
                info[pcasl_rl_topup].append([s.series_id])

        if (('pcasl_wfu_4_0C L>>R (COPY SLICES FROM R>>L)' in s.series_description) and
                ('epfid2d1_56' in s.sequence_name) and
                (s.dim3 == 43) and
                (s.dim4 == 3)):
                info[pcasl_lr_topup].append([s.series_id])

    return info

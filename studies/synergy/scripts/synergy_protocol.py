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

    ->> hdc_look.py -s syn239 -ss 1

            series_number  sequence_name                        series_description  dim1  dim2  dim3  dim4       TR     TE  is_derived  is_motion_corrected
         0              2   *tfl3d1_16ns                         T1_MPRAGE_GRAPPA2   256   240   192     1  2.30000   2.98       False                False
         1              3    *fl3d1r_t70                   TOF_3D_multi-slab SHORT   512   464    72     1  0.02100   3.43       False                False
         2              4    *fl3d1r_t70           TOF_3D_multi-slab SHORT_MIP_SAG   184   512     1     1  0.02100   3.43       False                False
         3              5    *fl3d1r_t70           TOF_3D_multi-slab SHORT_MIP_COR   184   464     1     1  0.02100   3.43       False                False
         4              6    *fl3d1r_t70           TOF_3D_multi-slab SHORT_MIP_TRA   512   464     1     1  0.02100   3.43       False                False
         5              7    *fl3d1r_t70                       BILAT CAROTID SLICE   184   464     1     1  0.02100   3.43       False                False
         6              8   *epfid2d1_64                   BOLD_resting 4X4X4 A>>P    64    64    35   190  2.00000  25.00       False                False
         7              9    *fl3d1r_t70                              RT MCA SLICE   512   464     1     1  0.02100   3.43       False                False
         8             10    *fl3d1r_t70                              LT MCA SLICE   512   464     1     1  0.02100   3.43       False                False
         9             11    *epse2d1_64                           rest_topup_A>>P    64    64   140     1  2.00000  25.00       False                False
         10            12    *epse2d1_64                           rest_topup_P>>A    64    64   140     1  2.00000  25.00       False                False
         11            13       *fl2d1r3    Brain 2D PhCon BILATERAL INT. CAROTIDS   192   144    20     1  0.03972   3.86       False                False
         12            14  *fl2d1_v100in  Brain 2D PhCon BILATERAL INT. CAROTIDS_P   192   144    20     1  0.03972   3.86        True                False
         13            15       *fl2d1r3                     Brain 2D PhCon RT MCA   192   144    20     1  0.03972   3.86       False                False
         14            16  *fl2d1_v100in                   Brain 2D PhCon RT MCA_P   192   144    20     1  0.03972   3.86        True                False
         15            17       *fl2d1r3                     Brain 2D PhCon LT MCA   192   144    20     1  0.03972   3.86       False                False
         16            18  *fl2d1_v100in                   Brain 2D PhCon LT MCA_P   192   144    20     1  0.03972   3.86        True                False

        ... cardiac scans are acquired after this point.


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

    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w.{item:01d}')

    tof = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-3dtof_angio.{item:01d}')

    pc_bilateral = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-pcbilateral_angio.{item:01d}')
    pc_right_mca = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-pcright_angio.{item:01d}')
    pc_left_mca = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-pcleft_angio.{item:01d}')

    rest_ap = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-epi_bold.{item:01d}')
    rest_topup_ap = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-topup_dir-ap_epi.{item:01d}')
    rest_topup_pa = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-topup_dir-pa_epi.{item:01d}')

    # Create an empty dictionary called info for each key

    info = {t1: [],
            tof: [],
            pc_bilateral: [],
            pc_right_mca: [],
            pc_left_mca: [],
            rest_ap: [],
            rest_topup_ap: [],
            rest_topup_pa: [],
            }

    # Loop over each sequence. Use if statements to determine which sequences should be linked to which key

    for idx, s in enumerate(seqinfo):

        # --------------------------------------
        # anat - T1

        if 'MPRAGE' in s.series_description:
                info[t1].append([s.series_id])

        if (('TOF_3D' in s.series_description) and
                ('fl3d1r_t70' in s.sequence_name) and
                (s.dim3 >= 64) and (s.dim3 <= 128)):
            info[tof].append([s.series_id])

        if (('Brain 2D PhCon BILATERAL' in s.series_description) and
                ('fl2d1r3' in s.sequence_name) and
                (not s.is_derived)):
                info[pc_bilateral].append([s.series_id])

        if (('Brain 2D PhCon RT MCA' in s.series_description) and
                ('fl2d1r3' in s.sequence_name) and
                (not s.is_derived)):
                info[pc_right_mca].append([s.series_id])

        if (('Brain 2D PhCon LT MCA' in s.series_description) and
                ('fl2d1r3' in s.sequence_name) and
                (not s.is_derived)):
                info[pc_left_mca].append([s.series_id])

        # --------------------------------------
        # resting state bold

        if (('BOLD_resting 4X4X4 A>>P' in s.series_description) and
                ('epfid2d1_64' in s.sequence_name) and
                (s.dim3 == 35) and
                (s.dim4 == 190)):
                info[rest_ap].append([s.series_id])

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

    return info

#
# Questions for Bob:
#   1. How to specify dki/dti/dwi?
#   

def create_key(template, outtype=('nii.gz','dicom'), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return (template, outtype, annotation_classes)


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group

    """

    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w.{item:01d}')
    t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T2w.{item:01d}')

    rest_fmri_ap = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_bold.{item:01d}')
    rest_topup_ap = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-resttopup_dir-ap_epi.{item:01d}')
    rest_topup_pa = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-resttopup_dir-pa_epi.{item:01d}')

    mt = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-mt.{item:01d}')

    pcasl_ap = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-restpcasl_acq-pcasl_bold.{item:01d}')
    pcasl_topup_ap = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-pcasltopup_dir-ap_epi.{item:01d}')
    pcasl_topup_pa = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-pcasltopup_dir-pa_epi.{item:01d}')

    swi_mag = create_key('sub-{subject}/{session}/swi/sub-{subject}_{session}_acq-swi_part-mag_GRE.{item:01d}')
    swi_pha = create_key('sub-{subject}/{session}/swi/sub-{subject}_{session}_acq-swi_part-phase_GRE.{item:01d}')
    swi_mip = create_key('sub-{subject}/{session}/swi/sub-{subject}_{session}_swimip.{item:01d}')
    swi     = create_key('sub-{subject}/{session}/swi/sub-{subject}_{session}_swi.{item:01d}')


    fmap_mag1 = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-gre_magnitude1.{item:01d}')
    fmap_phdiff = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-gre_phasediff.{item:01d}')



########################

    info = {t1: [],
            t2: [],
            rest_fmri_ap: [],
            rest_topup_ap: [],
            rest_topup_pa: [],
            mt: [],
            pcasl_ap: [],
            pcasl_topup_ap: [],
            pcasl_topup_pa: [],
            swi_mag: [],
            swi_pha: [],
            swi_mip: [],
            swi: [],
            fmap_mag1: [],
            fmap_phdiff: []
            }

    # Loop over each sequence. Use if statements to determine which sequences should be linked to which key

    for idx, s in enumerate(seqinfo):

        if (('mprage' in s.series_description) and
                (s.dim3 == 176) and
                (s.dim4 == 1)):
                info[t1] = [s.series_id]

        if (('flair' in s.series_description) and
                (s.dim3 == 176) and
                (s.dim4 == 1)):
                info[t2] = [s.series_id]

        if (('rest A>>P' in s.series_description) and
                (s.dim3 == 48) and
                (s.dim4 == 200)):
                info[rest_fmri_ap] = [s.series_id]

        if ('rest_topup_A>>P' in s.series_description):
                info[rest_topup_ap] = [s.series_id]

        if ('rest_topup_P>>A' in s.series_description):
                info[rest_topup_pa] = [s.series_id]

        if (('sag_mt' in s.series_description) and
                (s.dim3 == 120) and
                (s.dim4 == 1)):
                info[mt] = [s.series_id]

        if ('pcasl A>>P' in s.series_description):
                info[pcasl_ap] = [s.series_id]

        if ('pcasl_topup_A>>P' in s.series_description):
                info[pcasl_topup_ap] = [s.series_id]

        if ('pcasl_topup_P>>A' in s.series_description):
                info[pcasl_topup_pa] = [s.series_id]

        if (('Mag' in s.series_description) and
            ('swi3d' in s.sequence_name) and
            (s.dim1 == 192)):
                info[swi_mag] = [s.series_id]
            
        if (('Pha' in s.series_description) and
            ('swi3d' in s.sequence_name) and
            (s.dim1 == 192)):
                info[swi_pha] = [s.series_id]
            
        if (('mIP' in s.series_description) and
            ('swi3d' in s.sequence_name) and
            (s.dim1 == 192)):
                info[swi_mip] = [s.series_id]
            
        if (('SWI' in s.series_description) and
            ('swi3d' in s.sequence_name) and
            (s.dim1 == 192)):
                info[swi] = [s.series_id]

        if (('ax_grass_64' in s.series_description) and
            (s.TE == 5.19)):
                info[fmap_mag1] = [s.series_id]

        if (('ax_grass_64' in s.series_description) and
            (s.TE == 7.65)):
                info[fmap_phdiff] = [s.series_id]

            
    return info


# CH$ hdc_look.py -s 34P1003 -ss 1
#               series_id sequence_name  series_description  dim1  dim2  dim3  dim4     TR      TE  is_derived  is_motion_corrected
# 0           1-localizer        *fl2d1           localizer   192   192     3     1  0.020    5.00       False                False
# 1          2-sag_mprage  *tfl3d1_16ns          sag_mprage   256   240   176     1  2.300    2.98       False                False
# 2             3-sag_swi      *swi3d1r          Mag_Images   192   192   128     1  0.047   25.00       False                False
# 3             4-sag_swi      *swi3d1r          Pha_Images   192   192   128     1  0.047   25.00       False                False
# 4             5-sag_swi      *swi3d1r      mIP_Images(SW)   192   192   121     1  0.047   25.00       False                False
# 5             6-sag_swi      *swi3d1r          SWI_Images   192   192   128     1  0.047   25.00       False                False
# 6           7-sag_t2tse    *spc_133ns           sag_t2tse   256   240   176     1  3.200  222.00       False                False
# 7         8-sag_t2flair  *spcir_133ns         sag_t2flair   512   480   176     1  6.000  272.00       False                False
# 8              9-sag_mt      fl_mt3d1              sag_mt   256   208   120     1  0.030    4.57       False                False
# 9             10-sag_mt      fl_mt3d1              sag_mt   256   208   120     1  0.030    4.57       False                False
# 10       11-ax_dki_P>>A        *ep_b0         ax_dki_P>>A    84   128    59    68  9.700  100.00       False                False
# 11        12-sag_mprage  *tfl3d1_16ns        AXIAL MPRAGE   484   484    55     1  2.300    2.98        True                False
# 12           13-sag_swi      *swi3d1r       AXIAL SWI MAG   484   484    55     1  0.047   25.00        True                False
# 13           14-sag_swi      *swi3d1r       AXIAL SWI PHA   484   484    55     1  0.047   25.00        True                False
# 14           15-sag_swi      *swi3d1r       AXIAL SWI MIP   484   484    55     1  0.047   25.00        True                False
# 15           16-sag_swi      *swi3d1r           AXIAL SWI   484   484    55     1  0.047   25.00        True                False
# 16         17-sag_t2tse    *spc_133ns            AXIAL T2   484   484    55     1  3.200  222.00        True                False
# 17       18-sag_t2flair  *spcir_133ns      AXIAL T2 FLAIR   484   484    55     1  6.000  272.00        True                False
# 18            19-sag_mt      fl_mt3d1   AXIAL MAG TRANS 1   484   484    55     1  0.030    4.57        True                False
# 19            20-sag_mt      fl_mt3d1   AXIAL MAG TRANS 2   484   484    55     1  0.030    4.57        True                False
# 20       21-ax_dki_P>>A   *ep_b0_2000     ax_dki_P>>A_ADC    84   128    59     1  9.700  100.00        True                False
# 21       22-ax_dki_P>>A    *ep_b1000t  ax_dki_P>>A_TRACEW    84   128   118     1  9.700  100.00        True                False
# 22       23-ax_dki_P>>A   *ep_b0_2000      ax_dki_P>>A_FA    84   128    59     1  9.700  100.00        True                False
# 23       24-ax_dki_P>>A     Not found   ax_dki_P>>A_ColFA    84   128    59     1 -1.000   -1.00        True                False
# 24    25-dki_topup_A>>P   *epse2d1_84      dki_topup_A>>P   128    84    59     1  7.000   63.00       False                False
# 25    26-dki_topup_P>>A   *epse2d1_84      dki_topup_P>>A    84   128    59     1  7.000   63.00       False                False
# 26         27-rest A>>P  *epfid2d1_60           rest A>>P    60    64    48   200  3.000   30.00       False                False
# 27         28-rest A>>P  *epfid2d1_60          MoCoSeries    60    64    48   200  3.000   30.00       False                 True
# 28   29-rest_topup_A>>P   *epse2d1_60     rest_topup_A>>P    60    64    48     1  4.340   54.00       False                False
# 29   30-rest_topup_P>>A   *epse2d1_60     rest_topup_P>>A    64    60    48     1  4.340   54.00       False                False
# 30        31-pcasl A>>P   epfid2d1_64          pcasl A>>P    64    64    30    81  3.800   13.00       False                False
# 31        32-pcasl A>>P   epfid2d1_64          MoCoSeries    64    64    30    81  3.800   13.00        True                 True
# 32        33-pcasl A>>P   epfid2d1_64  Perfusion_Weighted    64    64    30     1  3.800   13.00        True                 True
# 33        34-pcasl A>>P   epfid2d1_64              relCBF    64    64    30     1  3.800   13.00        True                 True
# 34  35-pcasl_topup_P>>A   *epse2d1_64    pcasl_topup_P>>A    64    64    30     1  4.000   54.00       False                False
# 35  36-pcasl_topup_A>>P   *epse2d1_64    pcasl_topup_A>>P    64    64    30     1  4.000   54.00       False                False
# 36       37-ax_dti_A>>P        *ep_b0         ax_dti_A>>P    84   128    59    68  9.700  100.00       False                False
# 37       38-ax_dti_A>>P   *ep_b0_2000     ax_dti_A>>P_ADC    84   128    59     1  9.700  100.00        True                False
# 38       39-ax_dti_A>>P    *ep_b1000t  ax_dti_A>>P_TRACEW    84   128   118     1  9.700  100.00        True                False
# 39       40-ax_dti_A>>P   *ep_b0_2000      ax_dti_A>>P_FA    84   128    59     1  9.700  100.00        True                False
# 40       41-ax_dti_A>>P     Not found   ax_dti_A>>P_ColFA    84   128    59     1 -1.000   -1.00        True                False
# 41    42-dti_topup_A>>P   *epse2d1_84      dti_topup_A>>P    84   128    59     1  7.000   63.00       False                False
# 42    43-dti_topup_P>>A   *epse2d1_84      dti_topup_P>>A    84   128    59     1  7.000   63.00       False                False
# 43       44-ax_grass_64       *fm2d2r         ax_grass_64    84   128    48     1  0.300    5.19       False                False
# 44       45-ax_grass_64       *fm2d2r         ax_grass_64    84   128    48     1  0.300    7.65       False                False

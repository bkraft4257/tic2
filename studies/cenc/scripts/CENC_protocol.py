
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

    t1 = create_key('anat/sub-{subject}_T1w.{item:02d}')
    t2 = create_key('anat/sub-{subject}_T2w.{item:02d}')
    rest_fmri_ap = create_key('func/sub-{subject}_dir-ap_task-rest_run-{item:02d}_bold')
    rest_topup_ap = create_key('func/sub-{subject}_dir-ap_run-{item:02d}_bold')
    rest_topup_pa = create_key('func/sub-{subject}_dir-pa_run-{item:02d}_bold')
    mt = create_key('anat/sub-{subject}_MT_run-{item:02d}')


########################

    info = {t1: [],
            t2: [],
            rest_fmri_ap: [],
            rest_topup_ap: [],
            rest_topup_pa: [],
            mt: []
            
            }

    # Loop over each sequence. Use if statements to determine which sequences should be linked to which key

    for idx, s in enumerate(seqinfo):

        if (('mprage' in s.series_id) and
                (s.dim3 == 176) and
                (s.dim4 == 1)):
                info[t1] = [s.series_id]

        if (('flair' in s.series_id) and
                (s.dim3 == 176) and
                (s.dim4 == 1)):
                info[t2] = [s.series_id]

        if (('rest A>>P' in s.series_description) and
                (s.dim3 == 48) and
                (s.dim4 == 200)):
                info[rest_fmri_ap] = [s.series_id]

        if (('rest_topup_A>>P' in s.series_id) and
                (s.dim3 == 192) and
                (s.dim4 == 1)):
                info[rest_topup_ap] = [s.series_id]

        if (('rest_topup_P>>A' in s.series_id) and
                (s.dim3 == 192) and
                (s.dim4 == 1)):
                info[rest_topup_pa] = [s.series_id]

        if (('sag_mt' in s.series_id) and
                (s.dim3 == 120) and
                (s.dim4 == 1)):
                info[mt] = [s.series_id]

    return info

############
# series_id,sequence_name,dim1,dim2,dim3,dim4,TR,TE,is_motion_corrected
# 2-sag_mprage,*tfl3d1_16ns,256,240,176,1,2.3,2.98,False
# 3-sag_swi,*swi3d1r,192,192,128,1,0.047,25.0,False
# 4-sag_swi,*swi3d1r,192,192,128,1,0.047,25.0,False
# 5-sag_swi,*swi3d1r,192,192,121,1,0.047,25.0,False
# 6-sag_swi,*swi3d1r,192,192,128,1,0.047,25.0,False
# 7-sag_t2tse,*spc_133ns,256,240,176,1,3.2,222.0,False
# 8-sag_t2flair,*spcir_133ns,512,480,176,1,6.0,272.0,False
# 9-ax_dki_P>>A,*ep_b1000#3,84,128,59,68,9.7,100.0,False
# 10-ax_dki_P>>A,*ep_b0_2000,84,128,59,1,9.7,100.0,False
# 11-ax_dki_P>>A,*ep_b1000t,84,128,118,1,9.7,100.0,False
# 12-ax_dki_P>>A,*ep_b0_2000,84,128,59,1,9.7,100.0,False
# 13-ax_dki_P>>A,Not found,84,128,59,1,-1.0,-1.0,False
# 14-dki_topup_A>>P,*epse2d1_84,84,128,59,1,7.0,63.0,False
# 15-dki_topup_P>>A,*epse2d1_84,84,128,59,1,7.0,63.0,False
# 16-sag_mt,fl_mt3d1,192,144,120,1,0.03,4.57,False
# 17-sag_mt,fl_mt3d1,192,144,120,1,0.03,4.57,False
# 18-rest A>>P,*epfid2d1_60,60,64,48,200,3.0,30.0,False
# 19-rest A>>P,*epfid2d1_60,60,64,48,200,3.0,30.0,True
# 20-rest_topup_A>>P,*epse2d1_60,64,60,192,1,2.5,22.0,False
# 21-rest_topup_P>>A,*epse2d1_60,60,64,192,1,2.5,22.0,False
# 22-pcasl A>>P,epfid2d1_64,64,64,30,81,3.8,13.0,False
# 23-pcasl A>>P,epfid2d1_64,64,64,30,81,3.8,13.0,True
# 24-pcasl A>>P,epfid2d1_64,64,64,30,1,3.8,13.0,True
# 25-pcasl A>>P,epfid2d1_64,64,64,30,1,3.8,13.0,True
# 26-rest_topup_A>>P repeat,*epse2d1_60,60,64,192,1,2.5,22.0,False
# 27-pcasl_topup_P>>A,*epse2d1_64,64,64,150,1,1.5,22.0,False
# 28-pcasl_topup_A>>P,*epse2d1_64,64,64,150,1,1.5,22.0,False
# 29-sag_mprage,*tfl3d1_16ns,256,256,55,1,2.3,2.98,False
# 30-sag_swi,*swi3d1r,192,192,55,1,0.047,25.0,False
# 31-sag_swi,*swi3d1r,192,192,55,1,0.047,25.0,False
# 32-sag_swi,*swi3d1r,192,192,55,1,0.047,25.0,False
# 33-sag_swi,*swi3d1r,192,192,55,1,0.047,25.0,False
# 34-ax_dti_A>>P,*ep_b1300#3,84,128,59,72,9.7,100.0,False
# 35-sag_t2tse,*spc_133ns,256,256,55,1,3.2,222.0,False
# 36-sag_t2flair,*spcir_133ns,512,512,55,1,6.0,272.0,False
# 37-sag_mt,fl_mt3d1,192,192,55,1,0.03,4.57,False
# 38-sag_mt,fl_mt3d1,192,192,55,1,0.03,4.57,False
# 39-ax_dti_A>>P,*ep_b0_1300,84,128,59,1,9.7,100.0,False
# 40-ax_dti_A>>P,*ep_b1300t,84,128,59,1,9.7,100.0,False
# 41-ax_dti_A>>P,*ep_b0_1300,84,128,59,1,9.7,100.0,False
# 42-ax_dti_A>>P,Not found,84,128,59,1,-1.0,-1.0,False
# 43-dti_topup_A>>P,*epse2d1_84,84,128,236,1,4.6,43.0,False
# 44-dti_topup_P>>A,*epse2d1_84,84,128,236,1,4.6,43.0,False
# 45-ax_grass_64,*fm2d2r,84,128,48,1,0.3,5.19,False
# 46-ax_grass_64,*fm2d2r,84,128,48,1,0.3,7.65,False

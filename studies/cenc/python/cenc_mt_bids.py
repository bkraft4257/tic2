#!/usr/bin/env python3
"""
BIDS-based Magnetization Transfer Workflow.  Registration to T1 and calculation of MT Ratio (mtr.nii.gz) image.

INPUTS:  in image_processing/mt/sub-xxxx/ses-n/input

mt_m0.nii.gz  
mt_m1.nii.gz  
nu.nii.gz 
nu_brain.gz
wmlesions_lpa_labels_edited_v2.nii.gz

ACTIONS:

copies input mt_m0/m1 from BIDS_PATH/sub-xxxx/ses-n/anat/sub-xxxx_ses-1_acq-mt0/1.nii.gz
copies wmlesions_lpa_labels_edited_v2.nii.gz from image_processing/freesurfer/sub-xxxx/mri
call extract_tissue_masks.py which converts mgz files to nii.gz in additions to extracting tissue masks.  
    extract_tissue_masks.py puts all files in this input dir
registers m0/m1 to nu.nii.gz and puts warped images in results dir
calculates MTR image using warped m0/m1 and puts it in results dir
computes mask and wmlesion statistics when overlaid on MTR image
writes stats to JSON file in results dir, ready for redcap_upload


"""
import sys
import os                                               # system functions
import re
import numpy as np
import pandas
import json
import argparse
import shutil
import _utilities as util
import labels
import datetime
from collections import OrderedDict
import getpass
import subprocess
import ants_register
import nipype.interfaces.freesurfer as fs
import extract_tissue_masks

# ====================================================================================================
#  Main


def main():

    # Parsing Arguments

    parser = argparse.ArgumentParser(prog='cenc_mt_bids')

    parser.add_argument('-s', "--subjectid", help="Subject ID")
    parser.add_argument('-ss', "--sessionnum", help="Session number", default='1')
    parser.add_argument('-v', '--verbose', help="Verbose flag", action="store_true", default=False)

    args = parser.parse_args()

    if args.subjectid:
        subid = args.subjectid
    else:
        print('Must specify -s subjectid')
        sys.exit()
    
    mtdir = os.path.join(os.getenv('ACTIVE_IMAGE_PROCESSING_PATH'),'mt/sub-'+subid,'ses-1')
    fsdir = os.path.join(os.getenv('ACTIVE_IMAGE_PROCESSING_PATH'),'freesurfer/sub-'+subid,'mri')

    # verify that freesurfer results are available
    if not os.path.exists(fsdir+'/wmlesions_lpa_labels_edited_v2.nii.gz'):
        print("\nIt appears that freesurfer hasn't been run or the labels haven't been edited - do that first.\n")
        sys.exit()

    if args.verbose:
        print('processing ',mtdir)

    # ========  copy mt images and edited wmlesion labels to input dir =============================

    if args.verbose:
        print('copying mt images and lesions labels to input dir')

    if not os.path.exists(os.path.join(mtdir,'input','mt_m0.nii.gz')):

        shutil.copy(os.path.join(os.getenv('ACTIVE_BIDS_PATH'),'sub-'+subid,'ses-1','anat',
                                 'sub-'+subid+'_ses-1_acq-mt0.nii.gz'),
                                 os.path.join(mtdir,'input','mt_m0.nii.gz'))
        shutil.copy(os.path.join(os.getenv('ACTIVE_BIDS_PATH'),'sub-'+subid,'ses-1','anat',
                                 'sub-'+subid+'_ses-1_acq-mt1.nii.gz'),
                                 os.path.join(mtdir,'input','mt_m1.nii.gz'))
        shutil.copy(fsdir+'/wmlesions_lpa_labels_edited_v2.nii.gz',
                                 os.path.join(mtdir,'input','wmlesions_lpa_labels_edited_v2.nii.gz'))
    

    # ======= extract tissue masks  =========================

    if args.verbose:
        print('extracting tissue masks')

    if not os.path.exists(os.path.join(mtdir,'input','nu_brain.nii.gz')):

        extract_tissue_masks.masks_extract(subid,os.path.join(mtdir,'input'))

    # =========  register MT images to nu.nii.gz T1 image  ===================

    if args.verbose:
        print('registering MT images to T1 nu.nii ')

    if not os.path.exists(os.path.join(mtdir,'results','mt_m0_Warped.nii.gz')):

        ants_register.call_ants(os.path.join(mtdir,'input','mt_m0.nii.gz'), 
                                os.path.join(mtdir,'input','nu.nii.gz'),
                                os.path.join(mtdir,'results','mt_m0_'))

        ants_register.call_ants(os.path.join(mtdir,'input','mt_m1.nii.gz'), 
                                os.path.join(mtdir,'input','nu.nii.gz'),
                                os.path.join(mtdir,'results','mt_m1_'))

    # ==============  Calculate MTR image  =======================

    if args.verbose:
        print('calculating MTR image')

    if not os.path.exists(os.path.join(mtdir,'results','mtr.nii.gz')):

        command = ['ImageMath', 3, 
                   os.path.join(mtdir,'results','mtr.nii.gz'), 'MTR', 
                   os.path.join(mtdir,'results','mt_m0_Warped.nii.gz'),
                   os.path.join(mtdir,'results','mt_m1_Warped.nii.gz'), 
                   os.path.join(mtdir,'input','nu_brain.nii.gz')]

        util.iw_subprocess(command, args.verbose, args.verbose, False)

    # ===============  compute stats  ===========================

    if args.verbose:
        print('calculating stats for masks and lesions')

    if not os.path.exists(os.path.join(mtdir,'results','magtrans.json')):

        df_stats_gm_cortical = labels.measure(os.path.join(mtdir,'input','gm.cerebral_cortex.nii.gz'), 
                                              os.path.join(mtdir,'results','mtr.nii.gz'))
        df_stats_gm_subcortical = labels.measure(os.path.join(mtdir,'input','gm.subcortical.nii.gz'), 
                                                 os.path.join(mtdir,'results','mtr.nii.gz'))
        df_stats_wm_cerebral = labels.measure(os.path.join(mtdir,'input','wm.cerebral.nii.gz'), 
                                              os.path.join(mtdir,'results','mtr.nii.gz'))
        df_stats_ventricles = labels.measure(os.path.join(mtdir,'input','ventricles.nii.gz'), 
                                             os.path.join(mtdir,'results','mtr.nii.gz'))


        # calc wmlesions mtr

        df_stats_mt_wmlesions = labels.measure(os.path.join(mtdir,'input','wmlesions_lpa_labels_edited_v2.nii.gz'), 
                                             os.path.join(mtdir,'results','mtr.nii.gz'))

        # these will be numpy.ndarray, no longer a panda dataframe
        idx = df_stats_mt_wmlesions.loc[:, 'label'].values[:]
        mn  = df_stats_mt_wmlesions.loc[:, 'mean'].values[:]

        idx_str = np.array_str(idx,precision=2, max_line_width = 400)
        mn_str = np.array_str(mn,precision=2, max_line_width = 400)

        idx_str = idx_str.replace("[  ","")
        idx_str = idx_str.replace(".]","")
        idx_str = idx_str.replace(".","")
        idx_str = ','.join(idx_str.split())

        mn_str = mn_str.replace("[ ","")
        mn_str = mn_str.replace("]","")
        mn_str = ','.join(mn_str.split())

        # the mean of all the lesions needs to be computed with each lesion weighted by its area.  Just computing the
        #  mean of 'mn' will be erroneous since single-pixel lesions will have the same weight as big ones.  So,
        #  binarize the 'wmlesions' labels and run labels.measure using it.

        mtr = os.path.join(mtdir,'results','mtr.nii.gz')
        wmlesions = os.path.join(mtdir,'input','wmlesions_lpa_labels_edited_v2.nii.gz')

        df_stats_mt_wmlesions_bin = labels.measure(wmlesions, mtr, binarize_labels=True)

        mn_bin  = df_stats_mt_wmlesions_bin.loc[:, 'mean'].values[0]
        mn_bin_str = '{0:4.3f}'.format(mn_bin)

        std_bin  = df_stats_mt_wmlesions_bin.loc[:, 'std'].values[0]
        std_bin_str = '{0:4.3f}'.format(std_bin)
        
        # ==============  write JSON file of results =================================

        dict_redcap = OrderedDict((('subject_id', subid),
                                   ('mt_analyst', getpass.getuser()),
                                   ('mt_datetime', '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())),
                                   ('mt_gm_cortical_mean', '{0:4.3f}'.format(df_stats_gm_cortical['mean'].values[0])),
                                   ('mt_gm_cortical_std', '{0:4.3f}'.format(df_stats_gm_cortical['std'].values[0])),
                                   ('mt_gm_subcortical_mean', '{0:4.3f}'.format(df_stats_gm_subcortical['mean'].values[0])),
                                   ('mt_gm_subcortical_std','{0:4.3f}'.format(df_stats_gm_subcortical['std'].values[0])),
                                   ('mt_wm_cortical_mean', '{0:4.3f}'.format(df_stats_wm_cerebral['mean'].values[0])),
                                   ('mt_wm_cortical_std', '{0:4.3f}'.format(df_stats_wm_cerebral['std'].values[0])),
                                   ('mt_ventricles_mean', '{0:4.3f}'.format(df_stats_ventricles['mean'].values[0])),
                                   ('mt_ventricles_std', '{0:4.3f}'.format(df_stats_ventricles['std'].values[0])),
                                   ('mt_wmlesions_mean', mn_bin_str),
                                   ('mt_wmlesions_std', std_bin_str),
                                   ('mt_lesions_index', idx_str),
                                   ('mt_lesions_value', mn_str),
                                   )
                                  )

        magtrans_json_filename =  os.path.join(mtdir,'results', 'magtrans.json')

        with open(magtrans_json_filename, 'w') as outfile:
            json.dump(dict_redcap, outfile, indent=4, ensure_ascii=True, sort_keys=False)

# ====================================================================================================
# Main Function

if __name__ == "__main__":
    sys.exit(main())


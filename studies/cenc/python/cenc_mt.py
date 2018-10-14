#!/usr/bin/env python3
"""
Magnetization Transfer Workflow.  Registration to T1 and calculation of MT Ratio (mtr.nii.gz) image.
CAH version.  2 Oct 2018
"""
import sys
import os                                               # system functions
import re
import pandas
import json
import argparse
import _utilities as util
import cenc
import labels
import datetime
from collections import OrderedDict
import getpass
import subprocess
import nipype.interfaces.fsl as fsl
import nipype.interfaces.freesurfer as fs 
import nibabel
import scipy
import numpy

# ======================================================================================================================
def create_mask(in_brainmask, in_aseg, mask ):

     nii_brainmask   = nibabel.load(in_brainmask)
     array_brainmask = 1. * (nii_brainmask.get_data()>0)

     if True:
          nii_aseg      = nibabel.load(in_aseg)


          array_aseg      = nii_aseg.get_data()
          
          array_mask_01     = scipy.ndimage.morphology.binary_erosion( 1.*(array_brainmask>0), numpy.ones( [15,15,15] ) )
          array_mask_02      = 1.* ((array_mask_01 + array_aseg) > 0)
          
          #     out_nifti = nibabel.Nifti1Image( 1.*array_mask_02,  None, nii_brainmask.get_header() )
          #     nibabel.save( out_nifti,  '02.mask.nii.gz' )
          
          array_mask_03     = scipy.ndimage.morphology.binary_fill_holes( 1.*(array_mask_02) )
          #     out_nifti = nibabel.Nifti1Image( 1.*array_mask_03,  None, nii_brainmask.get_header() )
          #     nibabel.save( out_nifti,  '03.mask.nii.gz' )
          
          array_mask_04     = scipy.ndimage.morphology.binary_closing( array_mask_03, numpy.ones( [5,5,5] ))
          array_mask_05     = scipy.ndimage.morphology.binary_fill_holes( 1.*(array_mask_04) )
          array_mask_06     = scipy.ndimage.morphology.binary_opening( array_mask_05, numpy.ones( [5,5,5] ))
          
 
     out_nifti = nibabel.Nifti1Image( array_brainmask,  None, nii_brainmask.get_header() )
     nibabel.save( out_nifti,  mask )

# ======================================================================================================================
def save_to_json(input_dir, verbose):
    """ Write MagTrans results to JSON output file"""

    cenc_dirs = cenc.directories(input_dir)

    mtr = os.path.join(cenc_dirs['mt']['dirs']['register'], 'mtr.nii.gz')

    pandas.set_option('expand_frame_repr', False)

    # cenc_aseg_labels.sh generates these label files from aseg.nii.gz, which needs to be converted from aseg.mgz

    df_stats_gm_cortical = labels.measure(cenc_dirs['results']['labels']['gm.cortical'], mtr)
    df_stats_gm_subcortical = labels.measure(cenc_dirs['results']['labels']['gm.subcortical'], mtr)
    df_stats_wm_cerebral = labels.measure(cenc_dirs['results']['labels']['wm.cerebral'], mtr )
    df_stats_ventricles = labels.measure(cenc_dirs['results']['labels']['ventricles'], mtr)
    df_stats_wm_lesions = labels.measure(cenc_dirs['results']['labels']['lesions'], mtr)

    dict_redcap = OrderedDict((('subject_id', cenc_dirs['cenc']['id']),
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
                               ('mt_wmlesions_mean', '{0:4.3f}'.format(df_stats_wm_lesions['mean'].values[0])),
                               ('mt_wmlesions_std', '{0:4.3f}'.format(df_stats_wm_lesions['std'].values[0]))
                               )
                              )

    magtrans_json_filename =  os.path.join(cenc_dirs['mt']['dirs']['02-stats'], 'magtrans.json')

    with open(magtrans_json_filename, 'w') as outfile:
        json.dump(dict_redcap, outfile, indent=4, ensure_ascii=True, sort_keys=False)

    if verbose:
        cenc.print_json_redcap_instrument(magtrans_json_filename)

    return


# ======================================================================================================================
#  Main
def main():

    ## Parse Arguments
    usage = "usage: %prog -s 34Pxxxx [-ss <n> default=1]"
    parser = argparse.ArgumentParser(prog='cenc_mt')
    parser.add_argument('-s', "--subject", help="Subject ID 34Pxxxx", default='34P0000')
    parser.add_argument('-ss', "--session", help="Session Number", default='1')
    parser.add_argument('-v', "--verbose", help="Verbose flag", action="store_true", default=False)
    inArgs = parser.parse_args()

    if len(sys.argv) == 1:
         parser.print_help()
         sys.exit()

    subject = inArgs.subject
    if subject == '34P0000':
         parser.print_help()
         sys.exit()

    session = inArgs.session

    print('setting up directories')
    # setup directories:  image_processing/mt/sub-34Pxxxx/ses-1
    cenc_improc_dir = os.getenv('CENC_IMAGE_PROCESSING_PATH')
    os.chdir(cenc_improc_dir)
    cenc_improc_mt_dir = os.path.join(cenc_improc_dir,'mt')
    if not os.path.isdir(cenc_improc_mt_dir):
        os.mkdir(cenc_improc_mt_dir)

    os.chdir(cenc_improc_mt_dir)
    if not os.path.isdir('sub-'+subject):
         os.mkdir('sub-'+subject)
    os.chdir('sub-'+subject)
    if not os.path.isdir('ses-'+session):
         os.mkdir('ses-'+session)
    os.chdir('ses-'+session)


    # convert freesurfer output nu.mgz to nu.nii.gz
    if not os.path.isfile('nu.nii.gz'):
         print('creating nu.nii.gz')
         t1mgz = '../../../freesurfer/sub-'+subject+'/mri/nu.mgz'
         mc = fs.MRIConvert( in_file  = t1mgz,
                             out_file = 'nu.nii.gz',
                             out_type = 'niigz')
         mc.run()
         reorient = fsl.Reorient2Std( in_file = 'nu.nii.gz', out_file = 'nu.nii.gz')
         reorient.run()

    # convert freesurfer output brainmask.mgz to brainmask.nii.gz
    if not os.path.isfile('brainmask.nii.gz'):
         print('creating brainmask.nii.gz')
         maskmgz = '../../../freesurfer/sub-'+subject+'/mri/brainmask.mgz'
         mc = fs.MRIConvert( in_file  = maskmgz,
                             out_file = 'brainmask.nii.gz',
                             out_type = 'niigz')
         mc.run()
         reorient = fsl.Reorient2Std( in_file = 'brainmask.nii.gz', out_file = 'brainmask.nii.gz')
         reorient.run()

    # convert freesurfer output aparc.a2009s+aseg.mgz to aparc.a2009s+aseg.nii.gz
    if not os.path.isfile('aparc.a2009s+aseg.nii.gz'):
         print('creating aparc.a2009s+aseg.nii.gz')
         asegmgz = '../../../freesurfer/sub-'+subject+'/mri/aparc.a2009s+aseg.mgz'
         mc = fs.MRIConvert( in_file  = asegmgz,
                             out_file = 'aparc.a2009s+aseg.nii.gz',
                             out_type = 'niigz')
         mc.run()
         reorient = fsl.Reorient2Std( in_file = 'aparc.a2009s+aseg.nii.gz', out_file = 'aparc.a2009s+aseg.nii.gz')
         reorient.run()

    # Create final brain mask, mask.nii.gz
    if not os.path.isfile('mask.nii.gz'):
         print('creating mask.nii.gz')
         create_mask('brainmask.nii.gz',         
                     'aparc.a2009s+aseg.nii.gz', 
                     'mask.nii.gz')

    # use mask to extract brain from nu.nii.gz to produce nu_brain.nii.gz
    if not os.path.isfile('nu_brain.nii.gz'):
         print('creating nu_brain.nii.gz')
         util.iw_subprocess(['fslmaths', 
                             'nu.nii.gz',
                             '-mas', 
                             'mask.nii.gz',
                             'nu_brain.nii.gz'])

    # register m0 image to T1
    if not os.path.isfile('mt_Affine_nu_mt_m0_Warped.nii.gz'):
         print('creating mt_Affine_nu_mt_m0_Warped.nii.gz')
         input_mt_file = '../../../../bids/sub-'+subject+'/ses-'+session+'/anat/sub-'+subject+'_ses-'+session+'_acq-mt.nii.gz'
         command = ['antsRegistrationSyNQuick.sh', '-d', '3', '-m', input_mt_file , '-r', 'nu.nii.gz',
                    '-f', 'nu.nii.gz', '-t', 'a', '-o', 'mt_Affine_nu_mt_m0_']
         util.iw_subprocess( command, True, True, False)

    # register m1 image to T1
    if not os.path.isfile('mt_Affine_nu_mt_m1_Warped.nii.gz'):
         print('creating mt_Affine_nu_mt_m1_Warped.nii.gz')
         input_mt_file = '../../../../bids/sub-'+subject+'/ses-'+session+'/anat/sub-'+subject+'_ses-'+session+'_acq-mt.2.nii.gz'
         command = ['antsRegistrationSyNQuick.sh', '-d', '3', '-m', input_mt_file , '-r', 'nu.nii.gz',
                    '-f', 'nu.nii.gz', '-t', 'a', '-o', 'mt_Affine_nu_mt_m1_']
         util.iw_subprocess( command, True, True, False)

    # Calculate MTR image
    print('calculating mtr.nii.gz')
    command = ['ImageMath', 3, 'mtr.nii.gz', 'MTR', 'mt_Affine_nu_mt_m0_Warped.nii.gz', 
               'mt_Affine_nu_mt_m1_Warped.nii.gz', 'nu_brain.nii.gz']

    util.iw_subprocess( command, True, True, False)


    # ---------------------------------
    # now measure MT in various labels
    # ---------------------------------

    # convert freesurfer output aseg.mgz to aseg.nii.gz
    if not os.path.isfile('aseg.nii.gz'):
         print('creating aseg.nii.gz')
         asegmgz = '../../../freesurfer/sub-'+subject+'/mri/aseg.mgz'
         mc = fs.MRIConvert( in_file  = asegmgz,
                             out_file = 'aseg.nii.gz',
                             out_type = 'niigz')
         mc.run()
         reorient = fsl.Reorient2Std( in_file = 'aseg.nii.gz', out_file = 'aseg.nii.gz')
         reorient.run()


    
# ======================================================================================================================
# Main Function

if __name__ == "__main__":
    sys.exit(main())


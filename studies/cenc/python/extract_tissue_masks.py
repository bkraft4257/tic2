#!/usr/bin/env python3

import sys
import os                                               # system functions
import argparse
import labels
import _utilities as util
import nibabel
import nipype.interfaces.freesurfer as fs 

def masks_extract(subid, outdir):

    # outdir example, for mt:  /cenc/new2018/cenc/image_processing/mt/sub-34P1162/ses-1/input

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    fsdir = os.path.join(os.getenv('ACTIVE_IMAGE_PROCESSING_PATH'),'freesurfer/sub-'+subid,'mri')

    # =============== convert mgz masks to nii ===================================

    mgzfiles = [ os.path.join( fsdir, 'nu.mgz'),
                 os.path.join( fsdir, 'aseg.mgz'),
                 os.path.join( fsdir, 'brainmask.mgz'),
                 os.path.join( fsdir, 'aparc.a2009s+aseg.mgz'),
                 os.path.join( fsdir, 'wmparc.mgz')
               ]

    for ii in mgzfiles:
        mc = fs.MRIConvert( in_file  = ii,
                            out_file = os.path.join( outdir,str.replace( os.path.basename(ii),'.mgz','.nii.gz')),
                            out_type = 'niigz'
                            )
        mc.run()

    # ==============  extract masks ===============================================

    labels.extract(os.path.join(outdir, 'aseg.nii.gz'), [],
                   [10, 11, 12, 13, 17, 18, 49, 50, 51, 52, 53, 54],
                   os.path.join(outdir, 'gm.subcortical.nii.gz') , merge=1)

    labels.extract(os.path.join(outdir, 'aseg.nii.gz'), [], [3, 42],
                   os.path.join(outdir, 'gm.cerebral_cortex.nii.gz') , merge=1)

    labels.extract(os.path.join(outdir, 'aseg.nii.gz'), [], [8, 47],
                   os.path.join(outdir, 'gm.cerebellum.nii.gz') , merge=1)

    labels.extract(os.path.join(outdir, 'aseg.nii.gz'), [], [2, 41],
                   os.path.join(outdir, 'wm.cerebral.nii.gz') , merge=1)

    labels.extract(os.path.join(outdir, 'aseg.nii.gz'), [], [7, 46],
                   os.path.join(outdir, 'wm.cerebellum.nii.gz') , merge=1)

    labels.extract(os.path.join(outdir, 'aseg.nii.gz'), [], [4, 43],
                   os.path.join(outdir, 'ventricles.nii.gz') , merge=1)

    # ===================  Brain extraction nu_brain.nii.gz

    # create cleaner brain mask.nii.gz
    nii_brainmask  = nibabel.load(os.path.join(outdir, 'brainmask.nii.gz'))
    array_brainmask = 1. * (nii_brainmask.get_data()>0)
 
    out_nifti = nibabel.Nifti1Image( array_brainmask,  None, nii_brainmask.get_header() )
    nibabel.save( out_nifti, os.path.join(outdir, 'mask.nii.gz'))

    util.iw_subprocess(['fslmaths', 
                        os.path.join( outdir, 'nu.nii.gz'),
                        '-mas', 
                        os.path.join( outdir, 'mask.nii.gz'),
                        os.path.join( outdir, 'nu_brain.nii.gz')])



def main():

    # =============  parse arguments ======================================

    parser = argparse.ArgumentParser(prog='extract_tissue_masks')
    parser.add_argument('-s', "--subjectid", help="Subject ID")
    parser.add_argument('-ss', "--sessionnum", help="Session number", default='1')
    parser.add_argument('-m', "--modality", help="Modality (mt, swi, ...)")
    args = parser.parse_args()

    if args.subjectid:
        subid = args.subjectid
    else:
        print('Must specify -s subjectid')
        sys.exit()
    
    # =============  extract masks  ======================================

    masks_extract(subid, args.modality)


if __name__ == "__main__":
    sys.exit(main())

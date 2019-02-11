#!/usr/bin/env python3
"""
To avoid re-running freesurfer in the new BIDS setup, this script will copy the freesurfer folder from /cenc/mri/subject
into the BIDS image_processing folder.

"""

import sys
import os
import argparse
import shutil
import extract_tissue_masks

def main():

    parser = argparse.ArgumentParser(prog='ants_register')

    parser.add_argument('-s', "--subjectid", help="Subject ID")
    parser.add_argument('-ss', "--sessionnum", help="Session number", default='1')
    parser.add_argument('-v', '--verbose', help="Verbose flag", action="store_true", default=False)

    args = parser.parse_args()

    if not args.subjectid:
        print('Must specify -s subjectid')
        sys.exit()

    old_fs_dir = os.path.join('/cenc/mri/freesurfer',args.subjectid)
    bids_fs_dir = os.path.join(os.getenv('ACTIVE_IMAGE_PROCESSING_PATH'),'freesurfer/sub-'+args.subjectid)

    if os.path.exists(bids_fs_dir):
        print('dest dir appears to already exist - delete it if you want to copy again')
        sys.exit()

    if args.verbose:
        print('copying ',old_fs_dir,' to \n',bids_fs_dir)

    shutil.copytree(old_fs_dir,bids_fs_dir)

    # now, extract the masks and labels we will be using
    if os.path.exists(bids_fs_dir+'/results'):
        print('dest dir results folder appears to already exist - delete it if you want to copy again')
        sys.exit()

    extract_tissue_masks.masks_extract(args.subjectid,os.path.join(bids_fs_dir,'results'))


if __name__ == "__main__":
    sys.exit(main())

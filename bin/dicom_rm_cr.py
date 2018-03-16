#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  dicom_rm_cr.py:  remove CR/LF (\r,\n) from ImageComments (0020:4000)
                   in all DICOM images under a specified directory

"""

import os
import argparse
import glob
import dicom as dcm
import isdicom


def rm_cr(dname):

    for root, dirs, files in os.walk(dname):
        for fname in files:
            fullname = os.path.join(root,fname)
            if isdicom.isdcm(fullname):
                try:
                    ds = dcm.read_file(fullname)
                except dcm.errors.InvalidDicomError:
                    print('Bad DICOM: %s\n' % (fullname))

                if "ImageComments" in ds:      # (0020,4000)
                    comm =(ds.ImageComments)
                    comm2=comm.replace("\r","").replace("\n","")
                    ds.ImageComments=comm2
                    ds.save_as(fullname)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="dicom_rm_cr.py:  remove CR/LF from ImageComments")
    parser.add_argument("dname", type=str,
                        help="Directory containing DICOM images.")
    args = parser.parse_args()

    for dirname in glob.glob(args.dname):

        rm_cr(dirname)



#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

# display dicom header

import argparse
import pydicom
import glob

parser = argparse.ArgumentParser(description="dicominfo: print DICOM header(s)")

parser.add_argument("dicomimages", type=str,
                    help="DICOM image(s) - can use wild cards.")

args = parser.parse_args()

print('args.dicomimages = ',args.dicomimages)

glob_results = glob.glob(args.dicomimages)
print(glob_results)

for img in glob_results:
    print('checking ',img)
    ds = pydicom.dcmread(img)
    print(ds)

#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:



## Parsing Arguments
#
#
import os
import shutil
import sys
from  argparse import ArgumentParser

usage = "usage: icAntsBuildTemplate.py [--debugFlag --graphFlag] inDirectory"

parser = ArgumentParser(usage=usage)

parser.add_argument("inSubjectID",    help="" )
parser.add_argument("--debugFlag",  help="", action='store_true', default=True )
parser.add_argument("--graphFlag",  help="", action='store_true', default=False )

parser.add_argument("--template", action="store",  dest="nioTemplate", default="*.nii.gz", 
                    help="Template for NIO Data Grabber")

inArgs = parser.parse_args()

if inArgs.debugFlag:
    print
    print parser.parse_args()

"""
Initialize arguments
"""
startDir     = os.getcwd();

subjectDir   = '/infinite3/infinite/imaging_data/'

subjectID = inArgs.inSubjectID
aT1       = os.path.join(subjectDir, subjectID + "bv3", 'data','linked','T1.nii.gz')
bT1       = os.path.join(subjectDir, subjectID + "fv0", 'data','linked','T1.nii.gz')


gatherDir = os.path.join(subjectDir, 'templates', 'smallGroup', 'infinite_sst')

print gatherDir

"""
 Create Half Space Template Directory, copy T1.nii.gz files, and
 rename Baseline = a and Follow-Up = b.

"""
if not os.path.exists(gatherDir):
    os.makedirs(gatherDir)

os.chdir(gatherDir)


shutil.copy(aT1, os.path.join(gatherDir,subjectID + 'bv3_T1.nii.gz'))
shutil.copy(bT1, os.path.join(gatherDir,subjectID + 'fv0_T1.nii.gz'))




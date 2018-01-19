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


halfSpaceDir = os.path.join(subjectDir,subjectID + 'bv3', 'anatomic','subject_template')

print halfSpaceDir

"""
 Create Half Space Template Directory, copy T1.nii.gz files, and
 rename Baseline = a and Follow-Up = b.

"""
if not os.path.exists(halfSpaceDir):
    os.makedirs(halfSpaceDir)

os.chdir(halfSpaceDir)


shutil.copy(aT1, os.path.join(halfSpaceDir,'a_T1.nii.gz'))
shutil.copy(bT1, os.path.join(halfSpaceDir,'b_T1.nii.gz'))

"""
Apply N4 Correction to Basline and Follow-Up

"""

print '\n\n========================================================================================================'

a_n4_T1       = os.path.join(halfSpaceDir, 'a_n4_T1.nii.gz')
b_n4_T1       = os.path.join(halfSpaceDir, 'b_n4_T1.nii.gz')

sysCommand = 'N4BiasFieldCorrection -i ' + aT1 + ' -o ' + a_n4_T1

print sysCommand
os.system(sysCommand)
print '\n\n'

sysCommand = 'N4BiasFieldCorrection -i ' + bT1 + ' -o ' + b_n4_T1

print sysCommand
os.system(sysCommand)

print '\n\n========================================================================================================'


"""
  Create Half-Space with ANTS UNBIASEd Pairwise Registration
"""

sysCommand = 'unbiased_pairwise_registration.sh -d 3  -f ' + a_n4_T1 + ' -m ' + b_n4_T1 + ' -o ' + subjectID

print sysCommand
os.system(sysCommand)
print '\n\n'


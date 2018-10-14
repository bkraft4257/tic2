#!/usr/bin/env python

"""

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

from nipype.interfaces.ants import Registration
import nipype.interfaces.fsl as fsl

from   nipype.pipeline.engine import Workflow, Node

def get_bit(byteval,idx):
     # http://stackoverflow.com/questions/2591483/getting-a-specific-bit-value-in-a-byte-string
    return ((byteval&(1<<idx))!=0);

def extract_participant_id(in_dir, pattern):
     match = re.findall(pattern, in_dir)

     if not len(match) == 1:
          sys.exit('Participant ID not found')

     return match[0]

def main():
     ## Parsing Arguments
     #
     #

     usage = "usage: %prog"
     parser = argparse.ArgumentParser(prog='cenc_id')
     parser.add_argument("--in_cenc", help="CENC integer, acrostic, or directory", default = os.getcwd() )
     parser.add_argument("--cenc_dir", help="CENC integer, acrostic, or directory", default = os.getenv('CENC_MRI_DATA') )
     parser.add_argument("-m", "--method", help="Methods for ID. (list, update)", choices=['list','update','get'], default='get')
     parser.add_argument("--filter", help="Filter IDs", choices=['test','study','all'], default='study')
     parser.add_argument("--id_bitmask", help="1=id, 2=directory, 4=exists, (1)", default=1, type=int)
     parser.add_argument("-v", "--verbose", help="verbose flag", action="store_true", default=False )
     parser.add_argument("-o", "--output",  help="Return IDs as output", action="store_true", default=False )
     inArgs = parser.parse_args()

     output_flag = inArgs.output

     if inArgs.method in 'list':
          results = cenc.participants(inArgs.cenc_dir, inArgs.method, inArgs.filter, inArgs.verbose)

     if inArgs.method in 'update':
          results = cenc.participants(inArgs.cenc_dir, inArgs.method, inArgs.filter, inArgs.verbose)

     if inArgs.method in 'get':
          id, id_dir, id_exist = cenc.participant_id(inArgs.in_cenc)

          results = []

          if inArgs.id_bitmask & 1:
               results.append(id)
          
          if inArgs.id_bitmask & 2:
               results.append(id_dir)
          
          if inArgs.id_bitmask & 4:
               results.append(id_exist)

          output_flag = True

     if output_flag:
          if len(results)==1:
               return results[0]
          else:
               return results
     else:
          return
 
#
# Main Function
#

if __name__ == "__main__":
    sys.exit(main())


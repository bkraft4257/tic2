#!/usr/bin/env python

import glob
import argparse
import os

def find_files( in_dir=os.getcwd(), pattern='*/*.2-9.*' ):
 
    file_search_pattern = os.path.abspath(os.path.join(in_dir, pattern ))
    print(file_search_pattern)

    files = glob.glob( file_search_pattern) 
    print(files) 

    for ii in files:
        print(ii)

    return


                           
if __name__ == '__main__':
 
    # Parsing Arguments
    #
    #

    usage = 'usage: %prog [options] arg1 arg2'

    parser = argparse.ArgumentParser(prog='monitor_status')

    parser.add_argument('--in_dir', help='Input directory', default=os.getcwd())

    parser.add_argument("-v", "--verbose", help="Verbose flag", action="store_true", default=False)

    in_args = parser.parse_args()

    # Find 
    find_files(in_args.in_dir, '*/*.[2-9].*')

    find_files(in_args.in_dir, '*/*.1.*')

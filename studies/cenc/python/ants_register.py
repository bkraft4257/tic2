#!/usr/bin/env python3

import sys
import argparse
import _utilities as util


def call_ants(input_file, ref_image, output_file):

    command = ['antsRegistrationSyNQuick.sh', '-d', '3', '-m', input_file, '-r', ref_image,
               '-f', ref_image, '-t', 'a', '-o', output_file]

    util.iw_subprocess(command, True, True, False)


def main():

    # usage = "usage: %prog [options] inimg refimg outimg"

    parser = argparse.ArgumentParser(prog='ants_register')

    parser.add_argument("inimg", help="Input image")
    parser.add_argument("refimg", help="Reference image")
    parser.add_argument("outimg", help="Output image")

    args = parser.parse_args()

    print("args.inimg =", args.inimg)

    call_ants(args.inimg, args.refimg, args.outimg)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python

"""

"""
import shutil

import sys
import argparse

from nipype.algorithms.rapidart import ArtifactDetect
import nibabel
import pandas
import numpy

<<<<<<< HEAD
#  I am not sure if these steps are correct but it is a start.
#
#   >> mcflirt -in bold.nii.gz -plots -mats  -report -meanvol
#   >> gunzip *.gz
#   >> ./rapidart.py
#


=======
>>>>>>> caa3d72b85aed21f78c0102ada2dbfbb00368684
def write_confounds( input_file, outliers, output_file ):

     nii_fmri = nibabel.load( input_file )
     n_volumes = nii_fmri.shape[3]

     n_outliers = len(outliers)

     # Convert list of outliers to a column of 0 with a single 1

     confounds = numpy.zeros( (n_volumes, n_outliers), dtype=int )

     for ii,jj in enumerate(outliers):
         confounds[jj,ii] = 1

     df_out = pandas.DataFrame(confounds)
     df_out.to_csv(output_file, index=False, header=False)


def get_input_arguments():
    """
    __main__ function definition to run program from command line.
    """

    parser = argparse.ArgumentParser(prog='netprep')

    parser.add_argument("--input_file", help="Realigned fmri data", default='bold_mcf.nii')
    parser.add_argument("--fsl_realigment_parameters",  help="Realign parameters", default='bold_mcf.par')
    parser.add_argument("--mask_threshold", help="Threshold to create fMRI mask", default=200)

    return parser.parse_args()


def main():
    ## Parsing Arguments
    #
    #

    in_args = get_input_arguments()

    input_file = in_args.input_file
    outliers_file = 'art.bold_mcf_outliers.txt'
    confound_file = 'art.bold_mcf_confounds.txt'

    ad = ArtifactDetect()
    ad.inputs.realigned_files = in_args.input_file
    ad.inputs.mask_type = 'thresh'
    ad.inputs.mask_threshold  = in_args.mask_threshold
    ad.inputs.realignment_parameters = in_args.fsl_realigment_parameters
    ad.inputs.parameter_source = 'FSL'
    ad.inputs.norm_threshold = 2
    ad.inputs.use_differences = [True, False]
    ad.inputs.zintensity_threshold = 3
    ad.run()

    # Write out confounds

    df = pandas.read_csv( outliers_file, names=['outliers'], header=None)
    outliers = list(df['outliers'].values)

    write_confounds( input_file, outliers, confound_file )


#
# Main Function
#

if __name__ == "__main__":
    sys.exit(main())


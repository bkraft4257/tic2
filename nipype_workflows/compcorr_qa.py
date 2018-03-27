#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
compare correlation matrices from the command line.
"""

import argparse
from nilearn import input_data
from nilearn.connectome import ConnectivityMeasure

import os
import numpy
import scipy.io as sio

import matplotlib.pyplot as plt

def display_correlation_histogram(correlation_matrix1, correlation_matrix2, subsample=32):
    """

    :param correlation_matrix1: Filename of the correlation maxti
    :param correlation_matrix2:
    :param subsample:
    :return:
    """

    fig = plt.figure()

    bc_hist = correlation_matrix1.flatten()[0::subsample]
    ac_hist = correlation_matrix2.flatten()[0::subsample]

    plt.hist(bc_hist, 101, alpha=0.5, label='before', facecolor='red', ec='red');
    plt.hist(ac_hist, 101, alpha=0.5, label='after', facecolor='green', ec='green');
    plt.legend(loc='upper right')
    plt.title('Correlation Coefficient Histogram Before and After CompCorr')
    plt.xlabel('Correlation Coefficient')
    plt.ylabel('Count')
    fig.savefig('plot.png');


def calc_correlation_matrix(data, out_filename=None, kind='correlation'):
    """

    :param data:
    :param out_filename: Output filename for the Matlab mat file to store correlation matrix.
    :param kind: Nilearn's correlation matrix.  Possible values  {correlation, partial correlation,
    tangent, covariance, precision}
    :return:
    """
    correlation_measure = ConnectivityMeasure(kind=kind)
    correlation_matrix = (correlation_measure.fit_transform([data])[0]).astype(numpy.float16)


    print('\n\ncorrelation_matrix.dtype')
    print(correlation_matrix.dtype)
    print('\n\n')

    out_filename = os.path.abspath(out_filename)

    sio.savemat(out_filename, {'correlation_matrix': correlation_matrix})

    return out_filename


def _calc_correlation_matrix(data, kind='correlation'):
    """
    Calculate the correlation matrix with Nilearn's Connectivity Measure class.
    :param data:
    :param kind:
    :return:
    """
    correlation_measure = ConnectivityMeasure(kind=kind)
    correlation_matrix = correlation_measure.fit_transform([data])[0]

    return correlation_matrix


def _transform_nifti(in_file,
                     mask_file,
                     standardize = True,
                     smoothing_fwhm = 0,
                     low_pass = None,
                     high_pass = None,
                     t_r = None,
                     detrend = False, verbose=False):

    """

    Transforms the 4D in_file to a 2D matrix for futher processing with NILEARN

    :param in_file: 4D NIFTI input filename
    :param mask_file: Mask for voxels that will be detrended, filtered, and standardized along the 4th dimension.

    :param standardize: boolean, optional. If standardize is True, the time-series are
                        centered and normed: their mean is put to 0 and their variance
                        to 1 in the time dimension.

    :param smoothing_fwhm: float, optional  If smoothing_fwhm is not None, it gives the
                           full-width half maximum in millimeters of the spatial
                           smoothing to apply to the signal.

    :param detrend: boolean, optional. If detrending should be applied on timeseries
                   (before confound removal)

    :param low_pass: None or float, optional. low cutoff frequency for filtering the fMRI
                     bold signal, in Hertz.

    :param high_pass: None or float, optional. high cutoff frequency for filtering the
                      fMRI bold signal, in Hertz.

    :param t_r: float, Repetition time, in second (sampling period). This parameter must
                be defined if lowpass or highpass are defined.

    :param verbose: boolean, optional.  Print additional information to stdout.

    :return: niftimasker, nifti_masker.transformed 4D dataset.
    """

    if verbose:
        print('\nin_file = {0}'.format(in_file))
        print('mask_file = {0}\n'.format(mask_file))

    nifti_masker = input_data.NiftiMasker(mask_img=mask_file,
                                          standardize=standardize,
                                          smoothing_fwhm=smoothing_fwhm,
                                          detrend=detrend)

    nifti_masker.fit(in_file)

    return nifti_masker, nifti_masker.transform( in_file, confounds=None)



def main(in_args):

    # Calculate Correlation Matrix before_compcorr

    nifti_masker, before_compcorr = _transform_nifti( os.path.abspath(in_args.before_compcorr),
                                                      os.path.abspath(in_args.mask),
                                                      verbose=in_args.verbose)

    corr_before_compcorr = _calc_correlation_matrix(before_compcorr)
    numpy.fill_diagonal(corr_before_compcorr, 0)

    # Calculate Correlation Matrix after_compcorr

    nifti_masker, after_compcorr = _transform_nifti(in_args.after_compcorr, in_args.mask)

    corr_after_compcorr = _calc_correlation_matrix(after_compcorr)
    numpy.fill_diagonal(corr_after_compcorr, 0)


    # if in_args.save:
    #     nibabel.save(nifti_masker.inverse_transform(corr_after_compcorr), 'after_compcorr_cmatrix.nii.gz')


    # Save Correlation Histograms to PNG file
    display_correlation_histogram(corr_before_compcorr,
                                  corr_after_compcorr,
                                  subsample=in_args.subsample)
    return



if __name__ == '__main__':
    """ Compare corrlation matrices before and after CompCorr is applied to a 4D fMRI data set. 
    """

    ## Parsing Arguments
    #
    #

    usage = 'usage: %prog [options] arg1 arg2'

    parser = argparse.ArgumentParser(prog='labels_extract')

    parser.add_argument('before_compcorr', help='NIFTI file before compcorr')
    parser.add_argument('after_compcorr', help='NIFTI file before compcorr')
    parser.add_argument('mask', help='Mask to calculate compcorr')

    parser.add_argument('--subsample', help='Subsample correlation matrix by sampling every Nth correlation value to '
                                          'display', default=64)

    parser.add_argument('-v', '--verbose' , help='Verbose flag' , action='store_true' , default=False)
    parser.add_argument('-s', '--save' , help='Saves correlation matrix in NIFTI files' ,
                        action='store_true' , default=False)

    in_args = parser.parse_args()

    main(in_args)

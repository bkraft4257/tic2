# Purpose

netprep preprocess a 4D fMRI data set for network processing.  The workflow requires three inputs

1. A 4D fMRI NIFTI file
1. A gray matter tissue probability map
1. A CSV file containing the confounds to be regressed out.

Inputs to define the inputs and control the behavior of the netprep workflow are entered by a YAML file. Additional information about the YAML file can be seen later.

# Steps to run the workflow

1. Create an input directory for to copy or link the necessary files.
1. Copy an existing YAML file for the study to the input directory to modify for the individual subject. If you don't have a study specific YAML file you can create one from scratch by entering the command netprep study.yaml -g.
1. Run the netprep workflow.   nohup netprep.py study.yaml >> nohup.netprep.log &

Run time is only a few minutes per 4D fMRI data set.  The results are gathered and written to in the results subdirectory in the *netprep_methods_dir* specified in the YAML file. The idea is that a person can QA the results in the file. After the results have passed QA then the whole directory can moved up one level and the intermediate methods folder can be removed.  This will allow one to easily determine what files have been processed and undergone QA.


# Help from netprep.py

usage: netprep [-h] [-g] [-p] [-v] yaml

netprep performs preprocessing on an fMRI BOLD data set to prepare it for network analysis.
It does this in three steps:

    1) Transfrom the GM probability map to a GM mask with the same dimensions
       as the fMRI BOLD data

    2) Regress out the user specified confounds in addition to detrending, frequency filtering,
       and standardizing.

    3) Compare correlation matrices before and after regressing out the confounds.

positional arguments:
  yaml                YAML configuration file. Information about each input
                      parameter and output files are described in the YAML
                      template file.

optional arguments:
  -h, --help          show this help message and exit
  -g, --get_template  Copy the YAML template to the current directory. This
                      template can be used as a starting point.
  -p, --print_yaml    Print YAML template to stdout.
  -v, --verbose       Boolean flag to display more information to stdout.


# YAML Template
```
# YAML file for netprep workflow.
#
#
netprep_methods_dir: ../methods

fmri: <str, fmri_4D_bold_nifti_filename>

gm_probmap: <str, gray_matter_probability_map_nifti_filename>
gm_mask_threshold: <float, gray_matter_probability_threshold_to_create_mask>

nilearn_nifti_masker:
        confounds: <str, confounds_csv_filename>
        kind: correlation
        standardize: True
        smoothing_fwhm: 8
        detrend: True
        low_pass:
        high_pass:
        t_r:


# YAML inputs explained:
#
#  fmri          : filename of 4D BOLD NIFTI file
#
#  gm_probmap    : filename of gray matter probability map (GMPM). The fMRI NIFTI file and
#                  GMPM file MUST be in the same space but they do not have to have the same
#                  dimensions. The GMPM will be transformed by ANTS into the same space
#                  as the fMRI data.  The GMPM will also be converted into a GM mask according
#                  to the user specified threshold (gm_threshold).  If one already has a mask
#                  in the same space as the fMRI just enter it as the gm_probtissue and set
#                  the gm_threshold equal to 0.
#
#  gm_threshold  : Threshold to convert the GMPM to a mask. The mask will then be used in
#                  nilearn's NIFTIMASKER.
#
#  The remaining set of inputs control how the correlation matrix is created with nilearn.
#  Links to nilearn are below. I have simply copied the appropriate documentation for
#  each input parameter.
#
#  nilearn_nifti_masker:
#
#      confounds:  A CSV filename containing a list of confounds to be removed from fMRI
#                  4D BOLD NIFTI file. The CSV file contains a header containing
#                  a list of confounds. Each row corresponds to one volume of the fMRI
#                  4D BOLD NIFTI file.  For this reason, the number of rows in the
#                  CSV file must equal the number of volumes in the 4D BOLD NIFTI file.
#                  While it is expected that users will be using a subset of the
#                  confounds created by fmriprep.  The user may add one or more additional
#                  confounds that were calculated by other means.  The easiest
#                  way to work with CSV files on the command line is csvkit.
#
#       kind : correlation
#
#       standardize: boolean, optional. If standardize is True, the time-series are
#                    centered and normed: their mean is put to 0 and their variance
#                    to 1 in the time dimension.
#
#       smoothing_fwhm : float, optional  If smoothing_fwhm is not None, it gives the
#                        full-width half maximum in millimeters of the spatial
#                        smoothing to apply to the signal.
#
#       detrend: boolean, optional. If detrending should be applied on timeseries
#                (before confound removal)
#
#       low_pass: None or float, optional. low cutoff frequency for filtering the fMRI
#                bold signal, in Hertz.
#
#       high_pass: None or float, optional. high cutoff frequency for filtering the
#                 fMRI bold signal, in Hertz.
#
#       t_r: float, Repetition time, in second (sampling period). This parameter must
#                   be defined if lowpass or highpass are defined.
#
# netprep.py Outputs explained:
#
#   The netprep workflow takes a 4D fMRI NIFTI file and performs basic preprocessing to
#   prepare the time series for network analysis.  It will also calculate the correlation
#   matrices before and after the confounds have been regressed out.
#
#   gm_mask.nii.gz   : is the gray matter mask derived from the gray matter probability
#                      map.  The gm_mask is in the same space and dimensions of the
#                      fMRI BOLD NIFTI file.
#
#   preproc_mean.nii.gz  : is the mean of the fMRI BOLD 4D file.
#
#   fmri_confounds_kept.nii.gz  :  fMRI BOLD 4D file before confound regression. All other
#                                  methods of preprocessing have been applied as selected
#                                  by the user. Detrending low-pass filtering, high-pass
#                                  filtering, standardizing, and smoothing.
#
#   fmri_confounds_kept_correlation_matrix.mat :  Correlation matrix of fmri_confounds_bold.nii.gz
#                                                 stored as a Matlab mat file.
#
#   fmri_confounds_removed.nii.gz  - fMRI BOLD 4D file after regression. Processing is identical
#                                    to fmri_confounds_kept.nii.gz with the addition of the
#                                    confounds being regressed out of the signal.
#
#   fmri_confounds_removed_correlation_matrix.mat : Correlation matrix of
#                                                   fmri_confounds_removed.nii.gz stored as a
#                                                   Matlab mat file.
#
#   correlation_histogram_comparison.png :  This is a png file that plots the histograms
#                                           of the correlation matrices before and after
#                                           confound regression.
#
#   netprep.yaml  - The input YAML file is copied to the results directory for reference.
#
#
# References
#
#   csvkit                       : https://csvkit.readthedocs.io/en/1.0.2/
#   NiLearn Connectivity Measure : http://nilearn.github.io/modules/generated/nilearn.connectome.ConnectivityMeasure.html
#   NiLearn NiftiMasker          : http://nilearn.github.io/modules/generated/nilearn.input_data.NiftiMasker.html
#   NiLearn.signal.clean         : http://nilearn.github.io/modules/generated/nilearn.signal.clean.html#nilearn.signal.clean

```


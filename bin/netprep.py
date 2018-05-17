#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
network preprocessing workflow
"""

import shutil
import yaml
import pprint
import os
import argparse
import textwrap

from nipype.interfaces.ants import ApplyTransforms
import nipype.interfaces.io as nio  # Data i/o
import nipype.interfaces.fsl as fsl  # fsl
import nipype.interfaces.utility as niu  # utility
import nipype.pipeline.engine as pe  # pypeline engine

netprep_yaml_template_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'netprep.yaml.template')

# Set NIFTI files created by FSL to be saved with compression
fsl.FSLCommand.set_default_output_type('NIFTI_GZ')

# identity flag doesn't work in NiPype.  Submitted enhancement request. In the meantime create identity affine
# transform.
identity_transform = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'identity.txt')


def _nilearn_compare_compcorr(correlation_matrix1_filename,
                              correlation_matrix2_filename,
                              subsample=1,
                              verbose=False
                              ):
    """
    Compare two correlation matrices. This function will create a PNG figure of histograms of the correlation
    matrices overlaid on each other.

    :param correlation_matrix1_filename: Matlab mat filename of the correlation matrix 1 (before regressing out
    confounds).

    :param correlation_matrix2_filename: Matlab mat filename of the correlation matrix 2 (after regressing out
    confounds.)

    :param subsample: Subsample is the factor at which the correlation matrices will be downsampled when plotting the
    histograms.

    :param verbose:  Boolean flag to display additional information to standard out.

    :return: filename of the histogram plot comparing the two correlation matrices.

    """
    import os
    import scipy.io as sio
    import matplotlib.pyplot as plt
    import numpy
    import scipy.stats

    # NiPype requires that import statements and function definitions are defined within the calling function.

    def _get_correlation_matrix(in_filename, zero_diagonal=True, flatten_array=True, subsample=subsample):
        mat = sio.loadmat(in_filename)

        cmatrix = mat['correlation_matrix']
        cmatrix = cmatrix / cmatrix[0, 0]  # Normalize. Only necessary if saved as an int

        if zero_diagonal:
            numpy.fill_diagonal(cmatrix, 0)

        if (subsample is not None) & (subsample > 0):
            cmatrix = cmatrix[0::subsample, 0::subsample]

        if flatten_array:
            cmatrix = cmatrix.flatten()

        return cmatrix

    def _stats(correlation_matrix, verbose=False):
        """

        :param correlation_matrix: correlation matrix
        :return: (mean, std, skewness, kurtosis)
        """

        nhist_stats = (scipy.stats.tmean(correlation_matrix),
                       scipy.stats.tstd(correlation_matrix),
                       scipy.stats.skew(correlation_matrix),
                       scipy.stats.kurtosis(correlation_matrix),
                       )

        if verbose:
            print(nhist_stats)

        return nhist_stats

    correlation_matrix1 = _get_correlation_matrix(correlation_matrix1_filename, subsample=subsample)
    correlation_matrix2 = _get_correlation_matrix(correlation_matrix2_filename, subsample=subsample)

    out_filename = os.path.abspath('correlation_histogram_comparison.png')

    fig = plt.figure()

    n1, _, _ = plt.hist(correlation_matrix1, 101, alpha=0.5, label='before', facecolor='red', ec='red');
    n2, _, _ = plt.hist(correlation_matrix2, 101, alpha=0.5, label='after', facecolor='green', ec='green');

    # At this time, stats are calculated and printed but not stored.
    cm_stats1 = _stats(correlation_matrix1, verbose=verbose)
    cm_stats2 = _stats(correlation_matrix2, verbose=verbose)

    plt.legend(loc='upper right')
    plt.title('Correlation Coefficient Histogram Before and After CompCorr')
    plt.xlabel('Correlation Coefficient')
    plt.xlim(-1.0, 1.0)
    plt.ylabel('Count')
    fig.savefig(out_filename)

    return out_filename


def _nilearn_remove_confounds(in_file,
                              mask_file,
                              confounds=None,
                              kind='correlation',
                              standardize=True,
                              smoothing_fwhm=8,
                              low_pass=None,
                              high_pass=None,
                              t_r=None,
                              detrend=True,
                              out_filename='fmri_confounds_removed.nii.gz',
                              out_correlation_matrix='correlation_matrix.mat',
                              subsample=32,
                              ):
    """

    :param in_file: 4D NIFTI BOLD filename.

    :param mask_file: 3D NIFTI mask filename. Mask is used by nilearn to regress out signals from specific regions.
                      Typically, one will pass in a gray matter mask.  The mask must be the same dimensions as the
                      in_file.

    :param confounds: CSV filename of the confounds.

    :param kind: Methods of correlation when calculating correlation matrix with nilearn. Acceptable options are
                {correlation, partial correlation, tangent, covariance, precision}. Default is correlation

    :param standardize : boolean, optional  If standardize is True, the time-series are centered and normed: their
    mean is put to 0 and their variance to 1 in the time dimension.

    :param smoothing_fwhm:

    :param detrend : boolean, optional. This parameter is passed to signal.clean. Please see the related
    documentation for details

    :param low_pass: None or float, optional. This parameter is passed to signal.clean. Please see the related
    documentation for details

    :param high_pass: None or float, optional. This parameter is passed to signal.clean. Please see the related
    documentation for details

    :param t_r: None or float, optional. This parameter is passed to signal.clean. Please see the related
    documentation for details

    :param out_filename:
    :param out_correlation_matrix:
    :return:


    Parameter help for kind, standardize, smoothing_fwhm, detrend,

    References:
    http://nilearn.github.io/modules/generated/nilearn.connectome.ConnectivityMeasure.html
    http://nilearn.github.io/modules/generated/nilearn.input_data.NiftiMasker.html
    """

    from nilearn import input_data
    import nibabel
    import os
    from nilearn.connectome import ConnectivityMeasure
    import scipy.io as sio

    # NiPype requires that import statements and function definitions are defined within the calling function.

    def _calc_correlation_matrix(data, out_correlation_matrix=None, kind='correlation'):
        correlation_measure = ConnectivityMeasure(kind=kind)
        correlation_matrix = (correlation_measure.fit_transform([data])[0])

        if out_correlation_matrix is not None:
            out_correlation_matrix = os.path.abspath(out_correlation_matrix)

            print(correlation_matrix.shape)
            print(correlation_matrix[::subsample, ::subsample].shape)
            sio.savemat(out_correlation_matrix, {f'correlation_matrix_ss{subsample}': correlation_matrix[::subsample, ::subsample]})

        return out_correlation_matrix

    nifti_masker = input_data.NiftiMasker(mask_img=mask_file,
                                          standardize=standardize,
                                          smoothing_fwhm=smoothing_fwhm,
                                          detrend=detrend,
                                          low_pass=low_pass,
                                          high_pass=high_pass,
                                          t_r=t_r)

    nifti_masker.fit(in_file)

    # Remove specified confounds. If confounds set to None other processing is still applied.
    fmri_confounds_removed = nifti_masker.transform(in_file, confounds=confounds)

    # Save the NIFTI file.
    out_filename = os.path.abspath(out_filename)
    nibabel.save(nifti_masker.inverse_transform(fmri_confounds_removed), os.path.abspath(out_filename))

    # Calculate correlation matrix
    out_correlation_matrix = _calc_correlation_matrix(fmri_confounds_removed, out_correlation_matrix, kind=kind)

    # It is very important that filenames returned from NiPype workflow functions have absolute filenames.
    # IF they don't they will not be saved to nodes base directory.
    return out_filename, out_correlation_matrix


def init_netprep_wf(netprep_io, verbose):
    """
    """

    # --- Input Node
    netprep_inputnode = pe.Node(interface=niu.IdentityInterface(fields=['fmri', 'gm_probmap', 'fmri_confounds_tsv']),
                                name='netprep_inputnode')

    netprep_inputnode.inputs.fmri = netprep_io['fmri']
    netprep_inputnode.inputs.gm_probmap = netprep_io['gm_probmap']

    # --- Calculate mean of fMRI BOLD NIFTI file.
    #
    #  This step is required so the resampling of the GM tissue probability map has a
    #  3D file as a reference file.

    fslmean = pe.Node(interface=fsl.ImageMaths(op_string='-Tmean',
                                               out_file=netprep_io['fmri_mean']),
                      name='fslmean')

    # --- Transform GM tissue probability to bold_space
    #
    #  The GM tissue probability map is required to be in the same space as the fMRI BOLD nifti file.
    #  While they are already in the same space this node transforms the GM probability map to the same
    #  dimensions.
    #
    resample_gm_probmap = pe.Node(interface=ApplyTransforms(dimension=3,
                                                            transforms=[identity_transform],
                                                            output_image=netprep_io['gm_probmap_bold_space'],
                                                            interpolation='Linear',
                                                            default_value=0,
                                                            invert_transform_flags=[False]
                                                            ),
                                  name='resample_gm_probmap')

    # --- Create GM mask
    #
    #  This node will convert the resampled GM tissue probability map into a simple mask. This GM mask
    #  will be used for by nilearn for calculating the NIFTIMASKER object.
    #
    create_gm_mask = pe.Node(interface=fsl.ImageMaths(op_string='-thr {0} -bin'.format(netprep_io['gm_mask_threshold']),
                                                      out_file=netprep_io['gm_mask']),
                             name='create_gm_mask')

    # --- nilearn preprocessing and regressing out confounds
    #
    # nilearn has a fantastic function to regress out confounds and apply other preprocessing steps on the fMRI BOLD
    # signal. An function interface node has been created perform this network preprocessing.
    #

    nilearn_remove_confounds = pe.Node(interface=niu.Function(input_names=['in_file',
                                                                           'mask_file',
                                                                           'confounds',
                                                                           'out_filename',
                                                                           'out_correlation_matrix',
                                                                           'kind',
                                                                           'standardize',
                                                                           'smoothing_fwhm',
                                                                           'detrend',
                                                                           't_r',
                                                                           'low_pass',
                                                                           'high_pass'
                                                                           ],
                                                              output_names=['out_filename',
                                                                            'correlation_matrix'
                                                                            ],
                                                              function=_nilearn_remove_confounds),
                                       name='nilearn_remove_confounds')

    nilearn_remove_confounds.inputs.confounds = netprep_io['nilearn_nifti_masker']['confounds']
    nilearn_remove_confounds.inputs.out_filename = 'fmri_confounds_removed.nii.gz'
    nilearn_remove_confounds.inputs.out_correlation_matrix = 'fmri_confounds_removed_correlation_matrix.mat'
    nilearn_remove_confounds.inputs.kind = netprep_io['nilearn_nifti_masker']['kind']
    nilearn_remove_confounds.inputs.standardize = netprep_io['nilearn_nifti_masker']['standardize']
    nilearn_remove_confounds.inputs.smoothing_fwhm = netprep_io['nilearn_nifti_masker']['smoothing_fwhm']
    nilearn_remove_confounds.inputs.detrend = netprep_io['nilearn_nifti_masker']['detrend']
    nilearn_remove_confounds.inputs.t_r = netprep_io['nilearn_nifti_masker']['t_r']
    nilearn_remove_confounds.inputs.low_pass = netprep_io['nilearn_nifti_masker']['low_pass']
    nilearn_remove_confounds.inputs.high_pass = netprep_io['nilearn_nifti_masker']['high_pass']

    # --- nilearn preprocessing without regressing out confounds.
    #
    # This step is the same as above but regressing out the confounds is skipped.  This allows comparison
    # of the correlation matrices to be compared.

    nilearn_keep_confounds = pe.Node(interface=niu.Function(input_names=['in_file',
                                                                         'mask_file',
                                                                         'confounds',
                                                                         'out_filename',
                                                                         'out_correlation_matrix',
                                                                         'kind',
                                                                         'standardize',
                                                                         'smoothing_fwhm',
                                                                         'detrend'
                                                                         ],
                                                            output_names=['out_filename',
                                                                          'correlation_matrix'
                                                                          ],
                                                            function=_nilearn_remove_confounds),
                                     name='nilearn_keep_confounds')

    nilearn_keep_confounds.inputs.out_filename = 'fmri_confounds_kept.nii.gz'
    nilearn_keep_confounds.inputs.out_correlation_matrix = 'fmri_confounds_kept_correlation_matrix.mat'
    nilearn_keep_confounds.inputs.confounds = None
    nilearn_keep_confounds.inputs.kind = netprep_io['nilearn_nifti_masker']['kind']
    nilearn_keep_confounds.inputs.standardize = netprep_io['nilearn_nifti_masker']['standardize']
    nilearn_keep_confounds.inputs.smoothing_fwhm = netprep_io['nilearn_nifti_masker']['smoothing_fwhm']
    nilearn_keep_confounds.inputs.detrend = netprep_io['nilearn_nifti_masker']['detrend']
    nilearn_keep_confounds.inputs.t_r = netprep_io['nilearn_nifti_masker']['t_r']
    nilearn_keep_confounds.inputs.low_pass = netprep_io['nilearn_nifti_masker']['low_pass']
    nilearn_keep_confounds.inputs.high_pass = netprep_io['nilearn_nifti_masker']['high_pass']
    nilearn_keep_confounds.inputs.subsample = netprep_io['nilearn_nifti_masker']['subsample']

    # --- Compare correlation matrix histograms
    #
    # This node calls a user defined function to create a histogram plot of the two histograms for
    # visual comparison.

    nilearn_compare_compcorr = pe.Node(interface=niu.Function(input_names=['correlation_matrix1_filename',
                                                                           'correlation_matrix2_filename',
                                                                           'verbose'],
                                                              output_names=['correlation_histogram_png'],
                                                              function=_nilearn_compare_compcorr),
                                       name='nilearn_compare_compcorr')

    nilearn_compare_compcorr.inputs.verbose = verbose

    # --- Data sink
    #
    # A data sink node was created to save all the intermediate results. The results saved are specified by
    # the workflow connections by connecting output from the desired nodes to the data sink.
    #

    datasink_results = pe.Node(nio.DataSink(), name='datasink_results')
    datasink_results.inputs.base_directory = os.path.abspath(netprep_io['netprep_methods_dir'])

    # --- Connect the individual nodes to create a workflow
    #
    #  Individual nodes are connected so inputs and outputs can be passed from one node to another.
    #  This is a very simple (i.e linear workflow). After the workflow is created connecting nodes
    #  follows a very simple pattern.
    #
    #  netprep_wf.connect([   ( node_a, node_b,[(output_1_node_a, input_1_node_b)]),
    #                        ( node_a, node_c, [(output_2_node_a, input_1_node_c)]),
    #                        ( node_d, node_c, [(output_1_node_d, input_2_node_c)]),
    #                        ...
    #                     ])
    #
    #
    #  The order of how the nodes are connected is irrelevant.  A graphical representation of the nodes
    #  can be found in the workflows working directory.

    netprep_wf = pe.Workflow(name='netprep_wf')
    netprep_wf.base_dir = netprep_io['netprep_methods_dir']

    netprep_wf.connect([(netprep_inputnode, fslmean, [('fmri', 'in_file')]),

                        (fslmean, resample_gm_probmap, [('out_file', 'reference_image')]),
                        (netprep_inputnode, resample_gm_probmap, [('gm_probmap', 'input_image')]),

                        (resample_gm_probmap, create_gm_mask, [('output_image', 'in_file')]),

                        (create_gm_mask, nilearn_remove_confounds, [('out_file', 'mask_file')]),
                        (netprep_inputnode, nilearn_remove_confounds, [('fmri', 'in_file')]),

                        (create_gm_mask, nilearn_keep_confounds, [('out_file', 'mask_file')]),
                        (netprep_inputnode, nilearn_keep_confounds, [('fmri', 'in_file')]),

                        (nilearn_keep_confounds, nilearn_compare_compcorr, [('correlation_matrix',
                                                                             'correlation_matrix1_filename')]),

                        (nilearn_remove_confounds, nilearn_compare_compcorr, [('correlation_matrix',
                                                                               'correlation_matrix2_filename')]),

                        (fslmean, datasink_results, [('out_file', 'results.@fmri_mean')]),

                        (create_gm_mask, datasink_results, [('out_file', 'results.@gm_mask')]),

                        (nilearn_keep_confounds, datasink_results, [('out_filename',
                                                                     'results.@out_preproc_without_compcorr')]),

                        (nilearn_remove_confounds, datasink_results, [('out_filename',
                                                                       'results.@out_preproc_with_compcorr')]),

                        (nilearn_keep_confounds, datasink_results, [('correlation_matrix',
                                                                     'results.@correlation_matrix_without_compcorr')]),

                        (nilearn_remove_confounds, datasink_results, [('correlation_matrix',
                                                                       'results.@correlation_matrix_with_compcorr')]),

                        (nilearn_compare_compcorr, datasink_results, [('correlation_histogram_png',
                                                                       'results.@correlation_histogram_png')])
                        ])

    return netprep_wf


def _add_abs_path_if_necessary(in_abs_path, in_filename):
    """
    Helper function to add the absolute path to a filename if it isn't already defined.
    If in_filename is already defined with an absolute path this function just returns
    in_filename as is.

    :param in_abs_path: Absolute path to be added to the in_filename.
    :param in_filename: Filename to add the absolute path.
    :return: Filename with an absolute path.
    """

    if not os.path.isabs(in_filename):
        abs_filename = os.path.abspath(os.path.join(in_abs_path, in_filename))
    else:
        abs_filename = in_filename

    return abs_filename


def get_netprep_io(yaml_filename, verbose=False):
    """
    Reads YAML configuration file, processes YAML inputs, and sets output filenames.

    :param yaml_filename:  YAML input file for netprep workflow
    :param verbose:  boolean flag to dump out contents of YAML file to stdout.
    :return: dictionary of inputs and output for netprep workflow.
    """

    # === YAML Inputs Definitions

    netprep_io = _read_yaml_config(yaml_filename, verbose=False)

    # Verify that all input files have absolute paths.
    # Filenames that do not have absolute paths are assumed to be in
    # the current directory. We do not check if these files exist. Instead we are relying on
    # nipypes robust reporting method to do this. This may be changed in the future.

    netprep_io['netprep_methods_dir'] = os.path.abspath(netprep_io['netprep_methods_dir'])

    netprep_io['fmri'] = _add_abs_path_if_necessary(os.getcwd(), netprep_io['fmri'])
    netprep_io['nilearn_nifti_masker']['confounds'] = _add_abs_path_if_necessary(os.getcwd(),
                                                                                 netprep_io['nilearn_nifti_masker'][
                                                                                     'confounds'])
    netprep_io['gm_probmap'] = _add_abs_path_if_necessary(os.getcwd(), netprep_io['gm_probmap'])

    # === Outputs

    netprep_io['netprep_confounds_csv'] = 'bold_confounds.csv'
    netprep_io['fmri_mean'] = 'preproc_mean.nii.gz'
    netprep_io['gm_probmap_bold_space'] = 'gm_probmap.nii.gz'
    netprep_io['gm_mask'] = 'gm_mask.nii.gz'

    if verbose:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(netprep_io)

    return netprep_io


def _read_yaml_config(yaml_filename, verbose=False):
    """
    :param yaml_filename:  YAML input file for netprep workflow
    :param verbose:  boolean flag to dump out contents of YAML file to stdout.
    :return: cfg, a dictionary created from a safe_load of the specified YAML file.
    """
    with open(yaml_filename, 'r') as yaml_file:
        cfg = yaml.safe_load(yaml_file)

    if verbose:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(cfg)

    return cfg


def main(yaml_filename, verbose=False):
    """
    Controls flow of nipype netprep workflow.  1) Read YAML, 2) Define nodes and workflow, 3) print workflow,
    4) run workflow.

    :param yaml_filename:  YAML input file for netprep workflow
    :param verbose:  boolean flag to dump out contents of YAML file to stdout.
    :return:
    """

    # Read YAML file and set other outputs
    netprep_io = get_netprep_io(yaml_filename, verbose)

    # Initialize netprep workflow
    netprep_wf = init_netprep_wf(netprep_io, verbose)

    # Write Graph of workflwo
    netprep_wf.write_graph(graph2use='flat')

    netprep_wf.run()

    shutil.copy(yaml_filename, os.path.join(netprep_io['netprep_methods_dir'], 'results'))

    return


def _argparse_description():
    """
    Helper function to provide a description of the function called from the command line.

    :return: str, text description
    """

    return ("""
    
    netprep performs preprocessing on an fMRI BOLD data set to prepare it for network analysis.  
    It does this in three steps:
    
        1) Transfrom the GM probability map to a GM mask with the same dimensions 
           as the fMRI BOLD data
        
        2) Regress out the user specified confounds in addition to detrending, frequency filtering,
           and standardizing. 
           
        3) Compare correlation matrices before and after regressing out the confounds. 
        
    """)


def _argparse_epilog():
    """
    Helper function to provide a description of the function called from the command line.

    :return:
    """
    return ("""    
    """)


if __name__ == '__main__':
    """
    __main__ function definition to run program from command line. 
    """

    usage = "usage: %prog [options] arg1 arg2"

    parser = argparse.ArgumentParser(prog='netprep',
                                     description=textwrap.dedent(_argparse_description()),
                                     epilog=textwrap.dedent(_argparse_epilog()),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("yaml", help=("YAML configuration file.  Information about each input parameter """
                                      """and output files are described in the YAML template file."""))

    parser.add_argument("-g", "--get_template", help=("""Copy the YAML template to the current directory. """
                                                      """This template can be used as a starting point. """),
                        action="store_true", default=False)

    parser.add_argument('-p', '--print_yaml', help=("""Print YAML template to stdout."""),
                        action="store_true", default=False)

    parser.add_argument("-v", "--verbose", help="Boolean flag to display more information to stdout.",
                        action="store_true",
                        default=False)

    in_args = parser.parse_args()

    if in_args.print_yaml:
        with open(netprep_yaml_template_filename, 'r') as f:
            print(f.read())

    if in_args.get_template:
        shutil.copy(netprep_yaml_template_filename,
                    os.getcwd())

    if not (in_args.get_template | in_args.print_yaml):
        main(in_args.yaml, in_args.verbose)

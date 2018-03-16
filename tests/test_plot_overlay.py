# === ETL get_patient_movement_data ===
#
#  This ETL test is performed here because it takes a long time and is critical if the other tests are going to
#  execute properly and pass.
#
import pytest
import os
from tic_core import plot_overlay

t1w_filename = './data/spm/single_subj_T1.nii.gz'


tmap_filename = ('./data/brainomics_localizer/brainomics_data/S01/'
                 't_map_left_auditory_&_visual_click_vs_right_auditory&visual_click.nii.gz'
                 )


def test_plot_overlay_tmap_file_found():
    assert os.path.isfile(tmap_filename)


def test_plot_overlay_t1w_file_found():
    assert os.path.isfile(t1w_filename)

def test_plot_overlay_z():
#     parser.add_argument('overlay', help="Overlay Image")
#     parser.add_argument('--bg_img', help="Background Image")
#
#     parser.add_argument('--out_dir', help="Output directory (./)", default=os.getcwd())
#     parser.add_argument('--display_mode', help="Direction", choices=['x', 'y', 'z', 'ortho'], default='z')
#
#     #    parser.add_argument('--cut_coords', help="Number of slices", nargs='*', type=int, default=[1])
#     parser.add_argument('--nslices', help="Number of slices (5)", type=int, default=5)
#
#     parser.add_argument('--colorbar', help='If True, display a colorbar on the right of the plots (False).',
#                         action="store_true", default=False)
#
#     parser.add_argument('--symmetric_cbar', help=('Specifies whether the colorbar should range from -vmax to vmax or'
#                                                   'from vmin to vmax. Setting to auto will select the latter if the'
#                                                   'range of the whole image is either positive or negative. Note:'
#                                                   'The colormap will always be set to range from -vmax to vmax.'
#                                                   '(False)'),
#                         action="store_true", default=False)
#
#     parser.add_argument('--cmap', help=('Selects colormap for overlay image from a set list. Currently, only colormap '
#                                         'supported is the redblue diverging colormap. Other colormaps are expected '
#                                         'to be added in the future. (redblue)'), default='redblue_bipolar', choices=['redblue'])
#
#     parser.add_argument('--annotate',
#                         help=('If annotate is True, positions and left/right '
#                               'annotation is added to the plot. (false)'),
#                         action="store_true", default=False)
#
#     parser.add_argument('--draw_cross', help=('If draw_cross is True, a cross is drawn on the plot to '
#                                               'indicate the cut plosition. (false)'),
#                         action="store_true", default=False)
#
#     parser.add_argument('--alpha', help='Alpha of overlay image (0.8)', type=float, default=.8)
#
#     parser.add_argument('--vmax', help='Upper bound for plotting, passed to matplotlib.pyplot.imshow',
#                         type=float, default=None)
#
#     parser.add_argument('--dim', help=('Dimming factor applied to background image. By default, automatic heuristics'
#                                        'are applied based upon the background image intensity. Accepted float values,'
#                                        'where a typical scan is -1 to 1 (-1 = increase constrast; '
#                                        '1 = decrease contrast), but larger values can be used for a more pronounced'
#                                        'effect. 0 means no dimming. (0)'),
#                         type=float, default=0)
#
#     parser.add_argument('--threshold', help=('If None is given, the image is not thresholded. '
#                                              'If a number is given, it is used to threshold the image: '
#                                              'values below the threshold (in absolute value) '
#                                              'are plotted as transparent. If auto is given, the threshold '
#                                              'is determined magically by analysis of the image. (None)'),
#                         default=None)
#
#     parser.add_argument('--black_bg', help=('If True, the background of the image is set to be black.'
#                                             'If you wish to save figures with a black background,'
#                                             'you will need to pass facecolor=k, edgecolor=k to '
#                                             'matplotlib.pyplot.savefig. (False)'),
#                         action="store_true", default=False)
#
#     parser.add_argument('-v', '--verbose', help='If True, display a colorbar on the right of the plots. (false)',
#                         action="store_true", default=False)
#
    plot_overlay.plot_overlay_xyz(t1w_filename,
                                  tmap_filename,
                                  'z',
                                  30,
                                  alpha=0.6,
                                  )
                                  #
                                  # threshold=threshold,
                                  # colorbar=inArgs.colorbar, out_dir=inArgs.out_dir,
                                  # black_bg=inArgs.black_bg,
                                  # annotate=inArgs.annotate,
                                  # vmax=inArgs.vmax,
                                  # dim=inArgs.dim,
                                  # cmap=inArgs.cmap,
                                  # symmetric_cbar=inArgs.symmetric_cbar,
                                  # draw_cross=inArgs.draw_cross)


def test_plot_overlay_y():
    plot_overlay.plot_overlay_xyz(t1w_filename,
                                  tmap_filename,
                                  'y',
                                  30,
                                  alpha=0.8,
                                  )


def test_plot_overlay_y():
    # Ortho plots a single ortho slice at the center of the volume
    plot_overlay.plot_overlay_ortho(t1w_filename,
                                    tmap_filename,
                                    'ortho',
                                    5,
                                    alpha=0.6,
                                    draw_cross=True)

#
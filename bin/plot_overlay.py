#!/usr/bin/env python3
# coding: utf-8
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Plots several overlay images using nilearn.plot_stat_map.

http://nilearn.github.io/modules/generated/nilearn.plotting.plot_stat_map.html

"""
from __future__ import division

import os
import sys
import argparse
import plot_overlay


# ======================================================================================================================
# region Main Function
#

def _arg_parse_command_line_interface():

    usage = "usage: %prog [options] arg1 arg2"

    parser = argparse.ArgumentParser(prog='plot_overlay')

    parser.add_argument('overlay', help="Overlay Image")
    parser.add_argument('--bg_img', help="Background Image")

    parser.add_argument('--out_dir', help="Output directory (./)", default=os.getcwd())
    parser.add_argument('--display_mode', help="Direction", choices=['x', 'y', 'z', 'ortho'], default='z')

    #    parser.add_argument('--cut_coords', help="Number of slices", nargs='*', type=int, default=[1])
    parser.add_argument('--nslices', help="Number of slices (5)", type=int, default=5)

    parser.add_argument('--colorbar', help='If True, display a colorbar on the right of the plots (False).',
                        action="store_true", default=False)

    parser.add_argument('--symmetric_cbar', help=('Specifies whether the colorbar should range from -vmax to vmax or'
                                                  'from vmin to vmax. Setting to auto will select the latter if the'
                                                  'range of the whole image is either positive or negative. Note:'
                                                  'The colormap will always be set to range from -vmax to vmax.'
                                                  '(False)'),
                        action="store_true", default=False)

    parser.add_argument('--cmap', help=('Selects colormap for overlay image from a set list. Currently, only colormap '
                                        'supported is the redblue diverging colormap. Other colormaps are expected '
                                        'to be added in the future. (redblue)'), default='redblue_bipolar', choices=['redblue'])

    parser.add_argument('--annotate',
                        help=('If annotate is True, positions and left/right '
                              'annotation is added to the plot. (false)'),
                        action="store_true", default=False)

    parser.add_argument('--draw_cross', help=('If draw_cross is True, a cross is drawn on the plot to '
                                              'indicate the cut plosition. (false)'),
                        action="store_true", default=False)

    parser.add_argument('--alpha', help='Alpha of overlay image (0.8)', type=float, default=.8)

    parser.add_argument('--vmax', help='Upper bound for plotting, passed to matplotlib.pyplot.imshow',
                        type=float, default=None)

    parser.add_argument('--dim', help=('Dimming factor applied to background image. By default, automatic heuristics'
                                       'are applied based upon the background image intensity. Accepted float values,'
                                       'where a typical scan is -1 to 1 (-1 = increase constrast; '
                                       '1 = decrease contrast), but larger values can be used for a more pronounced'
                                       'effect. 0 means no dimming. (0)'),
                        type=float, default=0)

    parser.add_argument('--threshold', help=('If None is given, the image is not thresholded. '
                                             'If a number is given, it is used to threshold the image: '
                                             'values below the threshold (in absolute value) '
                                             'are plotted as transparent. If auto is given, the threshold '
                                             'is determined magically by analysis of the image. (None)'),
                        default=None)

    parser.add_argument('--black_bg', help=('If True, the background of the image is set to be black.'
                                            'If you wish to save figures with a black background,'
                                            'you will need to pass facecolor=k, edgecolor=k to '
                                            'matplotlib.pyplot.savefig. (False)'),
                        action="store_true", default=False)

    parser.add_argument('-v', '--verbose', help='If True, display a colorbar on the right of the plots. (false)',
                        action="store_true", default=False)

    in_args = parser.parse_args()

    if in_args.verbose:
        print(in_args.verbose)

    return in_args


def main():

    in_args = _arg_parse_command_line_interface()

    # Setting the threshold like this is necessary to avoid a bug in nilearn.plot_stat_map

    if in_args.threshold == 'auto' or in_args.threshold == None:
        threshold = in_args.threshold
    else:
        threshold = float(in_args.threshold)

    if 'ortho' in in_args.display_mode:

        # Ortho plots a single ortho slice at the center of the volume
        plot_overlay.plot_overlay_ortho(in_args.bg_img,
                                        in_args.overlay,
                                        in_args.display_mode,
                                        in_args.nslices,
                                        alpha=in_args.alpha,
                                        threshold=threshold,
                                        colorbar=in_args.colorbar,
                                        out_dir=in_args.out_dir,
                                        black_bg=in_args.black_bg,
                                        annotate=in_args.annotate,
                                        vmax=in_args.vmax,
                                        dim=in_args.dim,
                                        cmap=in_args.cmap,
                                        symmetric_cbar=in_args.symmetric_cbar,
                                        draw_cross=in_args.draw_cross)

    else:

        # Plots a series of slices
        plot_overlay.plot_overlay_xyz(in_args.bg_img,
                                      in_args.overlay,
                                      in_args.display_mode,
                                      in_args.nslices,
                                      alpha=in_args.alpha,
                                      threshold=threshold,
                                      colorbar=in_args.colorbar, out_dir=in_args.out_dir,
                                      black_bg=in_args.black_bg,
                                      annotate=in_args.annotate,
                                      vmax=in_args.vmax,
                                      dim=in_args.dim,
                                      cmap=in_args.cmap,
                                      symmetric_cbar=in_args.symmetric_cbar,
                                      draw_cross=in_args.draw_cross)


# endregion

if __name__ == "__main__":
    sys.exit(main())
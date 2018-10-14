#!/usr/bin/env python3

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
import datetime
from collections import OrderedDict
import getpass
import subprocess


def _calc_lesion_properties(lesion_label_filename, verbose=False):

    df_label_stats = labels.properties(lesion_label_filename)

    number_of_lesions, _ = df_label_stats.shape

    label_stats = {'number_of_lesions':number_of_lesions }

    if label_stats['number_of_lesions'] > 0:
        label_stats['total_lesion_volume'] = df_label_stats['volume_mm3'].sum()
        label_stats['mean_lesion_volume'] = df_label_stats['volume_mm3'].mean()
        label_stats['std_lesion_volume'] = df_label_stats['volume_mm3'].std()
        label_stats['min_lesion_volume'] = df_label_stats['volume_mm3'].min()
        label_stats['max_lesion_volume'] = df_label_stats['volume_mm3'].max()

    else:
        label_stats['total_lesion_volume'] = 0
        label_stats['mean_lesion_volume'] =  0
        label_stats['std_lesion_volume'] = 0
        label_stats['min_lesion_volume'] = 0
        label_stats['max_lesion_volume'] = 0

    return label_stats


def _calc_volumes_in_tissue_regions( tissue_mask,  mask, verbose=False ):

    df_properties = labels.properties(tissue_mask)
    df_measure    = labels.measure(tissue_mask, mask, binarize_image=True)

    tissue_volume = df_properties['volume_mm3'].values[0]
    label_fraction_volume_in_tissue = df_measure['mean'].values[0]

    label_volume_in_tissue = tissue_volume * label_fraction_volume_in_tissue

    output_metrics = (label_volume_in_tissue, label_fraction_volume_in_tissue, tissue_volume)

    if verbose:
        print( output_metrics )

    return output_metrics 

    


def cenc_stats(input_dir, in_image, out_json, instrument_prefix='', verbose=False):
    """ Write MagTrans Instrument to JSON output file"""

    cenc_dirs = cenc.directories( input_dir )

    if verbose:
         print(cenc_dirs['results']['dirs']['labels'])

    tissue_labels = {'gm_cerebral':    os.path.join( cenc_dirs['results']['dirs']['labels'], 'gm.cerebral_cortex.nii.gz'),
                     'gm_subcortical': os.path.join( cenc_dirs['results']['dirs']['labels'], 'gm.subcortical.nii.gz'),
                     'wm_cerebral':    os.path.join( cenc_dirs['results']['dirs']['labels'], 'wm.cerebral.nii.gz'),
                     'wm_lesions':     os.path.join( cenc_dirs['results']['dirs']['labels'], 'wmlesions_lpa_mask.nii.gz')
              }
    
    label_stats = _calc_lesion_properties(in_image, verbose=False)

    pandas.set_option('expand_frame_repr', False)

    (gm_cortical_label_volume, 
     gm_cortical_label_fraction, 
     gm_cortical_volume) = _calc_volumes_in_tissue_regions( tissue_labels['gm_cerebral'], in_image, verbose=False)

    (gm_subcortical_label_volume, 
     gm_subcortical_label_fraction, 
     gm_subcortical_volume) = _calc_volumes_in_tissue_regions( tissue_labels['gm_subcortical'], in_image, verbose=False)

    (wm_cerebral_label_volume, 
     wm_cerebral_label_fraction, 
     wm_cerebral_volume) = _calc_volumes_in_tissue_regions( tissue_labels['wm_cerebral'], in_image, verbose=False)

    (wm_lesions_label_volume, 
     wm_lesions_label_fraction, 
     wm_lesions_volume) = _calc_volumes_in_tissue_regions( tissue_labels['wm_lesions'], in_image, verbose=False)

    # CAHMOD:  if in_image contains 'edit', then put _ed at end of key

    if im_image.contains('edit'):

        dict_stats = OrderedDict(( ('subject_id_ed', cenc_dirs['cenc']['id']),
                               ( instrument_prefix + 'analyst_ed', getpass.getuser()),
                               ( instrument_prefix + 'datetime_ed', '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())),
                               ( instrument_prefix + 'image_ed', in_image),

                               (instrument_prefix +'lesions_number_ed', '{0:d}'.format(int(label_stats['number_of_lesions']))),
                               (instrument_prefix +'lesions_total_volume_mm3_ed', '{0:5.1f}'.format(label_stats['total_lesion_volume'])),
                               (instrument_prefix +'lesions_mean_volume_mm3_ed', '{0:5.1f}'.format(label_stats['mean_lesion_volume'])),
                               (instrument_prefix +'lesions_std_volume_mm3_ed', '{0:5.1f}'.format(label_stats['std_lesion_volume'])),
                               (instrument_prefix +'lesions_min_lesion_volume_mm3_ed', '{0:5.1f}'.format(label_stats['min_lesion_volume'])),
                               (instrument_prefix +'lesions_max_lesion_volume_mm3_ed', '{0:5.1f}'.format(label_stats['max_lesion_volume'])),

                               ( instrument_prefix + 'gm_cortical_volume_mm3_ed', '{0:4.3f}'.format( gm_cortical_volume)),
                               ( instrument_prefix + 'gm_cortical_label_volume_mm3_ed', '{0:4.3f}'.format( gm_cortical_label_volume)),
                               ( instrument_prefix + 'gm_cortical_label_fraction_ed', '{0:4.3f}'.format( gm_cortical_label_fraction)),

                               ( instrument_prefix + 'gm_subcortical_volume_mm3_ed', '{0:4.3f}'.format( gm_subcortical_volume)),
                               ( instrument_prefix + 'gm_subcortical_label_volume_mm3_ed', '{0:4.3f}'.format( gm_subcortical_label_volume)),
                               ( instrument_prefix + 'gm_subcortical_label_fraction_ed', '{0:4.3f}'.format( gm_subcortical_label_fraction)),

                               ( instrument_prefix + 'wm_cerebral_volume_mm3_ed', '{0:4.3f}'.format( wm_cerebral_volume)),
                               ( instrument_prefix + 'wm_cerebral_label_volume_mm3_ed', '{0:4.3f}'.format( wm_cerebral_label_volume)),
                               ( instrument_prefix + 'wm_cerebral_label_fraction_ed', '{0:4.3f}'.format( wm_cerebral_label_fraction)),

                               ( instrument_prefix + 'wm_lesions_volume_mm3_ed', '{0:4.3f}'.format( wm_lesions_volume)),
                               ( instrument_prefix + 'wm_lesions_label_volume_mm3_ed', '{0:4.3f}'.format( wm_lesions_label_volume)),
                               ( instrument_prefix + 'wm_lesions_label_fraction_ed', '{0:4.3f}'.format( wm_lesions_label_fraction))

                               )
                              )
    else:
        dict_stats = OrderedDict(( ('subject_id', cenc_dirs['cenc']['id']),
                               ( instrument_prefix + 'analyst', getpass.getuser()),
                               ( instrument_prefix + 'datetime', '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())),
                               ( instrument_prefix + 'image', in_image),

                               (instrument_prefix +'lesions_number', '{0:d}'.format(int(label_stats['number_of_lesions']))),
                               (instrument_prefix +'lesions_total_volume_mm3', '{0:5.1f}'.format(label_stats['total_lesion_volume'])),
                               (instrument_prefix +'lesions_mean_volume_mm3', '{0:5.1f}'.format(label_stats['mean_lesion_volume'])),
                               (instrument_prefix +'lesions_std_volume_mm3', '{0:5.1f}'.format(label_stats['std_lesion_volume'])),
                               (instrument_prefix +'lesions_min_lesion_volume_mm3', '{0:5.1f}'.format(label_stats['min_lesion_volume'])),
                               (instrument_prefix +'lesions_max_lesion_volume_mm3', '{0:5.1f}'.format(label_stats['max_lesion_volume'])),

                               ( instrument_prefix + 'gm_cortical_volume_mm3', '{0:4.3f}'.format( gm_cortical_volume)),
                               ( instrument_prefix + 'gm_cortical_label_volume_mm3', '{0:4.3f}'.format( gm_cortical_label_volume)),
                               ( instrument_prefix + 'gm_cortical_label_fraction', '{0:4.3f}'.format( gm_cortical_label_fraction)),

                               ( instrument_prefix + 'gm_subcortical_volume_mm3', '{0:4.3f}'.format( gm_subcortical_volume)),
                               ( instrument_prefix + 'gm_subcortical_label_volume_mm3', '{0:4.3f}'.format( gm_subcortical_label_volume)),
                               ( instrument_prefix + 'gm_subcortical_label_fraction', '{0:4.3f}'.format( gm_subcortical_label_fraction)),

                               ( instrument_prefix + 'wm_cerebral_volume_mm3', '{0:4.3f}'.format( wm_cerebral_volume)),
                               ( instrument_prefix + 'wm_cerebral_label_volume_mm3', '{0:4.3f}'.format( wm_cerebral_label_volume)),
                               ( instrument_prefix + 'wm_cerebral_label_fraction', '{0:4.3f}'.format( wm_cerebral_label_fraction)),

                               ( instrument_prefix + 'wm_lesions_volume_mm3', '{0:4.3f}'.format( wm_lesions_volume)),
                               ( instrument_prefix + 'wm_lesions_label_volume_mm3', '{0:4.3f}'.format( wm_lesions_label_volume)),
                               ( instrument_prefix + 'wm_lesions_label_fraction', '{0:4.3f}'.format( wm_lesions_label_fraction))

                               )
                              )


    if out_json==None:
         json_stats_filename =  in_image.replace( 'nii.gz', 'json')
    else:
         json_stats_filename = out_json
         
    if verbose:
         print( json_stats_filename )

    with open(json_stats_filename, 'w') as outfile:
         json.dump(dict_stats, outfile, indent=4, ensure_ascii=True, sort_keys=False)

    if verbose:
        util.print_json_redcap_instrument(json_stats_filename)

    return

# ======================================================================================================================
#  Main
def main():
    ## Parsing Arguments

    usage = "usage: %prog [options] arg1 arg2"

    parser = argparse.ArgumentParser(prog='cenc_label_volume_tissue_stats')

    parser.add_argument("in_image", help="Input image", default=None )
    parser.add_argument("--in_dir", help="Participant directory", default=os.getcwd())
    parser.add_argument("--out_json", help="Output JSON filename", default=None )
    parser.add_argument("--prefix", help="Instrument Prefix", default='' )

    parser.add_argument('-v', '--verbose', help="Verbose flag", action="store_true", default=False)

    inArgs = parser.parse_args()

    cenc_stats(inArgs.in_dir, inArgs.in_image, inArgs.out_json, inArgs.prefix, inArgs.verbose)


# Main Function

if __name__ == "__main__":
    sys.exit(main())

    

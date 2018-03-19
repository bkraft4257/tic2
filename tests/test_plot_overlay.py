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


# TODO: These three tests should be parameterized.
def test_plot_overlay_z():
    plot_overlay.plot_overlay_xyz(t1w_filename,
                                  tmap_filename,
                                  'z',
                                  30,
                                  alpha=0.6,
                                  )

def test_plot_overlay_y():
    plot_overlay.plot_overlay_xyz(t1w_filename,
                                  tmap_filename,
                                  'y',
                                  30,
                                  alpha=0.8,
                                  )

def test_plot_overlay_x():
    plot_overlay.plot_overlay_xyz(t1w_filename,
                                  tmap_filename,
                                  'x',
                                  30,
                                  alpha=0.8,
                                  )


def test_plot_overlay_ortho():
    # Ortho plots a single ortho slice at the center of the volume
    plot_overlay.plot_overlay_ortho(t1w_filename,
                                    tmap_filename,
                                    'ortho',
                                    5,
                                    alpha=0.6,
                                    draw_cross=True)

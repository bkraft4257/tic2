#!/usr/bin/env bash

# Environment variables

export HFPEF_SCRIPTS_PATH=${TIC_PATH}/studies/hfpef/scripts

export HFPEF_PATH=/gandg/hfpef/
export HFPEF_BIDS_PATH=${HFPEF_PATH}/bids
export HFPEF_IMAGE_ANALYSIS_PATH=${HFPEF_PATH}/image_analysis
export HFPEF_IMAGE_PROCESSING_PATH=${HFPEF_PATH}/image_processing
export HFPEF_IMAGE_PROCESSING_LOG_PATH=${HFPEF_IMAGE_PROCESSING_PATH}/logs

export HFPEF_QC_PATH=${HFPEF_PATH}/qc
export HFPEF_MRIQC_PATH=${HFPEF_QC_PATH}/mriqc

export HFPEF_FMRIPREP_PATH=${HFPEF_IMAGE_PROCESSING_PATH}/fmriprep
export HFPEF_NETPREP_PATH=${HFPEF_IMAGE_PROCESSING_PATH}/netprep
export HFPEF_ACT_PATH=${HFPEF_IMAGE_PROCESSING_PATH}/act   # ANTs Cortical Thickness

export HFPEF_BIDS_CONFIG_FILE=${HFPEF_SCRIPTS_PATH}/hfpef_bids.cfg
export HFPEF_HEUDICONV_PROTOCOL=${HFPEF_SCRIPTS_PATH}/hfpef_protocol.py
export HFPEF_CLEAN_BIDS=${HFPEF_SCRIPTS_PATH}/hfpef_clean_bids.sh

export HFPEF_SUBJECTS_DIR=${HFPEF_IMAGE_PROCESSING_PATH}/freesurfer

export HFPEF_SINGULARITY_USER_BIND_PATHS="/gandg"

export HFPEF_ACROSTIC_REGEX="hf[u|s][0-9]{3}"
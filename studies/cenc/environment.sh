#!/usr/bin/env bash

# Environment variables

export CENC_SCRIPTS_PATH=${TIC_PATH}/studies/cenc/scripts

export CENC_PATH=/cenc/new2018/cenc/
export CENC_BIDS_PATH=${CENC_PATH}/bids
export CENC_IMAGE_ANALYSIS_PATH=${CENC_PATH}/image_analysis
export CENC_IMAGE_PROCESSING_PATH=${CENC_PATH}/image_processing
export CENC_IMAGE_PROCESSING_LOG_PATH=${CENC_IMAGE_PROCESSING_PATH}/logs

export CENC_MRIQC_PATH=${CENC_PATH}/mriqc

export CENC_FMRIPREP_PATH=${CENC_IMAGE_PROCESSING_PATH}/fmriprep
export CENC_NETPREP_PATH=${CENC_IMAGE_PROCESSING_PATH}/netprep

export CENC_BIDS_CONFIG_FILE=${CENC_SCRIPTS_PATH}/CENC_bids.cfg
export CENC_HEUDICONV_PROTOCOL=${CENC_SCRIPTS_PATH}/CENC_protocol.py

export CENC_SUBJECTS_DIR=${CENC_IMAGE_PROCESSING_PATH}/freesurfer

export CENC_SINGULARITY_USER_BIND_PATHS="/cenc -B /gandg"

export CENC_ACROSTIC_REGEX="hf[u|s][0-9]{3}"

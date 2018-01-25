#!/usr/bin/env bash

# Environment variables

export HFPEF_SCRIPTS_PATH=${TIC_PATH}/studies/hfpef/scripts

export HFPEF_PATH=/gandg/hfpef/
export HFPEF_BIDS_PATH=${HFPEF_PATH}/bids
export HFPEF_IMAGE_ANALYSIS_PATH=${HFPEF_PATH}/image_analysis
export HFPEF_IMAGE_PROCESSING_PATH=${HFPEF_PATH}/image_processing
export HFPEF_IMAGE_PROCESSING_LOG_PATH=${HFPEF_IMAGE_PROCESSING_PATH}/log

export HFPEF_MRIQC_PATH=${HFPEF_PATH}/mriqc


export HFPEF_FMRIPREP_PATH=${HFPEF_IMAGE_PROCESSING_PATH}/fmriprep
export HFPEF_NETPREP_PATH=${HFPEF_IMAGE_PROCESSING_PATH}/netprep

export HFPEF_BIDS_CONFIG_FILE=${HFPEF_SCRIPTS_PATH}/hfpef_bids.cfg

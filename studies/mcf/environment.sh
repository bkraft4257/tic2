#!/usr/bin/env bash

# Environment variables

export MCF_SCRIPTS_PATH=${TIC_PATH}/studies/mcf/scripts

export MCF_PATH=/bkraft1/studies/mcf

export MCF_BIDS_PATH=${MCF_PATH}/bids
export MCF_IMAGE_ANALYSIS_PATH=${MCF_PATH}/image_analysis
export MCF_IMAGE_PROCESSING_PATH=${MCF_PATH}/image_processing
export MCF_IMAGE_PROCESSING_LOG_PATH=${MCF_IMAGE_PROCESSING_PATH}/logs

export MCF_QC_PATH=${MCF_PATH}/qc
export MCF_MRIQC_PATH=${MCF_QC_PATH}/mriqc

export MCF_FMRIPREP_PATH=${MCF_IMAGE_PROCESSING_PATH}/fmriprep
export MCF_NETPREP_PATH=${MCF_IMAGE_PROCESSING_PATH}/netprep
export MCF_ACT_PATH=${MCF_IMAGE_PROCESSING_PATH}/act
export MCF_CONN_PATH=${MCF_IMAGE_PROCESSING_PATH}/conn

export MCF_BIDS_CONFIG_FILE=${MCF_BIDS_PATH}/.bids.cfg
export MCF_HEUDICONV_PROTOCOL=${MCF_SCRIPTS_PATH}/mcf_protocol.py

export MCF_SUBJECTS_DIR=${MCF_IMAGE_PROCESSING_PATH}/freesurfer

export MCF_SINGULARITY_USER_BIND_PATHS="/bkraft1 -B /gandg"

export MCF_ACROSTIC_REGEX="mcf[0-9]{4}"
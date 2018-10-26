#!/usr/bin/env bash

# Environment variables

export MFC_SCRIPTS_PATH=${TIC_PATH}/studies/mfc/scripts

export MFC_PATH=/cenc/bkraft/mfc

export MFC_BIDS_PATH=${MFC_PATH}/bids
export MFC_IMAGE_ANALYSIS_PATH=${MFC_PATH}/image_analysis
export MFC_IMAGE_PROCESSING_PATH=${MFC_PATH}/image_processing
export MFC_IMAGE_PROCESSING_LOG_PATH=${MFC_IMAGE_PROCESSING_PATH}/logs

export MFC_QC_PATH=${MFC_PATH}/qc
export MFC_MRIQC_PATH=${MFC_QC_PATH}/mriqc

export MFC_FMRIPREP_PATH=${MFC_IMAGE_PROCESSING_PATH}/fmriprep
export MFC_NETPREP_PATH=${MFC_IMAGE_PROCESSING_PATH}/netprep
export MFC_ACT_PATH=${MFC_IMAGE_PROCESSING_PATH}/act
export MFC_CONN_PATH=${MFC_IMAGE_PROCESSING_PATH}/conn

export MFC_BIDS_CONFIG_FILE=${MFC_BIDS_PATH}/.bids.cfg
export MFC_HEUDICONV_PROTOCOL=${MFC_SCRIPTS_PATH}/mfc_protocol.py
export MFC_CLEAN_BIDS=${MFC_SCRIPTS_PATH}/clean_bids.sh


export MFC_SUBJECTS_DIR=${MFC_IMAGE_PROCESSING_PATH}/freesurfer

export MFC_SINGULARITY_USER_BIND_PATHS="/bkraft1 -B /gandg"
       
export MFC_ACROSTIC_REGEX="mfc[0-9]{3}"
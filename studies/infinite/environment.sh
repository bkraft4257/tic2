#!/usr/bin/env bash


# Environment variables

export INFINITE_FMRIPREP=$FMRIPREP_PATH/poldracklab_fmriprep_latest-2017-11-10-9ae650872d1e.img
export INFINITE_MRIQC=/cenc/software/mriqc/poldracklab_mriqc_latest-2017-08-30-f54388a6fb57.img
export INFINITE_HDC=/cenc/software/heudiconv/nipy_heudiconv-2017-09-26-6bef64b746f6.img

export INFINITE_PATH=/gandg/infinite/imaging_data/
export INFINITE_BIDS_PATH=${INFINITE_PATH}/bids
export INFINITE_IMAGE_PROCESSING_PATH=${INFINITE_PATH}/image_processing
export INFINITE_IMAGE_ANALYSIS_PATH=${INFINITE_PATH}/image_analysis
export INFINITE_IMAGE_PROCESSING_LOG_PATH=${INFINITE_IMAGE_PROCESSING_PATH}/logs
export INFINITE_MRIQC_PATH=${INFINITE_PATH}/mriqc

export INFINITE_BIDS_CONFIG_FILE=${INFINITE_SCRIPTS_PATH}/inf_bids.cfg

export INFINITE_FMRIPREP_PATH=${INFINITE_IMAGE_PROCESSING_PATH}/fmriprep
export INFINITE_NETPREP_PATH=${INFINITE_IMAGE_PROCESSING_PATH}/netprep

export INFINITE_SCRIPTS_PATH=${TIC_PATH}/studies/infinite/scripts

export INFINITE_HEUDICONV_PROTOCOL=${INFINITE_SCRIPTS_PATH}/infinite_protocol.py

export INFINITE_SUBJECTS_DIR=${INFINITE_IMAGE_PROCESSING_PATH}/freesurfer

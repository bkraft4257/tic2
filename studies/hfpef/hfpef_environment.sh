#!/usr/bin/env bash

alias hfpef_help='firefox https://github.com/theimagingcollective/nipype_workflows/wiki/HFPEF-Image-Processing &'

alias hfpef_hdc_old='/cenc/software/heudiconv/python/heudiconv/bin/heudiconv -c dcm2niix -b --minmeta -f /gandg/hfpef/scripts/hfpef_protocol.py -o /gandg/hfpef/bids/ -d "{subject}/{session}/data/dicom/2*/*/*.DCM"'

alias hfpef_hdc='/cenc/software/heudiconv/python/heudiconv/bin/heudiconv -c dcm2niix -b --minmeta -f /gandg/hfpef/scripts/hfpef_protocol.py -o /gandg/hfpef/bids/ -d "{subject}/2*/*/*.DCM"'

alias hfpef_clean_bids='/gandg/hfpef/scripts/hfpef_clean_bids.sh'

alias hfpef_fmriprep='/gandg/hfpef/scripts/fmriprep_hfpef.sh'
alias hfpef_mriqc='/gandg/hfpef/scripts/mriqc_hfpef.sh'

alias hfpef_mriqc_group='mriqc  /gandg/hfpef/bids /gandg/hfpef/mriqc group'

alias hfpef_prepare_netprep='/gandg/hfpef/scripts/prepare_netprep_hfpef.sh'
alias hfpef_netprep='/gandg/bkraft/tic_workflows/nipype_workflows/workflows/netprep.py'


export HFPEF_PATH=/gandg/hfpef/
export HFPEF_BIDS_PATH=${HFPEF_PATH}/bids
export HFPEF_IMAGE_ANALYSIS_PATH=${HFPEF_PATH}/image_analysis
export HFPEF_IMAGE_PROCESSING_PATH=${HFPEF_PATH}/image_processing
export HFPEF_SCRIPTS_PATH=${HFPEF_PATH}/scripts
export HFPEF_MRIQC_PATH=${HFPEF_PATH}/mriqc

export HFPEF_FMRIPREP_PATH=${HFPEF_IMAGE_PROCESSING_PATH}/fmriprep
export HFPEF_NETPREP_PATH=${HFPEF_IMAGE_PROCESSING_PATH}/netprep

alias cdh='cd $HFPEF_PATH'
alias cdhb='cd $HFPEF_BIDS_PATH'
alias cdhin='cd $HFPEF_PATH/incoming;echo;pwd;ls -lrt; echo;'
alias cdhia='cd $HFPEF_IMAGE_ANALYSIS_PATH'
alias cdhip='cd $HFPEF_IMAGE_PROCESSING_PATH'
alias cdhqc='cd $HFPEF_MRIQC_PATH'


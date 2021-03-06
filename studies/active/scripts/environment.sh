#!/usr/bin/env bash

# Environment variables
export HFPEF_PATH=/gandg/hfpef/
export HFPEF_BIDS_PATH=${HFPEF_PATH}/bids
export HFPEF_IMAGE_ANALYSIS_PATH=${HFPEF_PATH}/image_analysis
export HFPEF_IMAGE_PROCESSING_PATH=${HFPEF_PATH}/image_processing
export HFPEF_IMAGE_PROCESSING_WORKING_PATH=${HFPEF_IMAGE_PROCESSING_PATH}/_working
export HFPEF_SCRIPTS_PATH=${HFPEF_PATH}/scripts
export HFPEF_MRIQC_PATH=${HFPEF_PATH}/mriqc

export HFPEF_FMRIPREP_PATH=${HFPEF_IMAGE_PROCESSING_PATH}/fmriprep
export HFPEF_NETPREP_PATH=${HFPEF_IMAGE_PROCESSING_PATH}/netprep

export HFPEF_BIDS_CONFIG_FILE=${HFPEF_SCRIPTS_PATH}/hfpef_bids.cfg

# Aliases
alias rehfpef='source $HFPEF_SCRIPTS_PATH/hfpef_aliases.sh'
alias hfpef_help='firefox https://github.com/theimagingcollective/nipype_workflows/wiki/HFPEF-Image-Processing &'

alias hfpef_bids='bids-validator $HFPEF_BIDS_PATH -c $HFPEF_BIDS_CONFIG_FILE'
alias hfpef_bids_validitor='bids-validator $HFPEF_BIDS_PATH -c $HFPEF_BIDS_CONFIG_FILE'
alias hfpef_bv='bids-validator $HFPEF_BIDS_PATH -c $HFPEF_BIDS_CONFIG_FILE'

alias hfpef_hdc='/cenc/software/heudiconv/python/heudiconv/bin/heudiconv -c dcm2niix -b --minmeta -f /gandg/hfpef/scripts/hfpef_protocol.py -o /gandg/hfpef/bids/ -d "{subject}/2*/*/*.DCM"'

alias hfpef_display_bids='/gandg/hfpef/scripts/hfpef_display_bids.sh'
alias hfpef_bids_display='/gandg/hfpef/scripts/hfpef_display_bids.sh'

alias hfpef_clean_bids='/gandg/hfpef/scripts/hfpef_bids_clean.sh'
alias hfpef_bids_clean='/gandg/hfpef/scripts/hfpef_bids_clean.sh'

alias hfpef_fmriprep='/gandg/hfpef/scripts/hfpef_fmriprep.sh'
alias hfpef_mriqc='/gandg/hfpef/scripts/hfpef_mriqc.sh'

alias hfpef_mriqc_group='mriqc  /gandg/hfpef/bids /gandg/hfpef/mriqc group'

alias hfpef_gi_netprep_epi='/gandg/hfpef/scripts/hfpef_gi_netprep_epi.sh'
alias hfpef_gi_netprep_mbepi='/gandg/hfpef/scripts/hfpef_gi_netprep_mbepi.sh'

alias hfpef_gi_netprep='/gandg/hfpef/scripts/hfpef_gi_netprep.sh'
alias hfpef_netprep='/gandg/tic/nipype_workflows/netprep.py'


alias cdh='cd $HFPEF_PATH'
alias cdhb='cd $HFPEF_BIDS_PATH'
alias cdhin='cd $HFPEF_PATH/incoming;echo;pwd;ls -lrt; echo;'
alias cdhia='cd $HFPEF_IMAGE_ANALYSIS_PATH'
alias cdhip='cd $HFPEF_IMAGE_PROCESSING_PATH'
alias cdhipl='cd $HFPEF_IMAGE_PROCESSING_PATH/fmriprep_logs'
alias cdhqc='cd $HFPEF_MRIQC_PATH'
alias cdhs='cd $HFPEF_SCRIPTS_PATH'


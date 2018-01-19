#!/usr/bin/env bash

alias syn_hdc='/cenc/software/heudiconv/python/heudiconv/bin/heudiconv -c dcm2niix -b --minmeta -f /gandg/synergy/scripts/syn_protocol_with_angio.py -o /gandg/synergy/bids/ -d "{subject}/2*/*/*.DCM"'
alias syn_bids='bids-validator $SYNERGY_BIDS_PATH' # -c $SYNERGY_BIDS_CONFIG_FILE
alias syn_clean_bids=${SYNERGY_SCRIPTS_PATH}/syn_clean_bids.sh

alias syn_fmriprep='/gandg/synergy/scripts/syn_fmriprep.sh'
alias syn_mriqc='/gandg/hfpef/scripts/syn_mriqc.sh'
alias syn_mriqc_group='mriqc  $SYNERGY_BIDS_PATH $SYNERGY_MRIQC_PATH group'

alias syn_gi_netprep='/gandg/synergy/scripts/syn_gi_netprep.sh'
alias syn_netprep='netprep.py syn_netprep.yaml'

export SYNERGY_PATH=/gandg/synergy/
export SYNERGY_BIDS_PATH=${SYNERGY_PATH}/bids
export SYNERGY_IMAGE_ANALYSIS_PATH=${SYNERGY_PATH}/image_analysis
export SYNERGY_IMAGE_PROCESSING_PATH=${SYNERGY_PATH}/image_processing
export SYNERGY_SCRIPTS_PATH=${SYNERGY_PATH}/scripts
export SYNERGY_MRIQC_PATH=${SYNERGY_PATH}/mriqc

export SYNERGY_FMRIPREP_PATH=${SYNERGY_IMAGE_PROCESSING_PATH}/fmriprep
export SYNERGY_NETPREP_PATH=${SYNERGY_IMAGE_PROCESSING_PATH}/netprep

export SYNERGY_BIDS_CONFIG_FILE=${SYNERGY_SCRIPTS_PATH}/synergy_bids.cfg

alias cdsyn='cd $SYNERGY_PATH'
alias cdsynb='cd $SYNERGY_BIDS_PATH'
alias cdsynia='cd $SYNERGY_IMAGE_ANALYSIS_PATH'
alias cdsynip='cd $SYNERGY_IMAGE_PROCESS_PATH'
alias cdsynq='cd $SYNERGY_MRIQC_PATH'

alias cds='cd $SYNERGY_PATH'
alias cdsb='cd $SYNERGY_BIDS_PATH'
alias cdsq='cd $SYNERGY_MRIQC_PATH'
alias cdsia='cd $SYNERGY_IMAGE_ANALYSIS_PATH'
alias cdsip='cd $SYNERGY_IMAGE_PROCESSING_PATH'
alias cdsin='cd $SYNERGY_PATH/incoming;echo;pwd;ls -lrt; echo;'
alias cdss='cd $SYNERGY_SCRIPTS_PATH'

alias resyn='source $SYNERGY_SCRIPTS_PATH/synergy_aliases.sh'


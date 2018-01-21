#!/usr/bin/env bash

alias syn_hdc='/cenc/software/heudiconv/python/heudiconv/bin/heudiconv -c dcm2niix -b --minmeta -f $SYNERGY_SCRIPTS_PATH/synergy_protocol_with_angio.py -o $SYNERGY_BIDS_PATH -d "{subject}/2*/*/*.DCM"'
alias syn_bids='bids-validator $SYNERGY_BIDS_PATH -c $SYNERGY_BIDS_CONFIG_FILE'

alias syn_clean_bids=${SYNERGY_SCRIPTS_PATH}/syn_clean_bids.sh

alias syn_fmriprep='$SYNERGY_SCRIPTS_PATH/syn_fmriprep.sh'
alias syn_mriqc='$SYNERGY_SCRIPTS_PATH/syn_mriqc.sh'
alias syn_mriqc_group='mriqc  $SYNERGY_BIDS_PATH $SYNERGY_MRIQC_PATH group'

alias syn_gi_netprep='$SYNERGY_SCRIPTS_PATH/syn_gi_netprep.sh'
alias syn_netprep='netprep.py syn_netprep.yaml'


alias cdsyn='cd $SYNERGY_PATH'
alias cdsynb='cd $SYNERGY_BIDS_PATH'
alias cdsynia='cd $SYNERGY_IMAGE_ANALYSIS_PATH'
alias cdsynip='cd $SYNERGY_IMAGE_PROCESS_PATH'
alias cdsynq='cd $SYNERGY_MRIQC_PATH'

alias cds='cd $SYNERGY_PATH; lsreport'
alias cdsb='cd $SYNERGY_BIDS_PATH; lsreport_function'
alias cdsq='cd $SYNERGY_MRIQC_PATH; lsreport_function'
alias cdsia='cd $SYNERGY_IMAGE_ANALYSIS_PATH; lsreport_function'
alias cdsip='cd $SYNERGY_IMAGE_PROCESSING_PATH; lsreport_function'
alias cdsin='cd $SYNERGY_PATH/incoming; lsreport_function;'
alias cdss='cd $SYNERGY_SCRIPTS_PATH; lsreport_function'

alias resyn='source $SYNERGY_SCRIPTS_PATH/synergy_aliases.sh'

alias activate_synergy='source $SYNERGY_SCRIPTS_PATH/synergy_set_to_active_study.sh'

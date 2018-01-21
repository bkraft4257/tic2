#!/usr/bin/env bash

# Aliases
alias rehfpef='source $HFPEF_SCRIPTS_PATH/hfpef_aliases.sh'
alias hfpef_help='firefox https://github.com/theimagingcollective/nipype_workflows/wiki/HFPEF-Image-Processing &'

alias hfpef_bids='bids-validator $HFPEF_BIDS_PATH -c $HFPEF_BIDS_CONFIG_FILE'
alias hfpef_bids_validitor='bids-validator $HFPEF_BIDS_PATH -c $HFPEF_BIDS_CONFIG_FILE'
alias hfpef_bv='bids-validator $HFPEF_BIDS_PATH -c $HFPEF_BIDS_CONFIG_FILE'

alias hfpef_hdc='/cenc/software/heudiconv/python/heudiconv/bin/heudiconv -c dcm2niix -b --minmeta -f /gandg/hfpef/scripts/hfpef_protocol_v2.py -o /gandg/hfpef/bids/ -d "{subject}/2*/*/*.DCM"'

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

#alias cdh='cd $HFPEF_PATH; lsreport_function'
#alias cdhb='cd $HFPEF_BIDS_PATH; lsreport_function'
#alias cdhin='cd $HFPEF_PATH/incoming; lsreport_function'
#alias cdhia='cd $HFPEF_IMAGE_ANALYSIS_PATH; lsreport_function'
#alias cdhip='cd $HFPEF_IMAGE_PROCESSING_PATH; lsreport_function'
#alias cdhipl='cd $HFPEF_IMAGE_PROCESSING_PATH/fmriprep_logs; lsreport_function'
#alias cdhqc='cd $HFPEF_MRIQC_PATH; lsreport_function'
#alias cdhs='cd $HFPEF_SCRIPTS_PATH; lsreport_function'

alias as_hfpef='echo previous active_study : $ACTIVE_STUDY; source $HFPEF_SCRIPTS_PATH/hfpef_set_to_active_study.sh; echo current active_study  : $ACTIVE_STUDY;'

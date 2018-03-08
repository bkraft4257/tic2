#!/usr/bin/env bash

# Aliases
alias rehfpef='source $HFPEF_SCRIPTS_PATH/aliases.sh'
alias hfpef_help='firefox https://github.com/theimagingcollective/nipype_workflows/wiki/HFPEF-Image-Processing &'

alias hfpef_clean_bids='$HFPEF_SCRIPTS_PATH/hfpef_bids_clean.sh'
alias hfpef_bids_clean='$HFPEF_SCRIPTS_PATH/hfpef_bids_clean.sh'

# The JSON file written after the upgrade is different than before the upgrade.
# AcquisitionMatrixPE: 64 is no longer in the file and has been replaced with
# AcquisitionNumber: 1.  I then modified the hfpef_clean_bids.sh file to accommodate this change. It is a quick and ugly
# hack.

alias hfpef_clean_bids_2b='$HFPEF_SCRIPTS_PATH/hfpef_clean_bids_2b.sh'
alias hfpef_bids_clean_2b='$HFPEF_SCRIPTS_PATH/hfpef_clean_bids_2b.sh'

alias hfpef_gi_netprep_epi='$HFPEF_SCRIPTS_PATH/hfpef_gi_netprep_epi.sh'
alias hfpef_gi_netprep_mbepi='$HFPEF_SCRIPTS_PATH/hfpef_gi_netprep_mbepi.sh'

alias hfpef_gi_netprep='$HFPEF_SCRIPTS_PATH/hfpef_gi_netprep.sh'
alias hfpef_netprep='/gandg/tic/nipype_workflows/netprep.py'

alias cdh='cd $HFPEF_PATH; lsreport_function'
alias cdhb='cd $HFPEF_BIDS_PATH; lsreport_function'
alias cdhin='cd $HFPEF_PATH/incoming; lsreport_function'
alias cdhia='cd $HFPEF_IMAGE_ANALYSIS_PATH; lsreport_function'
alias cdhip='cd $HFPEF_IMAGE_PROCESSING_PATH; lsreport_function'
alias cdhipl='cd $HFPEF_IMAGE_PROCESSING_PATH/fmriprep_logs; lsreport_function'
alias cdhqc='cd $HFPEF_MRIQC_PATH; lsreport_function'
alias cdhs='cd $HFPEF_SCRIPTS_PATH; lsreport_function'

alias as_hfpef='echo previous active_study : $ACTIVE_STUDY; source $HFPEF_SCRIPTS_PATH/hfpef_set_to_active_study.sh; echo current active_study  : $ACTIVE_STUDY'

#!/usr/bin/env bash

# Aliases

alias cdas='cd $ACTIVE_PATH; lsreport_function'
alias cdb='cd $ACTIVE_BIDS_PATH; lsreport_function'
alias cdin='cd $ACTIVE_PATH/incoming; lsreport_function'
alias cdia='cd $ACTIVE_IMAGE_ANALYSIS_PATH; lsreport_function'
alias cdip='cd $ACTIVE_IMAGE_PROCESSING_PATH; lsreport_function'
alias cdipl='cd $ACTIVE_IMAGE_PROCESSING_PATH/logs; lsreport_function'
alias cdqc='cd $ACTIVE_MRIQC_PATH; lsreport_function'
alias cdqcl='cd $ACTIVE_MRIQC_PATH/logs; lsreport_function'
alias cdass='cd $ACTIVE_SCRIPTS_PATH; lsreport_function'

alias asp='echo; echo $ACTIVE_PATH; echo'
alias asi='active_study_info.sh'

alias bv='tic_bids_validator.sh'

alias sw='study_switcher.sh'

# Common environment variables used for ACTIVE scripts and such.

export ACTIVE_HEUDICONV_PATTERN="{subject}/2*/*/*.DCM"



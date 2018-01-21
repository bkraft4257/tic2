#!/usr/bin/env bash

# Aliases

alias cds='cd $ACTIVE_STUDY_PATH; lsreport_function'
alias cdb='cd $ACTIVE_STUDY_BIDS_PATH; lsreport_function'
alias cdin='cd $ACTIVE_STUDY_PATH/incoming; lsreport_function'
alias cdia='cd $ACTIVE_STUDY_IMAGE_ANALYSIS_PATH; lsreport_function'
alias cdip='cd $ACTIVE_STUDY_IMAGE_PROCESSING_PATH; lsreport_function'
alias cdipl='cd $ACTIVE_STUDY_IMAGE_PROCESSING_PATH/fmriprep_logs; lsreport_function'
alias cdqc='cd $ACTIVE_STUDY_MRIQC_PATH; lsreport_function'
alias cdss='cd $ACTIVE_STUDY_SCRIPTS_PATH; lsreport_function'

alias as='echo; echo $ACTIVE_STUDY_PATH; echo'
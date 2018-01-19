#!/usr/bin/env bash

alias reinf='source $INFINITE_SCRIPTS_PATH/inf_aliases.sh'

alias inf_mriqc='mriqc $PWD /gandg/infinite/imaging_data/mriqc participant --participant_label '

alias inf_bids='/usr/local/bin/bids-validator $INFINITE_BIDS_PATH'
alias inf_bids_validator='/usr/local/bin/bids-validator $INFINITE_BIDS_PATH'
alias inf_bv='/usr/local/bin/bids-validator $INFINITE_BIDS_PATH'

alias inf_clean_bids='$INFINITE_SCRIPTS_PATH/inf_clean_bids.sh'
alias inf_display_bids='$INFINITE_SCRIPTS_PATH/inf_display_bids.sh'

alias inf_hdc='${INFINITE_SCRIPTS_PATH}/inf_hdc.sh'

alias inf_fmriprep='${INFINITE_SCRIPTS_PATH}/inf_fmriprep.sh'

alias inf_mriqc='${INFINITE_SCRIPTS_PATH}/inf_mriqc.sh'
alias inf_mriqc_group='mriqc  $INFINITE_BIDS_PATH $INFINITE_MRIQC_PATH group'

alias inf_netprep_gi='${INFINITE_SCRIPTS_PATH}/inf_netprep_gi.sh'

export INFINITE_FMRIPREP=$FMRIPREP_PATH/poldracklab_fmriprep_latest-2017-11-10-9ae650872d1e.img
export INFINITE_MRIQC=/cenc/software/mriqc/poldracklab_mriqc_latest-2017-08-30-f54388a6fb57.img
export INFINITE_HDC=/cenc/software/heudiconv/nipy_heudiconv-2017-09-26-6bef64b746f6.img

export INFINITE_PATH=/gandg/infinite/imaging_data/
export INFINITE_BIDS_PATH=${INFINITE_PATH}/bids
export INFINITE_IMAGE_PROCESSING_PATH=${INFINITE_PATH}/image_processing
export INFINITE_IMAGE_ANALYSIS_PATH=${INFINITE_PATH}/image_analysis
export INFINITE_SCRIPTS_PATH=${INFINITE_PATH}/scripts
export INFINITE_MRIQC_PATH=${INFINITE_PATH}/mriqc

export INFINITE_FMRIPREP_PATH=${INFINITE_IMAGE_PROCESSING_PATH}/fmriprep
export INFINITE_NETPREP_PATH=${INFINITE_IMAGE_PROCESSING_PATH}/netprep

alias cdib='cd $INFINITE_BIDS_PATH'
alias cdid='cd $INFINITE_PATH/individuals'
alias cdiia='cd $INFINITE_IMAGE_ANALYSIS_PATH'
alias cdiip='cd $INFINITE_IMAGE_PROCESSING_PATH'
alias cdiipl='cd $INFINITE_IMAGE_PROCESSING_PATH/fmriprep_logs'
alias cdiq='cd $INFINITE_MRIQC_PATH'
alias cdiqc='cd $INFINITE_MRIQC_PATH'
alias cdis='cd $INFINITE_SCRIPTS_PATH'


alias inf_get_id='_get_infinite_id'

function _get_infinite_id() {
    dir_name=${1-$PWD}
    echo $dir_name  | grep -o "inf0[1-2][0-9][0-9]"
}
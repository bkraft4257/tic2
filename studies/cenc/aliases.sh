#!/usr/bin/env bash

# Aliases
alias recenc='source $CENC_SCRIPTS_PATH/../aliases.sh'

# When creating this alias you will need to update the study_switcher.py to include the cenc
# name.
alias sw_cenc='study_switcher.py cenc -d ; source $DOT_TIC_PATH/tic_study_switcher.sh'

alias cfif='$CENC_SCRIPTS_PATH/cenc_fmap_intended_for.sh'

# these below are from /cenc/tic_beta/studies/cenc/other/unix/cenc_aliases.sh, which
#  Constance has in her environment.  I just picked some I thought were useful.
#  There are functions mixed in here, maybe create a separate functions.sh later.

alias cdcs='cd $CENC_SCRIPTS; echo; ls;  echo'
alias cenc_redcap='python3 ${TIC_REDCAP_LINK_PATH}/redcap_link/redcap_upload.py cenc'

function cdcd() {
  if [ $# -eq 1 ]; then
      subjectID=$(printf "sub-34P1%03d\n" $1)
      subjectDir=${CENC_BIDS_PATH}/${subjectID}/ses-1;

      if [ -d $subjectDir ]; then
	  # title ${subjectID}
	  A=1
      else
      subjectDir=$CENC_BIDS_PATH
      # title "CENC"
      fi

  else
      subjectDir=${CENC_BIDS_PATH};
      # title "CENC"
  fi

 cd $subjectDir
 echo; echo $PWD; echo; ls;  echo
}

function cenc_update_participant_list() {
    echo "Updating cenc_update_participant_list"

    ls -1d ${CENC_BIDS_PATH}/34P1[0-9][0-9][0-9] > ${CENC_BIDS_PATH}/participant.list
    grep -o "34P1[0-9][0-9][0-9]" ${CENC_BIDS_PATH}/participant.list | sort > ${CENC_BIDS_PATH}/acrostic.list

}


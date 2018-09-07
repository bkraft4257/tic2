#!/usr/bin/env bash

# Aliases

# When creating this alias you will need to update the study_switcher.py to include the cenc
# name.
alias sw_cenc='study_switcher.py cenc -d ; source $DOT_TIC_PATH/tic_study_switcher.sh'

alias cfif='$CENC_SCRIPTS_PATH/cenc_fmap_intended_for.sh'



#################

#!/usr/bin/env bash
## Python Aliases
#

#alias cenc_aseg_labels.sh

alias cenc_dcm_parse='${CENC_SCRIPTS_PATH}/cenc_dcm_parse.sh'

alias cenc_dcm_clean_draft='grep -v rs02 dcmConvert_cenc.cfg.draft | dcm_remove_rs |
                            sort -n | tee dcmConvert_cenc.cfg'

alias cenc_freesurfer='${CENC_PYTHON_PATH}/cenc_freesurfer.py'
alias cenc_id='${CENC_PYTHON_PATH}/cenc_id.py'
alias cenc_mt='${CENC_PYTHON_PATH}/cenc_mt.py'
alias cenc_mv_incoming='${CENC_SCRIPTS_PATH}/cenc_mv_incoming.sh'
alias cenc_mv_qc='${CENC_PYTHON_PATH}/cenc_mv_qc.sh'
alias cenc_swi='${CENC_PYTHON_PATH}/cenc_swi.py'
alias cenc_wmlesions='${CENC_PYTHON_PATH}/cenc_wmlesions.py'
alias cenc_fmri_gather='${CENC_PYTHON_PATH}/fmri_gather.py'

alias cenc_duke_register='${CENC_SCRIPTS_PATH}/cenc_duke_register.sh'

alias cenc_update_participants="cenc_update_participant_list"

alias cenc_lrt_participants='ls -1drt ${CENC_BIDS_PATH}/34P1[0-9][0-9][0-9]'
alias cenc_llrt_participants='ls -ldrt ${CENC_BIDS_PATH}/34P1[0-9][0-9][0-9]'

# Aliases
alias cenc_redcap='python3 ${TIC_REDCAP_LINK_PATH}/redcap_link/redcap_upload.py cenc'

alias cdcs='cd $CENC_SCRIPTS_PATH; echo; ls;  echo'
alias cdcm='cd $CENC_MATLAB_PATH;  echo; ls;  echo'

# alias cfs='echo; echo $SUBJECTS_DIR; SUBJECTS_DIR=$CENC_SUBJECTS_DIR; echo $SUBJECTS_DIR; echo'

## Functions
#


function cenc_update_participant_list() {
    echo "Updating cenc_update_participant_list"

    ls -1d ${CENC_BIDS_PATH}/34P1[0-9][0-9][0-9] > ${CENC_BIDS_PATH}/participant.list
    grep -o "34P1[0-9][0-9][0-9]" ${CENC_BIDS_PATH}/participant.list | sort > ${CENC_BIDS_PATH}/acrostic.list

}

function ctf_sed() {
    # I had trouble getting the conversion to lower case working properly

    in_file=$1
    cat $in_file | sed -r -e 's/[[:blank:]]+/,/g' -e '$s/$/\n/' | tr '[:upper:]' '[:lower:]' | tee junk.csv
    mv junk.csv $in_file

#    -e '1 s/X/x/' -e '1 s/Y/y/'   -e '1 s/Z/z/' \
#    -e '1 s/C/c/' -e '1 s/A/a/'   -e '1 s/S/s/' 
#    echo "sed -r -e 's/[[:blank:]]+/,/g' -e '$s/$/\\\n/' $1"

}


function cdc() { 
    cdcd $1
}

# function for title
function title {
   HOSTBN=`hostname -s`
   PROMPT_COMMAND="echo -ne \"\033]0;[$HOSTBN]:${PWD}\007\""
}


function cdcd() {
  if [ $# -eq 1 ]; then
      subjectID=$(printf "sub-34P1%03d\n" $1)
      subjectDir=${CENC_BIDS_PATH}/${subjectID}/ses-1;
      echo subjectDir: $subjectDir

      if [ -d $subjectDir ]; then
	  # title ${subjectID}
	  :
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

function cdcds() { 
  if [ $# -eq 1 ]; then
      subjectID=$(printf "34P1%03d\n" $1)
      subjectDir=${CENC_BIDS_PATH}/${subjectID}/;
      
      if [ -d $subjectDir ]; then
	  # title ${subjectID}
	  :
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




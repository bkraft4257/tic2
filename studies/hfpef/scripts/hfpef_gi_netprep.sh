#!/bin/bash

# hfpef_gi_netprep.sh gathers the inputs for running netprep.


if [[ $# -lt 1 ]]; then
   echo "Usage: hfpef_gi_netprep.sh <subject_value,hfs070> <session_value,1>"
   echo "You may only enter one subject value and session value at a time."

   exit 0
fi

subject_id=${1}
session_id=${2-1}
subject=sub-${subject_id}
session=ses-${session_id}


echo
echo "hfpef_gi_netprep_epi.sh =============================================================================="
echo

$HFPEF_SCRIPTS_PATH/hfpef_gi_netprep_epi.sh $subject_id  $session_id



echo
echo "hfpef_gi_netprep_mbepi.sh =============================================================================="
echo

$HFPEF_SCRIPTS_PATH/hfpef_gi_netprep_mbepi.sh $subject_id  $session_id






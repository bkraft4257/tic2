#!/usr/bin/env bash

# Aliases
alias rehfpef='source $HFPEF_SCRIPTS_PATH/aliases.sh'

#alias hfpef_bids_clean='$HFPEF_SCRIPTS_PATH/hfpef_bids_clean.sh'
alias hfpef_bids_clean='$HFPEF_SCRIPTS_PATH/hfpef_clean_bids_2b.sh'

# The JSON file written after the upgrade is different than before the upgrade.
# AcquisitionMatrixPE: 64 is no longer in the file and has been replaced with
# AcquisitionNumber: 1.  I then modified the hfpef_clean_bids.sh file to accommodate this change. It is a quick and ugly
# hack.


alias hfpef_gi_netprep='$HFPEF_SCRIPTS_PATH/hfpef_gi_netprep.sh'
alias hfpef_conn='$HFPEF_SCRIPTS_PATH/hfpef_conn_setup.sh'

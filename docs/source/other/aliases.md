# Aliases

Aliases are simple commands that are defined to help move among the various directories
of the study.  They also provide a way to perform simple commands. An alias, unlike a
script, does not have a .sh or .py extension. Aliases for each study are defined in the
studies tic folder ($TIC_PATH/studies/<study>). Aliases that are common among all the
studies are defined in $TIC_PATH/init.

    tic_help - Launches the TIC Sphinx documentation.
    tic_stat - Displays information about the current TIC session (tic_path, active_study, and subjects_dir)

    clean_bids  - Cleans a single subject and sessions bids directory.
    
    cdas - change directory to active study main directory  
    cdb  - change directory to  BIDS directory  
    cdip - change directory to image processing directory (fmriprep, netprep, etc.)  
    cdin - change directory to DICOM incoming directory  
    cdqc - change directory to QC directory

These aliases allow you to quickly move between studies.

    swh - Set Hfpef as the active study  
    swi - Set Infinite as the active study  
    swm - Set iMove as the active study
    sws - Set Synergy as the active study


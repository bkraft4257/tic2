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


# Scripts

**hdc_singularity.sh**   - Converts DICOM to NIFTI and places them in the BIDS data directory.  
**fmriprep.sh**          - Runs fmriprep on a single subject.  
**mriqc.sh**             - Runs MRI Quality Control on a single subject.  
**mriqc_group.sh**       - Runs MRI Quality Control as a group on subjects in MRIQC directory.



# Quick Instructions

These quick instructions are intended to serve as a reminder on how to process a data set.  Each
step assumes that the previos steps have been completed and are correct. The commands are written
to be as general as possible by using the commonly used notation <variable>, where <variable> indicates
parameter that you are supposed to enter. I have expanded upon this convention by adding an example
for each field.  For example to convert your DICOM images to NIFTI in the BIDS data structure you run the
command

    >> hdc_singularity.sh -s <bids_subject_value, hfs070> -ss < bids_session_value, 1 >

The >> indicates the command prompt on the command line. It is not included in the command.  Each < > represents a variable.
It contains two parts: a short description and then an example.  At the command line, you would just type the command

    >> hdc_singularity.sh -s hfs070 -ss 1

to convert subject hfs070 session 1 and add it to the active study.


### Convert DICOM images to NIFTI

1. cdin
1. mv <dicom_dicom_dir, **hf_s070_hf_s070** > < bids_subject_value, **hfs070** >
1. **hdc_singularity** -s <bids_subject_value, **hfs070** > -ss < bids_session_value, **1** >

### Clean BIDS directory

1. cdb
2. **clean_bids** <subject_value,hfs070> <session_value,1>

### Check if BIDS directory is still valid

1. bv


### MRI Quality Control

1. mriqc.sh < subject_value, **hfs070** >

### fmriprep

1. fmriprep.sh < subject_value, **hfs070** >


# Aliases & Scripts

Aliases are simple commands that are defined to help move among the various directories
of the study.  They also provide a way to perform simple commands. An alias, unlike a
script, does not have a .sh or .py extension. Aliases for each study are defined in the
studies tic folder ($TIC_PATH/studies/<study>). Aliases that are common among all the
studies are defined in $TIC_PATH/init.

    tic_help - Launches the TIC Sphinx documentation.
    tic_info - Displays information about the current TIC session (tic_path, active_study, and subjects_dir)

    asi - Displays information about the current active study.  This is a long list and most users
    may find this to be information overload.
    
    cdas - change directory to active study main directory  
    cdb  - change directory to  BIDS directory  
    cdip - change directory to image processing directory (fmriprep, netprep, etc.)  
    cdin - change directory to DICOM incoming directory  
    cdqc - change directory to QC directory

These aliases allow you to quickly switch between studies by changing the active study.  All aliases
and scripts are the same across all studies.

    swh   - Set Hfpef as the active study  
    swi   - Set Infinite as the active study  
    swm   - Set iMove as the active study
    sws   - Set Synergy as the active study
    swc   - Set CENC as the active study
    swmcf - Set MCF as the active study (I ran out of single letter designations that made sense.


# Scripts

**hdc.sh**   - Converts DICOM to NIFTI and places them in the BIDS data directory.  
**clean_bids.sh**       - Runs MRI Quality Control as a group on subjects in MRIQC directory.

**fmriprep.sh**          - Runs fmriprep on a single subject.  
**mriqc.sh**             - Runs MRI Quality Control on a single subject.  

The scripts have been written to minimize the amount of stuff you have to remember for each study
while allowing you flexibility to call scripts with various options. For example, the fmriprep.sh
script sets several environment variables and then calls the command

nohup time /usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 \
                 $APP_SINGULARITY_IMAGE \
                 $ACTIVE_BIDS_PATH \
                 $ACTIVE_APP_OUTPUT_PATH \
                 --work-dir $ACTIVE_APP_WORKING_PATH \
                 participant ${@} > $log_file 2>&1 &

The ${@} is the bash syntax to pass all of the variables from the command line and insert them
for ${@}.  If you call fmriprep -h you can see the help for fmriprep with all of its optional
parameters. For example if you want to run fmriprep with only anatomical processing you can run
the script

fmriprep.sh --participant-label imove1061 --anat-only


We are hoping this structure will allow simplicity for new users with flexibilty for experieneced
users.


# Quick Instructions

These quick instructions are intended to serve as a reminder on how to process a data set.  Each
step assumes that the previos steps have been completed and are correct. The commands are written
to be as general as possible by using the commonly used notation <variable>, where <variable> indicates
parameter that you are supposed to enter. I have expanded upon this convention by adding an example
for each field.  For example to convert your DICOM images to NIFTI in the BIDS data structure you run the
command

    >> hdc.sh -s <bids_subject_value, hfs070> -ss < bids_session_value, 1 >

The >> indicates the command prompt on the command line. It is not included in the command.  Each < > represents a variable.
It contains two parts: a short description and then an example.  At the command line, you would just type the command

    >> hdc.sh -s hfs070 -ss 1

to convert subject hfs070 session 1 and add it to the active study.


### Convert DICOM images to NIFTI

1. **cdin**
2. **mv** <dicom_dicom_dir, **hf_s070_hf_s070** > < bids_subject_value, **hfs070** >
3. **hdc.sh** -s <bids_subject_value, **hfs070** > -ss < bids_session_value, **1** >

**Note:** hdc uses -s as the optional parameter to specify the subject_value. fmriprep and mriqc uses
the optional parameter --participant-label to specify the subject_value.  This inconsistency
is a result of the BIDS Apps coming from multiple groups.

### Clean BIDS directory

1. **cdb**
2. **clean_bids.sh** <subject_value, **hfs070 **> <session_value, **1** >

### Check if BIDS directory is still valid

1. **bv**

### MRI Quality Control

1. **mriqc.sh --participant-label** < subject_value, **hfs070** >


### fmriprep

1. **fmriprep.sh --participant-label** < subject_value, **hfs070** >









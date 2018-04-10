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

1. **cdin**
1. **mv** <dicom_dicom_dir, **hf_s070_hf_s070** > < bids_subject_value, **hfs070** >
1. **hdc.sh** -s <bids_subject_value, **hfs070** > -ss < bids_session_value, **1** >

### Clean BIDS directory

1. **cdb**
2. **clean_bids.sh** <subject_value, **hfs070 **> <session_value, **1** >

### Check if BIDS directory is still valid

1. **bv**

### MRI Quality Control

1. **mriqc.sh --participant-label** < subject_value, **hfs070** >


### fmriprep

1. **fmriprep.sh --participant-label** < subject_value, **hfs070** >









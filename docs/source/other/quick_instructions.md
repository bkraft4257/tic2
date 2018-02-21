# Aliases

**tic_help** - Launches the TIC Sphinx help documentation.

**clean_bids**  - Cleans a single subject and sessions bids directory.  
**fmriprep.sh**    - Runs fmriprep on a single subject.  
**hdc_singularity.sh** - Converts DICOM to NIFTI and places them in the BIDS data directory.  
**mriqc.sh**       - Runs MRI Quality Control on a single subject.  
**mriqc_group.sh** - Runs MRI Quality Control as a group on subjects in MRIQC directory.

**netprep**      - In testing phase.
**prepare_netprep** - In testing phase.

**cdas** - goto active study main directory  
**cdb**  - goto BIDS directory  
**cdip** - goto image processing directory (fmriprep, netprep, etc.)  
**cdin** - goto DICOM incoming directory  
**cdqc** - goto QC directory

# Quick Instructions

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


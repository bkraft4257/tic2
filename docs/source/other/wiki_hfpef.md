# Aliases

**hfpef_help** - Goes to this help page from a Unix terminal

**hfpef_clean_bids**  - Cleans a single subject and sessions bids directory.  
**hfpef_fmriprep**    - Runs fmriprep on a single subject.  
**hfpef_hdc**         - Converts DICOM to NIFTI and places them in the BIDS data directory.  
**hfpef_mriqc**       - Runs MRI Quality Control on a single subject.  
**hfpef_mriqc_group** - Runs MRI Quality Control as a group on subjects in MRIQC directory.  
**hfpef_netprep**      - In testing phase.  
**hfpef_prepare_netprep** - In testing phase.

**cdh**   - goto HFPEF main study directory  
**cdhb**  - goto HFPEF BIDS directory  
**cdhia** - goto HFPEF image processing directory (fmriprep, netprep, etc.)  
**cdhin** - goto HFPEF DICOM incoming directory  
**cdhip** - goto HFPEF image analysis directory  
**cdhqc** - goto HFPEF MRIQC directory

# Quick Instructions

## Convert DICOM images to NIFTI

1. cdhin
1. mv <dicom_dicom_dir,hf_s070_hf_s070> <bids_subject_value,hfs070>
1. **hfpef_hdc** -s <bids_subject_value,hfs070> -ss <bids_session_value,1>

## Clean BIDS directory (stop and wait)

1. cdhb
1. chmod +w -R <subject_value,hfs070>
1. **hfpef_clean_bids** <subject_value,hfs070> <session_value,1>

## MRI Quality Control

1. hfpef_mriqc <subject_value,hfs070>

## fmriprep

1. hfpef_fmriprep <subject_value,hfs070>


# Complete Instructions with Tedious Details

## Convert DICOM images to NIFTI

## Clean BIDS directory  (hfpef_clean_bids)

    Cleaning the BIDS directory does the following 
    1. Renames files with the .1. count number appended to each file.  This number indicates the number of files that matched the HFPEF DICOM to NIFTI protocol.   Ideally, this number should always be 1.  If a scan is repeated you will see higher numbers.  It is nearly impossible to write a program to decide which scan should be used. In cases where there are repeat scans someone will have to look at the images and make the call. 
    1. Adds Echo1 and Echo2 to the JSON file of all field maps. 
    1. Removes JSON files associated with magnitude1 field maps.  These JSON files are not needed.
    1. Links the field maps to the functional and DWI data sets by adding the IntendedFor field to the JSON files. 
    1. Reorients all GZ images with fslreorient2std.  (Yes this is still necessary).
    1. Performs a final search for repeat scans. If no repeat scans are found no further action should be needed. 


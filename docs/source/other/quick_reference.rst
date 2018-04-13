Quick Reference
===============

These quick instructions are intended to serve as a reminder on how to process a data set.  Each
step assumes that the previous steps have been completed and are correct. The commands are written
to be as general as possible by using the commonly used notation <variable>, where <variable> indicates
parameter that you are supposed to enter. I have expanded upon this convention by adding an example
for each field.  For example to convert your DICOM images to NIFTI in the BIDS data structure you run the
command

    >> hdc.sh -s <bids_subject_value, hfs070> -ss < bids_session_value, 1 >

The >> indicates the command prompt on the command line. It is not included in the command.  Each < > represents a variable.
It contains two parts: a short description and then an example.  At the command line, you would just type the command as

    >> hdc.sh -s hfs070 -ss 1

to convert subject hfs070 session 1 and add it to the active study.


Convert DICOM images to NIFTI
-----------------------------
After you have downloaded the DICOM images from the PACS you go to the ACTIVE_STUDY incoming directory.

    .. code-block:: console

        >> cdin
        >> mv <dicom_dicom_dir, hf_s070_hf_s070 > < bids_subject_value, hfs070 >
        >> hdc.sh -s <bids_subject_value, hfs070 > -ss < bids_session_value, 1 >
        >> hdc_look.py -s <bids_subject_value, hfs070 > -ss < bids_session_value, 1 >


hdc.sh calls the heudiconv singularity image.
hdc_look.py is not absolutely necessary but it allows you to view what has been converted by heudiconv.
You may edit heudiconv's sub-<subject_value>_ses-<session_value>.edit.txt to correct any mistakes.

**Note:** hdc uses -s as the optional parameter to specify the subject_value. fmriprep and mriqc uses
the optional parameter --participant-label to specify the subject_value.  This inconsistency
is a result of the BIDS Apps being created by different groups.

Clean BIDS directory
--------------------
Once the DICOM images have been converted the BIDS directory needs to be cleaned.  The cleaning process
is specific to each study.  However, cleaning primarily does three things:

a. Remove .1. from all filenames  
b. FSL ROI topup files so the PA/AP or RL/LR have the same number of volumes.  
c. Sets the IntendedFor field in the fmap json files to to apply the TOPUP/Field Map to the EPI data.  
d. Reorients the images to standard FSL orientation with fslreorient2std.  

The cleaning process is done for all studies with 

    .. code-block:: console

        >> cdb
        >> clean_bids.sh <subject_value, hfs070> <session_value, 1 >


At the end of the cleaning processing the clean_bids.sh script will search for any files containing
*.[2-9].*.  If these files are found then you will need to make a decision of which files to keep.
Once you have decided which files to keep just rename them to remove ".[2-9]".  I usually do this
with the rename command.

    .. code-block:: console

        >> rename .2. . *



Check if BIDS directory is still valid
--------------------------------------
For an ongoing study this is complicated. Here is the bids-validator help


Usage: bids-validator <dataset_directory> [options]

Options:
  --help, -h            Show help                                      [boolean]
  --version, -v         Show version number                            [boolean]
  --ignoreWarnings      disregard non-critical issues                  [boolean]
  --ignoreNiftiHeaders  disregard NIfTI header content during validation
                                                                       [boolean]
  --verbose             Log more extensive information about issues.   [boolean]
  --config, -c          Optional configuration file. See
                        https://github.com/INCF/bids-validator for more info.

This tool checks if a dataset in a given directory is compatible with the Brain
Imaging Data Structure specification. To learn more about Brain Imaging Data
Structure visit http://bids.neuroimaging.io

The bids-validator behaviour can be modified through the files .bidsignore and the configuration
file .bids.cfg.  Both files affect the validation in a similar fashion. .bidsignore was implemented after
--config optional parameter.  

When you validate a BIDS directory with bv the contents of .bidsignore and .bids.cfg will be displayed  
so you can easily see what is being validated.  These files may need to be changed to accommodate the
state of the study or the BIDS App being applied. 

Other files that may need to be modified according to the situation is participants.tsv. 

The bv script will also refresh the acrostic.list and acrostic.csv files every time it is called. 

    .. code-block:: console

        >> bv

MRI Quality Control
-------------------
mriqc.sh is a script that simplifies calling the mriqc singularity image. You can see all of the options 
of the mriqc singularity image with the command "mriqc -h"

    .. code-block:: console

        >> mriqc.sh --participant-label < subject_value, hfs070 >



**REMEMBER**: Just because you ran the script doesn't mean it completed. YOU HAVE TO LOOK.



Preprocessing Anatomical and Functional Images
----------------------------------------------
fmriprep.sh is a script that simplifies calling the fmriprep singularity image. You can see all of the options 
of the fmriprep singularity image with the command "fmriprep -h"

fmriprep has three primary functions.

1. Runs FreeSurfer on your anatomical images.
1. Performs distortion correction to the functional data.
1. Normalizes the anatomical and functional images to the same space.
1. Measures but does not apply the temporal components in the gray matter, CSF, and white matter.

    .. code-block:: console
        
        >> fmriprep.sh --force-syn --participant-label < subject_value, hfs070 >


**REMEMBER**: Just because you ran the script doesn't mean it completed. YOU HAVE TO LOOK.



### Checking what has been processed








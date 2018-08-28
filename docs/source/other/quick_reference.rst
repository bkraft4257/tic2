Quick Reference
===============

These quick instructions are intended to serve as a reminder on how to process a data set.  Each
step assumes that the previous steps have been completed and are correct. The commands are written
to be as general as possible by using the commonly used notation <variable>, where <variable> indicates
parameter that you are supposed to enter. I have expanded upon this convention by adding an example
for each field.  For example to convert your DICOM images to NIFTI in the BIDS data structure you run the
command

    >> hdc.sh -s <bids_subject_value, hfs070> -ss < bids_session_value, 1 >

The >> indicates the command prompt on the command line. You do not type >> as part of the command.  Each set of < >
represents a variable. It contains two parts: a short description and then an example.  At the command line, you would
just type the command as

    >> hdc.sh -s hfs070 -ss 1

to convert subject hfs070 session 1 and add it to the active study.  If you are new to Unix the > and < are also used to
redirect output. The only time < and > are used to represent a variable is when they are used together with a variable name
in between them.  You should be able to determine how <> are used by their context.


Select the Study to be ACTIVE
-----------------------------

Each study is setup to be processed with similar if not identical processing steps. This is accomplished with the concept
of an ACTIVE STUDY.  If your account is setup correctly for TIC you should see the following when you log into a terminal
on the computer for processing.

.. code-block:: console

    >> ssh -YC  bkraft@aging1a

           Last login: Wed Jul 18 09:26:45 2018 from flip.medctr.ad.wfubmc.edu

           -------- freesurfer-Linux-centos6_x86_64-stable-pub-v5.3.0 --------
           Setting up environment for FreeSurfer/FS-FAST (and FSL)
           FREESURFER_HOME   /aging1/software//freesurfer
           FSFAST_HOME       /aging1/software//freesurfer/fsfast
           FSF_OUTPUT_FORMAT nii.gz
           SUBJECTS_DIR      /aging1/software//freesurfer/subjects
           MNI_DIR           /aging1/software//freesurfer/mni
           FSL_DIR           /aging1/software//fsl5.09


           TIC_PATH     : /gandg/bkraft/tic/tic_core

           FMRIPREP_SINGULARITY_IMAGE =  /aging1/software/fmriprep//poldracklab_fmriprep_latest-2017-11-10-9ae650872d1e.img
           MRIQC_SINGULARITY_IMAGE    =  /aging1/software//mriqc/poldracklab_mriqc_latest-2017-08-30-f54388a6fb57.img
           HDC_SINGULARITY_IMAGE      =  /aging1/software//heudiconv/nipy_heudiconv-2018-03-02-bf4d6e1d4d0e.img
           TRACULA_SINGULARITY_IMAGE  =  /aging1/software//bids_apps/bids_tracula_latest-2017-08-11-efd6196f92ca.img

           ANTS_CORTICAL_THICKNESS_SINGULARITY_IMAGE =  /aging1/software//bids_apps/bids_antscorticalthickness-2017-10-14-95aa110c26f8.img


           SUBJECTS_DIR : /gandg/hfpef/image_processing/freesurfer
           ACTIVE_STUDY : HFPEF


The above is displayed in my terminal when I login to the aging1a as bkraft.  The last line tells you my current ACTIVE
STUDY.  After logging in you can find information about the current ACTIVE STUDY by running the alias **asi**.  The
alias asi runs the bash script active_study_info.sh.

.. code-block:: console

    >> asi

         HFPEF

         ACTIVE_ACROSTIC_REGEX              =  hf[u|s][0-9]{3}

         ACTIVE_SCRIPTS_PATH                =  /gandg/bkraft/tic/tic_core/studies/hfpef/scripts
         ACTIVE_PATH                        =  /gandg/hfpef
         ACTIVE_BIDS_PATH                   =  /gandg/hfpef/bids
         ACTIVE_HEUDICONV_PROTOCOL          =  /gandg/bkraft/tic/tic_core/studies/hfpef/scripts/hfpef_protocol.py

         ACTIVE_CLEAN_BIDS                  =  /gandg/bkraft/tic/tic_core/studies/hfpef/scripts/hfpef_clean_bids.sh
         ACTIVE_SINGULARITY_USER_BIND_PATHS =  /gandg

         ACTIVE_IMAGE_ANALYSIS_PATH         =  /gandg/hfpef/image_analysis
         ACTIVE_IMAGE_PROCESSING_PATH       =  /gandg/hfpef/image_processing
         ACTIVE_IMAGE_PROCESSING_LOG_PATH   =  /gandg/hfpef/image_processing/logs

         ACTIVE_MRIQC_PATH                  =  /gandg/hfpef/qc/mriqc

         ACTIVE_ACT_PATH                    =  /gandg/hfpef/image_processing/act
         ACTIVE_FMRIPREP_PATH               =  /gandg/hfpef/image_processing/fmriprep
         ACTIVE_NETPREP_PATH                =  /gandg/hfpef/image_processing/netprep

         SUBJECTS_DIR                       =  /gandg/hfpef/image_processing/freesurfer
         ACTIVE_SUBJECTS_DIR                =  /gandg/hfpef/image_processing/freesurfer


Switching between studies is easy.  The bash function for switching between studies is sw.  This calls the python script
called study_switcher.py. You can switch to a different study calling sw and the study name.  For example to switch to the
Mindfulness Functional Connectivity study (mfc) you issue the command


.. code-block:: console

    >> sw mfc

        ACTIVE_STUDY is now MFC


The study_switcher.py can also be used to set your default study.

.. code-block:: console

    >> sw mfc -d


Will set the Mindfulness Functional Connectivity study as the default study.  The next time you login to process data
your ACTIVE STUDY will be MFC.  This is accomplished by writing a bash script to your $HOME/.tic/tic_default_study.sh.
This bash script is called everytime you login.


Convert DICOM images to NIFTI
-----------------------------
After you have downloaded the DICOM images from the PACS you go to the ACTIVE_STUDY incoming directory.

    .. code-block:: console

        >> cdin
        >> mv <dicom_dicom_dir, hf_s070_hf_s070 > < bids_subject_value, hfs070 >
        >> hdc.sh -s <bids_subject_value, hfs070 > -ss < bids_session_value, 1 >
        >> hdc_look.py -s <bids_subject_value, hfs070 > -ss < bids_session_value, 1 >


hdc.sh calls the heudiconv singularity image.  In order to call hdc.sh for each study the study must have an HDC protocol
created. This protocol is stored in the environment variable $ACTIVE_HEUDICONV_PROTOCOL.   The HDC protocol is a python
function that is created by the end users and tells heudiconv how to interpret, sort, and rename DICOM files. The protocol
files are relatively easy to create and is best done using another protocol file as an example.

hdc_look.py is not absolutely necessary but it allows you to view what has been converted by heudiconv.
You may edit heudiconv's sub-<subject_value>_ses-<session_value>.edit.txt to correct any mistakes.

**Note:** hdc uses -s as the optional parameter to specify the subject_value. fmriprep and mriqc uses
the optional parameter --participant-label to specify the subject_value.  This inconsistency
is a result of the BIDS Apps being created by different groups. It is even move confusing because the BIDS APP
antsCorticalThickness uses --participant_label to specify the subject_value (notice the use of underscore instead of dash).

TIC uses bash shell script wrapper functions to call the BIDS apps.  This allows one to have the majority of parameters
set necessary to call the SINGULARITY or DOCKER images correctly. The wrapper functions have been updated to accept the
parameter flag -s and replace it with --participant_label or --participant-label as required by the BID APP. This allows
TIC to keep things as simple as possible.  Of course, this also obfuscate what is happening behind the scenes. You can
always look at the code for each bash shell script wrapper in the $TIC_PATH/bin directory.


Clean BIDS directory
--------------------
Once the DICOM images have been converted the BIDS directory needs to be cleaned.  The cleaning process
is specific to each study.  However, cleaning primarily does two things:

1. Remove .1. from all filenames.
1. Sets the IntendedFor field in the fmap json files to to apply the TOPUP/Field Map to the EPI data.

For DTI studies cleaning may also include

1. truncating DTI B0 image for the TOPUP AP/RL and PA/LR scans to have the same number of volumes.

In earlier studies bash scripts were written to do this cleaning process. While these bash scripts worked well they
were not easily extended.  For this reason, BIDS cleaning has been rewritten to generic functions clean_bids.py and
fmap_intended_for.py.  These two scripts allow one to clean the BIDS directory for fmriprep.


The cleaning process is done for all studies with

    .. code-block:: console

        >> cdb
        >> clean_bids.py <subject_value, hfs070> <session_value, 1 >


You can obtain more help about the clean_bids.py by requesting help with the -h parameter.

    .. code-block:: console

    >> bids clean_bids.py -h

        usage: clean_bids [-h] [-s [SUBJECT [SUBJECT ...]]]
                          [-ss [SESSION [SESSION ...]]] [-v] [-l | -u]

        optional arguments:
          -h, --help            show this help message and exit
          -s [SUBJECT [SUBJECT ...]], --subject [SUBJECT [SUBJECT ...]]
                                BIDS subject value
          -ss [SESSION [SESSION ...]], --session [SESSION [SESSION ...]]
                                BIDS session value
          -v, --verbose         Turn on verbose mode.
          -l, --lock            Disable write permission to *.nii.gz and *.json files
          -u, --unlock          Enable write permission to *.nii.gz and *.json files


At the end of the cleaning processing the clean_bids.sh script will search for any files containing
*.[2-9].*.  If these files are found then you will need to make a decision of which files to keep.
Once you have decided which files to keep just rename them to remove ".[2-9]".  I usually do this
with the rename command.

    .. code-block:: console

        >> rename .2. . *


If you are using TOPUP for your fmriprep processing you will need to have the TOPUP AP/PA or RL/LR nii.gz contain the
same number of volumes.  The easiest way to do this is to acquire these calibration files with the same number of volumes.
However, sometimes for DTI data people prefer to acquire the DTI data with R/L and then acquire a L/R calibration data
set to save time.  You can do this but you will need to extract the b0 volumes from the larger data set to match the
number of volumes in the calibration data set.  I do this fslroi.  This command is easy to use and is quick.


The final thing that needs to be done to clean the BIDS directory if you are going to use field maps or TOPUP distortion
correction is to set the following flags in the fmap and topup JSON files.




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



Checking what has been processed
--------------------------------

    .. code-block:: console

        >> bps -h

        usage: processing_status [-h] [-s SUBJECT] [-ss SESSION] [-a ACROSTIC_LIST]
                                 [--display_max_rows DISPLAY_MAX_ROWS]
                                 [--glob_current_directory_only] [-v] [-H]
                                 [--subject_only] [--summary]
                                 [--nan {drop,only,ignore}]
                                 [--display_group {found,missing,both}]
                                 file_pattern

        positional arguments:
          file_pattern          String file pattern to glob

        optional arguments:
          -h, --help            show this help message and exit
          -s SUBJECT, --subject SUBJECT
                                Regular expression subject acrostic
          -ss SESSION, --session SESSION
                                Regular expression session
          -a ACROSTIC_LIST, --acrostic_list ACROSTIC_LIST
                                Acrostic List
          --display_max_rows DISPLAY_MAX_ROWS
                                Display a maximum number of rows
          --glob_current_directory_only
                                Recursive boolean flag for glob
          -v, --verbose         Turn on verbose mode.
          -H, --noheader        Remove header from output
          --subject_only        Only display subject
          --summary             Display summary stats
          --nan {drop,only,ignore}
                                Remove NaNs from output
          --display_group {found,missing,both}
                                Display files that were found, missing, or both.
                                Default is both.

    .. code-block:: console

        >> bps_fmriprep_bold


    .. code-block:: console

        >> bps_fmriprep_t1w






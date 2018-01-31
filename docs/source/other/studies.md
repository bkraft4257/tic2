# Studies

Investigators are encouraged to share scripts that they used to process
their individual studies. These scripts are stored in the folder

$TIC_PATH/studies under the invidual studies name. For example, in the
list below there are four studies listed

$TIC_PATH/studies

    /active   
    /infinite
    /hfpef
    /synergy

Dr. Christina Hugenschmidt is the PI for the studies infinite, hfpef,
and synergy. **active** is a generic study that contains many of the
common programs that are shared among the various studies. For example,
most neuroimaging studies that acquire functional data will want to
process their data through fmriprep. We have created a bash script
called fmriprep.sh to process the **active** study.

If you want to process a different study you have to set the study you
want to process as the active study. This is similar to how FreeSurfer
works with their SUBJECTS_DIR. You can process any study you want with
FreeSurfer. However, you need to set the environment variable of the
SUBJECTS_DIR to associate the data with the proper study.

TIC takes a similar approach. You can see all of the environment
variables associated with the ACTIVE_STUDY with the following command

     >>> env | grep -i ACTIVE

          ACTIVE_STUDY=HFPEF
          ACTIVE_SCRIPTS_PATH=/gandg/bkraft/tic//studies/hfpef/scripts
          ACTIVE_PATH=/gandg/hfpef/
          ACTIVE_BIDS_PATH=/gandg/hfpef//bids
          ACTIVE_IMAGE_ANALYSIS_PATH=/gandg/hfpef//image_analysis
          ACTIVE_IMAGE_PROCESSING_PATH=/gandg/hfpef//image_processing
          ACTIVE_IMAGE_PROCESSING_LOG_PATH=/gandg/hfpef//image_processing/logs
          ACTIVE_MRIQC_PATH=/gandg/hfpef//mriqc
          ACTIVE_FMRIPREP_PATH=/gandg/hfpef//image_processing/fmriprep
          ACTIVE_NETPREP_PATH=/gandg/hfpef//image_processing/netprep
          ACTIVE_BIDS_CONFIG_FILE=/gandg/bkraft/tic//studies/hfpef/scripts/hfpef_bids.cfg

You can see from the first listed environment variable $ACTIVE_STUDY
that the active study is HFPEF. We can process the hfpef subject hfs073
with the fmriprep with the command

     fmriprep.sh --participant_label hfs073

You can switch to another study with the command study_switcher.py by
doing the following

     >>> study_switcher.py -s synergy
     >>> source $TIC_INIT_PATH/tic_study_switcher.sh
     >>> echo $ACTIVE_STUDY

        SYNERGY

The need to run two separate commands to make another study active is
because it is difficult (if not impossible) to set the environment
variable of the parent process. To circumvent this problem,
study_switcher.py writes a text file to set the environment variables
and then we source this file. Since it is tiresome to type these
commands we have created aliases to switch between different studies.

``` code
>>> swh   
Previous active study = SYNERGY  
Current active study = HFPEF
   
>>> swi   
   Previous active study = HFPEF 
   Current active study = INFINITE
   
>>> sws 
   Previous active study = INFINITE   
   Current active study = SYNERGY  
```

Our goal is to write all scripts and functions to operate on the Active
Study and then allow the user switch between studies. We are hoping that
this will facilitate code reuse, decreased documentation, and will be
easier on our users because they only have to remember one command to
run fmriprep across all studies.

## Study Directory Structure

Finding data is always a challenge in large studies. It helps to have a
systematic way for data to be stored with a common naming convention.
The data structure presented here is intended to be a guideline as
opposed to a set of stringent rules. Individual investigators and
studies will have their own needs and need to have the flexibility to do
what is best for them. Regardless of the final data structure chosen for
each study this page will serve as a set of guidelines.

    study_name/
        bids/ (BIDS' directory structure consisting of NIFTI and JSON files)
            .heudiconv/  (hidden directory containing information about DICOM to NIFTI conversion)
                x01/
                   ses-1/
                        info/  (contains information about DICOM to NIFTI conversion)
                              **dicominfo_ses-1.tsv**  (DICOM fields to be used to select DICOM files to NIFTI conversion)
                              **x01_ses-1.auto.txt**   (text file showing which files will be converted and how)
                              **x01_ses-1.edit.txt**   (text file that user can edit to override auto setttings)

                   ...
                   ses-n/
                        
                x02/
                ...
                xnn/
            sub_x01/
            sub_x02/
            ...
            sub_xnn/

        image_processing/
            logs/        
            .working/     
            fmriprep/     (output for fmriprep processing)
            freesurfer/   (output for freesurfer processing via fmriprep)
            netprep/      (output for freesurfer processing via fmriprep)
            act/          (output for antsCorticalThickness BID app)
            bids_app1/
            bids_app2/
            ...
            
        image_analysis/

        mriqc/
            derivatives
            logs
            reports
            restpcasl.csv
            T1w.csv
            work
            working

        scripts/
        templates/

## Aliases



## Scripts



## Design Details
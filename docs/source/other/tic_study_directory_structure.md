# Purpose:

This page describes the common directory structure that is currently being shared among TIC studies.

# Background

Finding data is always a challenge in large studies. It helps to have a systematic way for data to be stored with a common naming convention. The data structure presented here is intended to be a guideline as opposed to a set of stringent rules.  Individual investigators and studies will have their own needs and need to have the flexibility to do what is best for them.
Regardless of the final data structure chosen for each study this page will serve as a set of guidelines.

# Directory Structure

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
            .logs/        (currently called fmriprep_logs)
            .working/     (currently called fmriprep_working)
            fmriprep/     (output for fmriprep processing)
            freesurfer/   (output for freesurfer processing via fmriprep)
            netprep/      (output for freesurfer processing via fmriprep)
            other1/
            other2/

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

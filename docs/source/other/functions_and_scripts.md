
# Scripts

**bids_processing_status.py** - Will search for files that match a specific pattern and compare it to the
acrostic.list in the BIDS_PATH.

**clean_bids.sh**       - Runs MRI Quality Control as a group on subjects in MRIQC directory.

**hdc_look.py**         - Display DICOM information and Heudiconv files used for DICOM to NIFTI conversion.

**hdc_clean.py**        - Deletes all files created by the hdc.sh except the participant inforamation in
participants*.tsv, acrostic.list, and acrostic.csv.

<br />
<br />

# Functions


<br />
<br />

# Singularity Scripts

**act.sh**              - BIDS App for ANTs Cortical Thickness.

**fmriprep.sh**         - Runs fmriprep on a single subject.

**hdc.sh**              - Converts DICOM to NIFTI and places them in the BIDS data directory.

**mriqc.sh**            - Runs MRI Quality Control on a single subject.

<br />

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


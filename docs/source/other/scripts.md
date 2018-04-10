# Scripts

**hdc.sh**               - Converts DICOM to NIFTI and places them in the BIDS data directory.

**hdc_look.py**          - Displays the DICOM header information and those DICOM images selected for conversion.

**clean_bids.sh**        - Runs MRI Quality Control as a group on subjects in MRIQC directory.

**fmriprep.sh**          - Runs fmriprep on a single subject.  

**mriqc.sh**             - Runs MRI Quality Control on a single subject.

**mriqc_group.sh**       - Runs MRI Quality Control as a group on subjects in MRIQC directory.

# Singularity Scripts

The singularity scripts:
* hdc.sh
* fmriprep.sh
* mriqc.sh
* mriqc_group.sh

have been written to minimize the number of arguments that you have to remember for each study
while allowing you flexibility to call scripts with various options. For example, the fmriprep.sh
script sets several environment variables and then calls the command

nohup time /usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 \
                 $APP_SINGULARITY_IMAGE \
                 $ACTIVE_BIDS_PATH \
                 $ACTIVE_APP_OUTPUT_PATH \
                 --work-dir $ACTIVE_APP_WORKING_PATH \
                 participant ${@} > $log_file 2>&1 &

The ${@} is the bash syntax to pass all of the variables from the command line and insert them
for ${@}.  If you want to see the fmriprep help you can call the alias function

If you call fmriprep -h you can see the help for fmriprep with all of its optional
parameters. For example if you want to run fmriprep with only anatomical processing you can run
the script

fmriprep.sh --participant-label imove1061 --anat-only


We are hoping this structure will allow simplicity for new users with flexibilty for experieneced
users. Advanced


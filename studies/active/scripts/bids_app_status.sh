#!/usr/bin/env bash

echo ' ' | tee $log_file
echo 'datetime.now()         = ' $(date) | tee -a $log_file
echo 'active study           = ' $ACTIVE_STUDY | tee -a $log_file
echo 'bids app               = ' $BIDS_APP | tee -a $log_file
echo 'bids path              = ' $ACTIVE_BIDS_PATH | tee -a $log_file
echo 'log path               = ' $ACTIVE_IMAGE_PROCESSING_LOG_PATH | tee -a $log_file
echo 'output path            = ' $ACTIVE_APP_OUTPUT_PATH | tee -a $log_file
echo 'working path           = ' $ACTIVE_APP_WORKING_PATH | tee -a $log_file
echo 'SUBJECTS_DIR           = ' $SUBJECTS_DIR | tee -a $log_file
echo 'singularity command    = ' $SINGULARITY_COMMAND
echo 'app singularity image  = ' $APP_SINGULARITY_IMAGE | tee -a $log_file
echo 'log file               = ' $log_file | tee -a $log_file
echo ' ' | tee -a $log_file
echo 'parameters             = ' ${parameters}  | tee -a $log_file
echo ' ' | tee -a $log_file
echo ' ' | tee -a $log_file

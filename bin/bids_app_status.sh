#!/usr/bin/env bash

echo ' ' | tee log_file
echo 'datetime.now()         = ' $(date) | tee log_file
echo 'active study           = ' $ACTIVE_STUDY | tee log_file
echo 'bids app               = ' $BIDS_APP | tee log_file
echo 'bids path              = ' $ACTIVE_BIDS_PATH | tee log_file
echo 'log path               = ' $ACTIVE_IMAGE_PROCESSING_LOG_PATH | tee log_file
echo 'output path            = ' $ACTIVE_APP_OUTPUT_PATH | tee log_file
echo 'working path           = ' $ACTIVE_APP_WORKING_PATH | tee log_file
echo 'SUBJECTS_DIR           = ' $SUBJECTS_DIR | tee log_file
echo 'singularity command    = ' $SINGULARITY_COMMAND
echo 'app singularity image  = ' $APP_SINGULARITY_IMAGE | tee log_file
echo 'log file               = ' $log_file | tee log_file
echo ' ' | tee log_file

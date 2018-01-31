NiPype allows you to control it's execution and logging behavior.  Detailed information about its configuration settings may be found here [http://nipype.readthedocs.io/en/latest/users/config_file.html](http://nipype.readthedocs.io/en/latest/users/config_file.html)

You can create an nipype.cfg file for fmriprep by including it in the --config parameter.  As an example here is a configuration file I created to maximize the information provided to debug potential problems with the workflow

[logging]
workflow_level = DEBUG
filemanip_level = DEBUG
interface_level = DEBUG
log_to_file=true
log_directory=/Users/bkraft/tic/cenc/single/log
[execution]
stop_on_first_crash = true
hash_method = timestamp
display_variable = :1
keep_inputs = true%


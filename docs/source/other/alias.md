# Aliases

Aliases are simple commands that are defined to help move among the various directories
of the study.  They also provide a way to perform simple commands. An alias, unlike a
script, does not have a .sh or .py extension. Aliases for each study are defined in the
studies tic folder ($TIC_PATH/studies/<study>). Aliases that are common among all the
studies are defined in $TIC_PATH/init.

    tic_help       - Launches the TIC Sphinx documentation.
    tic_info | tsi - Displays information about the current TIC session (tic_path, active_study, and subjects_dir)

    asi - Displays information about the current active study.  This is a long list and most users
    may find this to be information overload.
    
    cdas     - change directory to active study main directory
    cdb      - change directory to  BIDS directory
             
    cdip     - change directory to image processing directory (fmriprep, netprep, etc.)
    cdipl    - change directory to image processing log directory 
    cdin     - change directory to DICOM incoming directory
             
    cdqc     - change directory to QC directory
    cdqcmri  - change directory to MRIQC directory 
    cdqcmril - change directory to MRIQC log directory 

A bash function has been created to allow you to quickly switch between studies by changing the active study.  This function calls
the python function study_switcher.py.  Both functions take arguments to control the functions behavior.

To display the help of study_switcher.py (or any python function) set the optional argument -h.

```
   >>sw -h  
   
   usage: study_switcher [-h] [-d] [-v] {hfpef,synergy,infinite,cenc,imove,mcf}

    positional arguments:
    {hfpef,synergy,infinite,cenc,imove,mcf}
                      Switch to a different study.

    optional arguments:
    -h, --help            show this help message and exit
    -d, --default         Set selected study as default.
    -v, --verbose         Display contents of study_switcher output_file.

    ACTIVE_STUDY is now HFPEF
```

To switch to a different study

```
    >> sw cenc

        ACTIVE_STUDY is now CENC

```

To set your default study.  Setting the default study produces no output unless you set the -v option.

```
    >> sw cenc -d
    >>
```


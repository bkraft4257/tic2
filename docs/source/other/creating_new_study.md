Creating a New Study
====================

We are hoping that TIC will explode and that there will be many new
studies added to the TIC repository. We have created a Python script,
create_new_study.py, to help adding a new study to the TIC repository.

This script will create the directories (bids, image_processing,
image_analysis, etc.) where you will store the new study's data and
derivatives. The script will also create a <study_name> folder in the
specified TIC path.

To create a new study in TIC you can run the command

```
   >>> create_new_study.py <study_name>  <study_path> <tic_path>
   
```

<study_name> is the name of your new study. It should be a short name
without any punctuation.

<study_path> is the path where you are going to
store the study's data.

<tic_path> it the path of your TIC repository where you want to add the
the initial scripts and configuration for the new study.

Once you have initialized your study you will have to add it commit the
TIC repository.

The create_new_study.py script will create the following files in the
$TIC_PATH

```

$TIC_PATH/studies/<study_new>/

    aliases.sh
    cenc_init.sh
    environment.sh

    scripts


<study_path>/<study_name>/
    
    /bids
    
    /qc
        /mriqc
    
    /image_analysis
    
        
    /image_processing
        /logs



```


Welcome to the nipype_workflows wiki!


fmriprep is a NiPype workflow created by Russ Poldrack’s group.  It essentially does lots of the things that TIC has been working on for the last two years with Dr Heugenschmidt.

The goal is to look into using fmriprep instead of what I wrote.

It has many advantages compared to other methods. 1) software is open source, 2) it uses NiPype,  3) it performs all of the preprocessing steps needed.   4) it uses the BIDS file format.

The BIDS file format is similar to what we already do with some notable exceptions.   1) DICOM and NIFTI images need to be separated.   2) Naming convention must be strictly enforced and includes subject ID in filenames.  3) NIFTI files are separated from the derived files.   This is similar to our input, methods, results.

I recommend reorganizing the data for studies as follows:

<study>/dicom  
<study>/data  
<study>/derived/  
<study>/results  
<study>/work

Each section is independent of the others:
 - dicom is where the dicom to nifti conversion occurs.
 - data is where the nifti images reside in the BIDS file structure.
 - derived is where the output from fmriprep goes. It contains subfolders called fmriprep and freesurfer.
 - results contain final QA’d results.
 - work is the working directory for fmriprep.  
    . If you don’t specify a working directory it writes the intermediate files into the docker image.  
    . This makes it impossible to see intermediate results.
_______________________________________________________________
   Specifying a working directory is not optional!
_______________________________________________________________

After installation according to the instructions you run:  
    fmri_docker <abs_data_path> <abs_output_path>

Known Issues & Workarounds-

 - Shell does not find fmri_docker.  
        One workaround that worked was to find where fmri_docker was installed by pip and find the python file fmri_docker.py.  Use this file to run fmri_docker. Ad-hoc and hacky, but the files will run. fmriprep creator NeuroStars has been emailed, asking about this deviation from the instructions on their webpage.

  --Credits:  
bkraft4257 experimented, determined and wrote these instructions.
kchawla-pi reformatted and uploaded them to the wiki

>
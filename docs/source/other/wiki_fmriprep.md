fmriprep is a NiPype workflow created by Russ Poldrack’s group.  It essentially does lots of the things that I have been working on for the last two years with Christina.  fmriprep has many advantages compared to other methods. 1) software is open source, 2) it uses NiPype,  3) it performs all of the preprocessing steps needed.   4) it uses the BIDS file format.

The BIDS file format is similar to what we already do with some notable exceptions.   1) DICOM and NIFTI images need to be separated.   2) Naming convention must be strictly enforced and includes subject ID in filenames.  3) NIFTI files are separated from the derived files.   This is similar to our input, methods, results.

# BIDS file structure

I recommend reorganizing the data for studies as follows:
<study>/dicom
<study>/data
<study>/derived/
<study>/results
<study>/work

each section is independent of the others. dicom is where the dicom to nifti conversion occurs.  data is where the nifti images reside in the BIDS file structure. derived is where the output from fmriprep goes. It contains subfolders called fmriprep and freesurfer.  results contain final QAed and final results.  work is the working directory for fmriprep.  If you don’t specify a working directory (-w option) it writes the intermediate files in the docker image, which makes it impossible to review intermediate results.


# Installation

Documentation to install fmriprep is located here. [https://fmriprep.readthedocs.io/en/stable/installation.html](https://fmriprep.readthedocs.io/en/stable/installation.html)  You install fmriprep with pip.

pip install --user --upgrade fmriprep-docker

Craig has installed fmriprep-docker, Docker, and Singularity on aging1a.  I have reached out to Will Robinson about installing Singularity on the HPCC cluster.

When I tried this my shell couldn’t find fmri_docker. I found where fmri_docker was installed by pip and found the python file fmri_docker.py.  I used this file to run fmri_docker.  I don’t think this is 100% correct but the files will run.   I have sent a email to NeuroStars asking about this deviation from the instructions on their webpage.

## Posted question to NeuroStars

I am new to Docker and fmriprep. I have read the documentation and am running it on a simple data set. I have encountered some problems with modules not being found. This leads me to think I have done something wrong. I installed fmriprep-docker with pip on my Mac OS 10.12.

$ pip install --user --upgrade fmriprep-docker
The installation worked fine. The run command as stated in the instructions did not work.

$ fmriprep-docker /path/to/data/dir /path/to/output/dir participant
The command wasn't found. This may make sense sinceI didn't make any changes to my environment after the pip install. Instead I had to find where pip installed fmriprep. There I found the python file fmriprep_docker.py

I then ran the command

/path/to/fmriprep/fmriprep-docker.py /path/to/data/dir /path/to/output/dir participant

and the command ran and started chugging away at my data. I am concerned that the slight difference between fmriprep_docker and fmriprep_docker.py is causing my problems that I am experiencing.

Once I know I am correctly running fmriprep_docker I will send additional information about my errors.

Thanks for your help,

Bob


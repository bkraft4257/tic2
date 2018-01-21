# Setting up your TIC Environment

TIC is hosted on GITHUB. This allows easy access to the software.
However, each individual investigators setup will be different depending
upon investigators computers. We have a TIC environment setup on aging1a
and aging2a, which is the easiest way to setup your TIC environment.

### Setup BASH or ZSH

Set your shell to bash or zsh. These two shells are 99% compatible.
   The zsh has some additional bells and whistles. If you are interested
   in the zsh you should check out oh-my-zsh at http://ohmyz.sh/. It is
   a wonderful shell with frequent updates and nice features. I (bkraft)
   use it just for the auto-complete features.


### Install Python 3.6 or higher

TIC expects a user to be using Python 3.6 or higher. You can check
which version of python you are using in your shell with

```console
   >>> python --version
```

If you are not running python version 3.6 or higher on your machine you
will need install Python 3.6 on your machine and setup your shell to
point to this version. TIC recommends Anaconda distribution of Python.
You can download Anaconda distribution of Python from https://www.anaconda.com/download/


If you are running your analysis on aging1a or aging2a Anaconda Python
3.6 has already been installed at /opt/anaconda3-4.4.0/bin/python

Later we will be modifying the tic_wake_aging1a_environment.sh file to
your specific environment.



### Cloning TIC on your computer from GitHub

If you are installing TIC on your own computers you will need to
clone the software from the GitHub repository.

   1. Create a directory where you want to install the TIC software
      files.
   2. git clone https://github.com/bkraft4257/tic2.git

This will clone the TIC files to this directory. The TIC files have
already been installed on aging1a/2a. You may want to keep multiple
copies of the GitHub files on your computer. This allows you to modify
the files for testing things without affecting other users or changing
processing for a study currently in progress.


### Running the initial TIC Setup

Once you are using the bash/zsh is created run the command

```console
   >>> export TIC_PATH=<tic_path>
   >>> $TIC_PATH/init/tic_initial_setup.py
```

where <tic_path> is the full path where you cloned the TIC GitHub
repository. On aging1a/2a it is /gangd/tic/

This command will create the directory $HOME/.tic for storing the local
copies of your tic environment files.


### Modifying your .bashrc or .zshrc

Now that you have successfully copied the TIC files from the repository
to .tic you need to modify your .bash or .zshrc file to include the
following

```console
# TIC Setup

export TIC_PATH=/gandg/tic2/  
export TIC_INIT_PATH=$HOME/.tic

source $TIC_INIT_PATH/tic_zshrc.sh
```

### Modifying tic_wake_aging1a_software_environment.sh

This is where things become complicated. If you are planning to run TIC
on your own computer you will need to have the software that you are
planning to run on your local computer locally installed.

Here is the list of software that is currently installed on aging1a

* FreeSurfer
* FSL
* ANTs
* heudiconv (singularity image)
* fmriprep (singularity image)
* mriqc (singularity image)
* bids-validator
* mricron
* itksnap
* nipype
* Matlab
    * SPM
    * GraphVar
    * CONN

You don't have to install each of these software packages on your
computer. However, at a bare minimum we recommend

* FreeSurfer
* FSL
* ANTs
* fmriprep (singularity image)
* bids-validator
* heudiconv (singularity image)
* nipype

if you are planning to use SPM and CONN then you will also need to
install Matlab along with these packages. Don't forget to update your
Matlab startup file.

Once you have installed these packages on your computer you will need to
copy the file ~/.tic/tic_wake_aging1a_environment.sh to a file that can
be used for your computer. For example,

```console
cp ~/.tic/tic_wake_aging1a_environment.sh ~/.tic/tic_my_computer_environment.sh
```
You can then modify your tic_my_computer_environment.sh to point to
these individual software packages. You also need to change
~/.tic/tic_zshrc.sh to source your new tic_my_computer_environment.sh
file. This means changing

```console
source ${TIC_INIT_PATH}/tic_wake_aging1a_environment.sh
```

to

```console
source ${TIC_INIT_PATH}/tic_wake_aging1a_environment.sh
```


### Final Check

You should now be able to logout of you computer and log back in. If
things are setup correctly you should see the following when you log
back into your computer and open up a terminal

```console
-------- freesurfer-Linux-centos6_x86_64-stable-pub-v5.3.0 --------
Setting up environment for FreeSurfer/FS-FAST (and FSL)
FREESURFER_HOME   /aging1/software//freesurfer
FSFAST_HOME       /aging1/software//freesurfer/fsfast
FSF_OUTPUT_FORMAT nii.gz
SUBJECTS_DIR      /aging1/software//freesurfer/subjects
MNI_DIR           /aging1/software//freesurfer/mni
FSL_DIR           /aging1/software//fsl5.09


TIC_PATH     : /gandg/tic2/
SUBJECTS_DIR : /aging1/software//freesurfer/subjects
umask        : 002

>>>

```

The above assumes that you have FreeSurfer and FSL properly installed
and referenced in your tic_my_computer_environment.sh file. If you don't
see that send bkraft@wwakehealth an email and he can help you debug the
problem.

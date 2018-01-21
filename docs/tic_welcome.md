# TIC Welcome

## Introduction

The Imaging Collective is a group of independent NeuroImaging
researchers who are willing to share their knowledge, expertise, and
software for analyzing their data. Our goal is to make processing data
faster, easier, and with a broader set of tools among our members then
individuals could do on their own.


Software created by individual investigators is intended to be
open-source and shared with TIC. Most of the software developed by TIC
is intended to make processing neuroimaging data easier and use common
tools. These are the tools we are asking people to share.

**Sharing software tools is completely voluntary.** Investigators may
develop their own proprietary tools as part of their own research. We
hope these tools will be shared through collaborations but investigators
are not obligated to share these toosl.

TIC has adopted the Brain Imaging Data Structure (BIDS) for easy
collaboration. BIDS provides a common directory structure storing
NeuroImaging data. Along with the data the BIDS structure contains JSON
files which contain additional information about the neuroimaging data,
which may be used as a quick reference.

BIDS has encouraged investigators to create BIDS Apps. These apps
provide a convenient and easy way for investigators to process their
data. TIC relies heavily on these Apps to do their processing. Each App
has their own little quirks. By identifying these quirks and sharing our
experience with how to run the software TIC members can get more down
with less effort.

## Setting up your TIC Environment

TIC is hosted on GITHUB. This allows easy access to the software.
However, each individual investigators setup will be different depending
upon investigators computers. We have a TIC environment setup on aging1a
and aging2a, which is the easiest way to setup your TIC environment.

### TIC on aging1a/aging2a

TIC software is currently residing on aging1a and aging2a in the
directory /gandg/tic2, which is a clone of the GitHub repository. Here
are the steps for setting up your environment.

1. Set your shell to bash or zsh. These two shells are 99% compatible.
   The zsh has some additional bells and whistles. If you are interested
   in the zsh you should check out oh-my-zsh at http://ohmyz.sh/. It is
   a wonderful shell with frequent updates and nice features. I (bkraft)
   use it just for the auto-complete features.

2. TIC expects a user to be using Python 3.6 or higher. You can check
   which version of python you are using in your shell with

```console
   >>> python --version
```

If you are not running python version 3.6 or higher on your machine you
will need install Python 3.6 on your machine and setup your shell to
point to this version. TIC recommends Anaconda distribution of Python.
If you are running your analysis on aging1a or aging2a Anaconda Python
3.6 has been installed at

/opt/anaconda3-4.4.0/bin/python

You can set this to your PYTHON distribution by adding the following in
your $HOME/.basrhc or $HOME/.zshrc. The commands to include in your
respective shell setup file are

export PYTHON_PATH=/opt/anaconda3-4.4.0/bin/python  
export PATH=$PYTHON_PATH:$PATH


3. Once you are using the bash/zsh is created run the command

```console
   >>> /gandg/tic2/init/setup_tic.sh
```

This command will create the directory $HOME/.tic for storing the local
initil

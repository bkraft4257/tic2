
TIC Overview
============

For processing data (the TIC way), TIC provides various Python and bash
scripts, functions, aliases, and perhaps most important BIDS Apps. By
creating a set of functions that can be used on multiple studies
investigators can share resources and knowledge. This allows each
investigator to do more on their data with less effort.

This page will describe the TIC Environment and TIC project structure.
TIC aliases,


GitHub
------

TIC is stored on GitHub. You can find the TIC repository at

https://github.com/orgs/theimagingcollective/dashboard

This allows anyone to download, clone, and/or fork the software.
Students who are accustom to processing data one way will be able to
continue to process the data when they graduate and move on to a
different labs.


TIC Project Structure
---------------------

The high level view of the TIC directory structure is

    ./bin

    ./init

    ./docs
        /build
        /source

    ./studies
        /active
        /hfpef
        /infinite
        /synergy
        /...

    ./tic_core

**bin** - contains executable Python and Bash scripts. When the TIC
environment is setup correctly the $TIC_PATH/bin is added to your
environment path, $PATH, so these functions and scripts can be easily
accessible.

**init** - contains files and scripts that are used to initialize and
help setup a users TIC environment. Many of these files are copied to
the users home directory in the directory .tic

**docs** - contains the HTML, ReStructured Text, and Markdown files for
generating the TIC documnetation. The TIC documentation is a living
document and should grow as more people join TIC. Documentation can
easily be created and added to the TIC HTML page by writing in Markdown
or Restructed test and adding these documents to the Sphinx Index.
Additional information will be provided on how one may contribute to the
TIC documentation.

**studies** - contains functions for the individual studies.  The active study
is unique in that it contains functions that will be used across multiple studies but are
applied according to the environment variable $ACTIVE_STUDY.

**tic_core** - contains functions that are used by the python scripts.


:ref:`_tic_documentation-overview`


TIC Environment
---------------



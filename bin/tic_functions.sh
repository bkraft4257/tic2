#!/bin/env bash


# A function to launch multiple fslview windows, one per image. This allows one to use fslview for images that do not have 
# the same pixel dimensions.

function fslview_all_function() {

	 for ii in $@; do 
	     fslview $ii & 
	 done

}


function cdls() {
    cd $1;
    lsreport
}


#
# Copy the file and add a date stamp to it. 
#

function cpds() {

    for ii in $@; do 
	cp $ii $ii.d$( date +"%m%d%y")
    done
}

#
# Rename file by adding a date stamp on the end
#

function mvds() {

    for ii in $@; do 
	mv $ii $ii.d$( date +"%m%d%y")
    done
}


# lsreport() dumps out the path and the current contents of the directory

function lsreport_function() {
    
    echo
    pwd 
    echo
    ls $@
    echo
}




# killbranch()  kills a specific branch of the tree

function killbranch() {
    
#   http://stackoverflow.com/questions/392022/best-way-to-kill-all-child-processes

    local _pid=$1
    local _sig=${2-9}
    kill -stop ${_pid} # needed to stop quickly forking parent from producing children between child killing and parent killing

    for _child in $(ps -o pid --no-headers --ppid ${_pid}); do

        cmd="killbranch ${_child} ${_sig}"
	echo $cmd
	$cmd
    done

    cmd="kill -${_sig} ${_pid}"
    echo $cmd
    $cmd
}



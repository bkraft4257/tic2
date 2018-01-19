#!/bin/bash
#
# Use as follows 
#
#    cat linkInfinite_v2.txt | xargs -L 1 ./infCreateLinks.sh
#

niftiPath=../nifti/
ln -sf ${niftiPath}${1} ${2}


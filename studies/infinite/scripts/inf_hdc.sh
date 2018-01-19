#!/bin/bash


/cenc/software/heudiconv/python/heudiconv/bin/heudiconv \
-c dcm2niix -b --minmeta \
-f /gandg/infinite/imaging_data/scripts/inf_protocol.py \
-o /gandg/infinite/imaging_data/bids/ \
-d '{subject}/{session}/data/dicom/dicom.tar.gz' "$@"
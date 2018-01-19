#!/bin/bash

subject_id=${1}

for ii in 1 2; do

    echo sub-${subject_id}_ses-${ii}

    /cenc/software/heudiconv/python/heudiconv/bin/heudiconv \
	 -c dcm2niix -b --minmeta -f /gandg/infinite/imaging_data/scripts/inf_protocol_v2.py \
	 -o /gandg/infinite/imaging_data/bids/ \
	 -d '{subject}/{session}/data/dicom/dicom.tar.gz' \
	 -s inf0${subject_id} \
	 -ss ${ii} > hdc_inf0${subject_id}_${ii}.log

    echo '============================================='
done


#/cenc/software/heudiconv/python/heudiconv/bin/heudiconv \
#-c dcm2niix -b --minmeta -f /gandg/infinite/imaging_data/scripts/inf_protocol_v2.py \
#-o /gandg/infinite/imaging_data/bids/ \
#-d '{subject}/{session}/data/dicom/dicom.tar.gz' \
#-s inf0${subject_id} \
#-ss 2 > hdc_inf0${subject_id}_2.log


#hdc_inf -d '{subject}/{session}/data/dicom/dicom.tar.gz' -s inf0${subject_id} -ss 2 -o /gandg/infinite/imaging_data/bids > hdc_inf0${subject_id}_2.log
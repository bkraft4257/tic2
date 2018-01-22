#!/usr/bin/env bash


alias catlast='ls -1drt * | tail -1 | xargs cat'
alias cl='ls -1drt * | tail -1 | xargs cat'

alias cdtic='cd $TIC_PATH; lsreport_function'
alias cdstudies='cd $STUDIES_PATH; lsreport_function'
alias cdtemplates='cd $TEMPLATES_PATH; lsreport_function'

alias cdixi='cd $TEMPLATE_IXI; lsreport_function'
alias cdinia='cd $TEMPLATE_INIA19; lsreport_function'
alias cdmni='cd $TEMPLATE_MNI; lsreport_function'

alias cdsd='cd $SUBJECTS_DIR; lsreport_function'

alias cda='echo; echo $PWD; cd $(pwd -P); echo $PWD; echo; ls; echo'

alias retic='source $TIC_PATH/tic_aliases.sh'
alias lstic='echo; echo $TIC_PATH; echo'

FMRIPREP_PATH=/cenc/software/fmriprep/
FMRIPREP_SINGULARITY_IMAGE_V1=$FMRIPREP_PATH/poldracklab_fmriprep_latest-2017-08-28-8f9c2862d74f.img
FMRIPREP_SINGULARITY_IMAGE_V2=$FMRIPREP_PATH/poldracklab_fmriprep_latest-2017-11-10-9ae650872d1e.img

FMRIPREP_SINGULARITY_IMAGE=$FMRIPREP_SINGULARITY_IMAGE_V1

MRIQC_SINGULARITY_IMAGE=/cenc/software/mriqc/poldracklab_mriqc_latest-2017-08-30-f54388a6fb57.img
HDC_SINGULARITY_IMAGE=/cenc/software/heudiconv/nipy_heudiconv-2017-09-26-6bef64b746f6.img

alias fmriprep='/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 $FMRIPREP_SINGULARITY_IMAGE'
alias mriqc='/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 $MRIQC_SINGULARITY_IMAGE'

alias hdc_convert='/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 -c dcm2niix $HDC_SINGULARITY_IMAGE'

alias hdc_find_repeats='find ${session_dir} -name \"*.[2-9].*\"' 
alias hdc_find_1='find ${session_dir} -name \"*.[2-9].*\"'
alias hdc_find_2='find ${session_dir} -name \"*.[2-9].*\"'
alias hdc_rename_1='find ${session_dir} -name \"*.1.*\" | xargs rename .1. .' 

alias hdc_scan='/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 $HDC_SINGULARITY_IMAGE -f /cenc/software/heudiconv/hdc_convertall.py -c none'
alias hdc_add_header='$HDC_PATH/hdc_add_header.py'
alias hdc_csvlook='$HDC_PATH/hdc_csvlook.sh'
alias hdc_pdlook='$HDC_PATH/hdc_pdlook.py'
alias hdc_copy='cp $HDC_PATH/hdc_template.py .' 
alias hdc_find_dcm='$HDC_PATH/hdc_find_dcm.sh' 
alias hdc_find_dicom='$HDC_PATH/hdc_find_dcm.sh' 

alias ag='alias | grep'
alias hg='history | grep '
alias eg='env | grep '
alias lg='ls | grep '

alias lsp='echo; echo $PATH | tr ":" "\n" | cat -n | sort -n -r; echo'          # Enumerates path
alias lspp='echo; echo $PYTHONPATH | tr ":" "\n" | cat -n | sort -n -r; echo'   # Enumerates Python Path
alias lssd='echo; echo $SUBJECTS_DIR; echo'

alias l1='ls -1d'
alias lld='ld -ld'
alias llr='ls -lrt'
alias lls='ls -lrS'

alias frv='freeview'
alias fsv='fslview'
alias fsvall='fslview_all_function'

alias lnflatten='${TIC_PATH}/lnflatten.sh'
alias cpflatten='${TIC_PATH}/cpflatten.sh'

source ${TIC_PATH}/studies/active/aliases.sh
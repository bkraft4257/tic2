#!/usr/bin/env bash

alias tic_make_docs='cd $TIC_PATH/docs/; make clean; make html; cd -; firefox $TIC_PATH/docs/build/html/index.html&'

alias dfgandg='echo; df -h /gandg/; echo'

alias tic_help='firefox $TIC_PATH/docs/build/html/index.html&'

source $TIC_PATH/bin/tic_functions.sh

alias sw='study_switcher.py '

alias swh='study_switcher.py -s hfpef; source $TIC_INIT_PATH/tic_study_switcher.sh'
alias swi='study_switcher.py -s infinite; source $TIC_INIT_PATH/tic_study_switcher.sh'
alias sws='study_switcher.py -s synergy; source $TIC_INIT_PATH/tic_study_switcher.sh'

alias catlast='ls -1drt * | tail -1 | xargs cat'
alias cl='ls -1drt * | tail -1 | xargs cat'

alias cdtic='cd $TIC_PATH; lsreport_function'
alias cdtemplates='cd $TEMPLATES_PATH; lsreport_function'

alias cdixi='cd $TEMPLATE_IXI; lsreport_function'
alias cdinia='cd $TEMPLATE_INIA19; lsreport_function'
alias cdmni='cd $TEMPLATE_MNI; lsreport_function'

alias cdsd='cd $SUBJECTS_DIR; lsreport_function'

alias cda='echo; echo $PWD; cd $(pwd -P); echo $PWD; echo; ls; echo'

alias retic='source $TIC_PATH/init/tic_aliases.sh'
alias lstic='echo; echo $TIC_PATH; echo'

alias fmriprep='/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 $FMRIPREP_SINGULARITY_IMAGE'
alias mriqc='/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 $MRIQC_SINGULARITY_IMAGE'

alias hdc_convert='/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1  $HDC_SINGULARITY_IMAGE -c dcm2niix'

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
alias fse='fsleyes'

alias fsvall='fslview_all_function'

alias lnflatten='${TIC_PATH}/lnflatten.sh'
alias cpflatten='${TIC_PATH}/cpflatten.sh'

source ${TIC_PATH}/studies/active/aliases.sh
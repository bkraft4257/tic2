#!/usr/bin/env bash

# Set environment variables that are machine dependent.

case $(hostname) in
  aging1a | aging2a)
	SOFTWARE_PATH=/aging1/software/
    ;;

  *)
     echo "Unknown HOSTNAME"
esac


# Templates

export TEMPLATES_PATH=/cenc/software/imagewake2/release/templates
export TEMPLATE_IXI=${TEMPLATES_PATH}/ixi
export TEMPLATE_MNI=${TEMPLATES_PATH}/mni
export TEMPLATE_INIA19=${TEMPLATES_PATH}/inia19_rhesus_macaque

# Setup Python2 and Python 3

export PYTHON2_PATH=/opt/anaconda2/bin
export PYTHON3_PATH=/opt/anaconda3-4.4.0/bin

export PATH="$PYTHON3_PATH:$PATH"
 
# Nipype Configuration
     export NIPYPE_PYTHON_PATH=$PYTHON3_PATH
     export NIBABEL_PATH=${SOFTWARE_PATH}/nibabel
     export PATH=${NIPYPE_PYTHON_PATH}:$PATH

# ANTS Configuration
    export ANTS_PATH='/aging1/software/ants/bin/'
    export ANTSPATH=$ANTS_PATH
    export PATH=${ANTSPATH}:$PATH

# MRIcron Configuration 
     export MRICRON_PATH=/opt/software/mricron
     export PATH=${MRICRON_PATH}:$PATH

# MIMP Configuration
    export MIMP_PATH=${SOFTWARE_PATH}/MIMP143
    export RRI_NIFTI_TOOLS_PATH=${SOFTWARE_PATH}/rri_nifti_tools


# ITKsnap Configuration
    export ITKSNAP_PATH=/aging1/software/itksnap3
    export PATH=${ITKSNAP_PATH}/bin:$PATH        


# FSL Configuration
   export FSL509_DIR=${SOFTWARE_PATH}/fsl5.09
   export FSL505_DIR=${SOFTWARE_PATH}/fsl5.05

   export FSLDIR=${FSL509_DIR}
   source ${FSLDIR}/etc/fslconf/fsl.sh

   export PATH=${FSLDIR}/bin:$PATH        


# FREE SURFER Configuration
   export TUTORIAL_DATA=/bkraft2/freesurfer
   export FREESURFER_HOME=${SOFTWARE_PATH}/freesurfer

#
#  echo doesn't work with scp.  [-t 1 ] checks to see if the current terminal is an
#  interactive terminal.  If it is you can setup FreeSurfer. If it is not 
#
#  http://stackoverflow.com/questions/12440287/scp-doesnt-work-when-echo-in-bashrc
#
#  This assumes that I don't want to call FreeSurfer when I running an scp command from
#  a remote computer. 

if [ -t 1 ]; then 
   echo
   source $FREESURFER_HOME/SetUpFreeSurfer.sh
   echo
fi


# Human Connectome Configuration  
   export HCP_WORKBENCH_PATH=/aging1/software/workbench/
   export PATH=${HCP_WORKBENCH_PATH}/bin_rh_linux64:$PATH        

   export HCPPIPEDIR=/aging1/software/hcp/Pipelines-master/
   export PATH=${HCPPIPEDIR}:$PATH        


# MATLAB and third Party Configuration 

   MATLAB_PATH=/aging1/software/R2015a/bin
   # MATLAB_PATH=/aging1/software/R2014b/bin
   export PATH=${MATLAB_PATH}:$PATH

   export SPM_PATH=${SOFTWARE_PATH}/SPM12
   export CONN_PATH=${SOFTWARE_PATH}/conn/conn18a
   export W2MHS_PATH=${SOFTWARE_PATH}/W2MHS/

# HEUDICONV
  
export TIC_SOFTWARE_PATH=/aging1/software/
export HDC_PATH=$TIC_SOFTWARE_PATH/heudiconv/

# SINGULARITY IMAGES

export FMRIPREP_PATH=$TIC_SOFTWARE_PATH/fmriprep/
export FMRIPREP_SINGULARITY_IMAGE=$FMRIPREP_PATH/poldracklab_fmriprep_latest-2017-11-10-9ae650872d1e.img
export MRIQC_SINGULARITY_IMAGE=$TIC_SOFTWARE_PATH/mriqc/poldracklab_mriqc_latest-2017-08-30-f54388a6fb57.img
export HDC_SINGULARITY_IMAGE=$TIC_SOFTWARE_PATH/heudiconv/nipy_heudiconv-2018-03-02-bf4d6e1d4d0e.img

export ANTS_CORTICAL_THICKNESS_SINGULARITY_IMAGE='/cenc/software/bids_apps/antsCorticalThickness/bids_antscorticalthickness-2017-10-14-95aa110c26f8.img'

export SINGULARITY_COMMAND='/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1'

PATH=$DCM2NIIX_PATH:$HDC_PATH:$HDC_PYTHONPATH:$PATH


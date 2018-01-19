# fmriprep.py

## Goal

fmriprep is a nipype workflow that takes structural and functional data
and performs basic fMRI preprocessing. This includes processing the data
through FreeSurfer.

## fmriprep location

fmriprep is run on aging1a as a singularity image. The singularity image
is located here

/cenc/software/fmriprep//poldracklab_fmriprep_latest-2017-08-28-8f9c2862d74f.img

An alias has been created as part of the TIC distribution that makes it
easier to run fmriprep from the command line. The alias is

alias fmriprep='/usr/local/bin/singularity run -w
                -B /cenc -B /gandg -B /bkraft1
                $FMRIPREP_SINGULARITY_IMAGE'

## Examples on how to use fmriprep



## fmriprep -h

bids fmriprep -h
usage: fmriprep [-h] [-v]
                [--participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]
                [-t TASK_ID] [--debug] [--nthreads NTHREADS]
                [--omp-nthreads OMP_NTHREADS] [--mem_mb MEM_MB] [--low-mem]
                [--use-plugin USE_PLUGIN] [--anat-only]
                [--ignore-aroma-denoising-errors]
                [--ignore {fieldmaps,slicetiming} [{fieldmaps,slicetiming} ...]]
                [--longitudinal] [--bold2t1w-dof {6,9,12}]
                [--output-space {T1w,template,fsnative,fsaverage,fsaverage6,fsaverage5} [{T1w,template,fsnative,fsaverage,fsaverage6,fsaverage5} ...]]
                [--template {MNI152NLin2009cAsym}]
                [--output-grid-reference OUTPUT_GRID_REFERENCE] [--use-aroma]
                [--fmap-bspline] [--fmap-no-demean] [--use-syn-sdc]
                [--force-syn] [--no-freesurfer] [--no-submm-recon]
                [-w WORK_DIR] [--reports-only] [--write-graph]
                bids_dir output_dir {participant}

FMRIPREP: fMRI PREProcessing workflows

positional arguments:

**bids_dir**  
the root folder of a BIDS valid dataset  
(sub-XXXXX folders should be found at the top level in this folder).
output_dir the output path for the outcomes of preprocessing and visual
reports {participant} processing stage to be run, only "participant" in
the case of FMRIPREP (see BIDS-Apps specification).

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

**Options for filtering BIDS queries:**

  --participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...], --participant-label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]
                        one or more participant identifiers (the sub- prefix can be removed)

  -t TASK_ID, --task-id TASK_ID
                        select a specific task to be processed

**Options to handle performance:**

--debug run debug version of workflow

--nthreads NTHREADS, --n_cpus NTHREADS, -n-cpus NTHREADS maximum number
of threads across all processes

--omp-nthreads OMP_NTHREADS maximum number of threads per-process

--mem_mb MEM_MB, --mem-mb MEM_MB upper bound memory limit for FMRIPREP
processes

--low-mem attempt to reduce memory usage (will increase disk usage in
working directory)

--use-plugin USE_PLUGIN nipype plugin configuration file

  --anat-only           run anatomical workflows only

--ignore-aroma-denoising-errors ignores the errors ICA_AROMA returns
when there are no components classified as either noise or signal

Workflow configuration:

  --ignore {fieldmaps,slicetiming} [{fieldmaps,slicetiming} ...]
                        ignore selected aspects of the input dataset to disable corresponding parts of the workflow

  --longitudinal        treat dataset as longitudinal - may increase runtime

  --bold2t1w-dof {6,9,12}
                        Degrees of freedom when registering BOLD to T1w images. 9 (rotation, translation, and scaling) is used by default to compensate for field inhomogeneities.

  --output-space {T1w,template,fsnative,fsaverage,fsaverage6,fsaverage5} [{T1w,template,fsnative,fsaverage,fsaverage6,fsaverage5} ...]
                        volume and surface spaces to resample functional series into

                         - T1w: subject anatomical volume

                         - template: normalization target specified by --template

                         - fsnative: individual subject surface

                         - fsaverage*: FreeSurfer average meshes

  --template {MNI152NLin2009cAsym}
                        volume template space (default: MNI152NLin2009cAsym)

  --output-grid-reference OUTPUT_GRID_REFERENCE
                        Grid reference image for resampling BOLD files to volume template space. It determines the field of view and resolution of the output images, but is not used in normalization.

**Specific options for running ICA_AROMA:**

--use-aroma add ICA_AROMA to
your preprocessing stream

Specific options for handling fieldmaps:
  --fmap-bspline        fit a B-Spline field using least-squares (experimental)
  --fmap-no-demean      do not remove median (within mask) from fieldmap

Specific options for SyN distortion correction:
  --use-syn-sdc         EXPERIMENTAL: Use fieldmap-free distortion correction
  --force-syn           EXPERIMENTAL/TEMPORARY: Use SyN correction in addition to fieldmap correction, if available

Specific options for FreeSurfer preprocessing:
  --no-freesurfer       disable FreeSurfer preprocessing
  --no-submm-recon      disable sub-millimeter (hires) reconstruction

Other options:

  -w WORK_DIR, --work-dir WORK_DIR
                        path where intermediate results should be stored

  --reports-only        only generate reports, don't run workflows. This will only rerun report aggregation,
  not reportlet generation for specific nodes.

  --write-graph         Write workflow graph.
aging1a ➜  bids
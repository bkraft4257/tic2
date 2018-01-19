# ANTS Cortical Thickness

https://github.com/BIDS-Apps/antsCorticalThickness

BIDS App ANTS Cortical Thickness (ACT) measures the Cortical Thickness
of T1W images contained in the anat directory of a BIDS data set.

Running ACT is similar to running other Singularity Images on the BIDS
data set. ACT applies a strict interpretation of the bids-validator. If
the bids-validator finds an anomaly will halt processing. I am still
trying to find a legitimate way around this. In the meantime, a hack
that works is to copy the BIDS directory and delete all files and sub
directories until you contain only anatomical images in the anat
directory. It is much easier to make a single directory pass the
bids-validator.


### Examples

```console

nohup time /usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 \
/cenc/software/bids_apps/antsCorticalThickness/bids_antscorticalthickness-2017-10-14-95aa110c26f8.img \
$BIDS_PATH $IMAGE_PROCESSING_PATH participant &> /gandg/bkraft/data/bids_ds001/image_processing/logs/act_ds001.logs &


```

### Usage
This App has the following command line arguments:

		usage: run.py [-h]
                  [--participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]
                  [--n_cpus N_CPUS]
                  [--stage {brain_extraction,template_registration,tissue_segmentation,qc,cortical_thickness}]
                  [-v]
                  bids_dir output_dir {participant}

    Cortical thickness estimation using ANTs.

    positional arguments:
      bids_dir              The directory with the input dataset formatted
                            according to the BIDS standard.
      output_dir            The directory where the output files should be stored.
                            If you are running group level analysis this folder
                            should be prepopulated with the results of
                            the participant level analysis.
      {participant}         Level of the analysis that will be performed. Multiple
                            participant level analyses can be run independently
                            (in parallel) using the same output_dir.

    optional arguments:
      -h, --help            show this help message and exit
      --participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]
                            The label(s) of the participant(s) that should be
                            analyzed. The label corresponds to
                            sub-<participant_label> from the BIDS spec (so it does
                            not include "sub-"). If this parameter is not provided
                            all subjects should be analyzed. Multiple participants
                            can be specified with a space separated list.
      --n_cpus N_CPUS       Number of CPUs/cores available to use.
      --stage {brain_extraction,template_registration,tissue_segmentation,qc,cortical_thickness}
                            Which stage of ACT to run
      -v, --version         show program's version number and exit

To run it in participant level mode (for one participant):

    docker run -i --rm \
		-v /Users/filo/data/ds005:/bids_dataset:ro \
		-v /Users/filo/outputs:/outputs \
		bids/antscorticalthickness \
		/bids_dataset /outputs participan
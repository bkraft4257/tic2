# BIDS Apps

BIDS Apps are a coolection of Docker and Singularity images that are
intended to simplify the processing of neuroimaging data. When running
these BIDS Apps on aging1a or aging2a the singularity images for these
apps can be found here

/cenc/software/bids_apps


## ANTS Cortical Thickness

https://github.com/BIDS-Apps/antsCorticalThickness

### Examples

```console

ACT_SINGULARITY_IMAGE=/cenc/software/bids_apps/antsCorticalThickness/bids_antscorticalthickness-2017-10-14-95aa110c26f8.img
ACT_SINGULARITY_COMMAND='/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 $ACT_SINGULARITY_IMAGE'

act /gandg/bkraft/data/bids_ds001/bids /gandg/bkraft/data/bids_ds001/image_processing participant --participant_label 01

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
		/bids_dataset /outputs participant --participant_label 01
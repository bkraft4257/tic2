Creating a New Study
====================

First Steps
-----------

We are hoping that TIC will explode and that there will be many new
studies added to the TIC repository. We have created a Python script,
create_new_study.py, to help adding a new study to the TIC repository.

This script will create the directories (bids, image_processing,
image_analysis, etc.) where you will store the new study's data and
derivatives. The script will also create a <study_name> folder in the
specified TIC path.

To create a new study in TIC you can run the command

```
   >>> create_new_study.py <study_name>  <study_data_path> <tic_path>
   
```

<study_name> is the name of your new study. It should be a short name
without any punctuation.

<study_path> is the path where you are going to
store the study's data.

<tic_path> it the path of your TIC repository where you want to add the
the initial scripts and configuration for the new study.

Once you have initialized your study you will have to add it commit the
TIC repository.

The create_new_study.py script will create the following files in the
$TIC_PATH

```

$TIC_PATH/studies/<study_new>/

    aliases.sh
    cenc_init.sh
    environment.sh

    scripts


<study_path>/<study_name>/
    
    /bids
    
    /qc
        /mriqc
    
    /image_analysis
    
        
    /image_processing
        /logs


```


Other things you will need to do
--------------------------------

There are a few other things that you will need to do in order to have a
fully functioning TICS study.

1. Copy or link the <study_name>_init.sh file to your $HOME/.tic
   directory.

2. Add the <study_name>_init.sh to your .zshrc file. The easiest way to
   do this is with this command

   ```
   source $TIC_INIT_PATH/<study_name>_init.sh
   ```

3. Create a BIDS protocol. You can see directions on how to do this in
   the BIDS app heudiconv. <need a link to the documentation here>

4. Add <study_name> to STUDY_CHOICES in $TIC_PATH/bin/study_switcher.py.
   You will also need to commit this change.


Creating a heudiconv protocol for the DICOM to NIFTI conversion
---------------------------------------------------------------

The first step in creating the heudiconv protocol is to have a set of
DICOM images from the study. These DICOM images may be stored in a
single directory, a parent directory with subdirectories, or a tarball.

You will scan these files with heudiconv to determine what images were
scanned in the protcol.

hdc_scan -d '{subject}.dicom.tar.gz' -s <subject_id>

hdc_scan is an alias created in TIC to run heudiconv on aging1a/2a. The
alias is

```
    >>> alias 'hdc_scan'

    hdc_scan='/usr/local/bin/singularity run -w \
    -B /cenc \
    -B /gandg \
    -B /bkraft1 $HDC_SINGULARITY_IMAGE \
    -f /cenc/software/heudiconv/hdc_convertall.py 
    -c none'
    
```

For example, you can run hdc_scan on a tarball

for example

```
   >>> ls *
   34P1081.dicom.tar.gz
   
   >>> hdc_scan -d '{subject}.dicom.tar.gz' -s 34P1081

```


This will scan the DICOM images and create a hidden directory,
.heudiconv, which contains information about the contents of the DICOM images.

```
    >>> cd ./.heudiconv/34P1081/info

    >>> ls -1 *
    34P1081.auto.txt
    34P1081.edit.txt
    convertall.py
    dicominfo.tsv
    dicominfo_with_header_.tsv
    filegroup.json
    hdc_convertall.py
```

The file dicominfo.tsv is a tab separated file containing 29 pieces of
information for each DICOM images acquired. Y

```
hdc_add_header dicominfo.tsv -v
              series_id           sequence_name           series_description  dim1  dim2  dim3  dim4     TR      TE  is_derived  is_motion_corrected
 0          2-sag_mprage            *tfl3d1_16ns                   sag_mprage   256   240   176     1  2.300    2.98       False                False
 1          3-sag_swi                *swi3d1r                   Mag_Images   192   192   128     1  0.047   25.00       False                False
 2          4-sag_swi                *swi3d1r                   Pha_Images   192   192   128     1  0.047   25.00       False                False
 3          5-sag_swi                *swi3d1r               mIP_Images(SW)   192   192   121     1  0.047   25.00       False                False
 4          6-sag_swi                *swi3d1r                   SWI_Images   192   192   128     1  0.047   25.00       False                False
 5          7-sag_t2tse              *spc_133ns                    sag_t2tse   256   240   176     1  3.200  222.00       False                False
 6          8-sag_t2flair            *spcir_133ns                  sag_t2flair   512   480   176     1  6.000  272.00       False                False
 7          9-ax_dki_P>>A             *ep_b1000#3                  ax_dki_P>>A    84   128    59    68  9.700  100.00       False                False
 8        10-ax_dki_P>>A             *ep_b0_2000              ax_dki_P>>A_ADC    84   128    59     1  9.700  100.00        True                False
 9        11-ax_dki_P>>A              *ep_b1000t           ax_dki_P>>A_TRACEW    84   128   118     1  9.700  100.00        True                False
10       12-ax_dki_P>>A             *ep_b0_2000               ax_dki_P>>A_FA    84   128    59     1  9.700  100.00        True                False
11       13-ax_dki_P>>A               Not found            ax_dki_P>>A_ColFA    84   128    59     1 -1.000   -1.00        True                False
... 
```


You will use the information in this file to create a BIDS protocol.  Your protocol will look something like this

```
import os

def create_key(template, outtype=('nii.gz','dicom'), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return (template, outtype, annotation_classes)


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group

    """

    t1 = create_key('anat/sub-{subject}_T1w')
    t2 = create_key('anat/sub-{subject}_T2w')
    rest = create_key('func/sub-{subject}_dir-{acq}_task-rest_run-{item:02d}_bold')

    fmap_rest = create_key('fmap/sub-{subject}_acq-func{acq}_dir-{dir}_run-{item:02d}_epi')

    info = {t1:[],
            t2:[],
            rest:[],
            fmap_rest:[],            
            }

    for idx, s in enumerate(seqinfo):

        if (s.dim3 == 208) and (s.dim4 == 1) and ('T1w' in s.protocol_name):
            info[t1] = [s.series_id]

        if (s.dim3 == 208) and ('T2w' in s.protocol_name):
            info[t2] = [s.series_id]

        if (s.dim4 >= 99) and (('dMRI_dir98_AP' in s.protocol_name) or ('dMRI_dir99_AP' in s.protocol_name)):
            acq = s.protocol_name.split('dMRI_')[1].split('_')[0] + 'AP'
            info[dwi].append({'item': s.series_id, 'acq': acq})

        ...

    return info
```

Once you have your protocol setup you will convert your study using this
protocol definition with the command hdc_convert

```

    >>> alias hdc_convert

    hdc_convert='/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 -c dcm2niix $HDC_SINGULARITY_IMAGE'


```

For example,


```

   >>> hdc_convert -d '{subject}.dicom.tar.gz' -s 34P1081 -o <outdir>
   
```


bkraft - I think this is an oversimplification now and should probably
be removed. We should just do this using hdc_convert. We could discuss
how someone could make their own alias for conversion.

At TIC we try to simplify things even further. If you have connected
your study to the ACTIVE_STUDY and you have downloaded the DICOM images
through a DICOM receiver that was created by Ricardo you can then just
type the command

```
    >>> hdc.sh 34P1081 1 
    
```
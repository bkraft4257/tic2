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

for example if the DICOM images were in a tarball called imove000.dicom.tar.gz
you can convert the DICOM images with a generic DICOM to NIFTI
conversion.

```
   >>> hdc_scan -d '{subject}.dicom.tar.gz' -s imove000 --ss 1
   
   where -s contains the subject_value and -ss is the session_value for
   the study.
      
```

**VERY IMPORTANT** - if you are using the zshrc you must include the
quotes around the -d parameter. If you leave out the quotes the zsh will
do automatic brace expansion and you will be kerfuffled.


If your data was exported from the BME PACS through a DICOM receiver you
will need to specify where the DICOM images are located and setup an
appropriate glob string. Images that are exported via a DICOM receiver
will be stored in the data structure as follows

```

    imove000
        /20180205
            /MR0001
            /MR0002
            /MR....
            
    DICOM images stored in each of the MR[0-9][0-9][0-9] subdirectories 
    with the extension DCM.
     
   when this is the data structure you can scan the directory for DICOM 
   images with this command
   
   >>> hdc_scan -d '{subject}/*/*/*.DCM' -s imove000 -ss 1 
  
```

**TIP 1** Your subject_value, in this example imove000, must be the
parent directory containing your DICOM images. If it is not (and it
won't be if you exported from BME PACS) you will need to rename the
directory.

**TIP 2** An easy way to determine the glob pattern is to do the
following to find the first DICOM image.

```
    >>> find imove000 -name "*.DCM" -print -quit
    
    imove000/20180205/MR0002/000150.DCM
    
```

you then just replace the above with '{subject}/*/*/*.DCM. You can also
use the bash script hdc_find_dcm to perform the same task

```
    >>> hdc_find_dcm imove000

    imove000/20180205/MR0002/000150.DCM
    
```

The hdc_scan file will scan the DICOM images and create a hidden
directory, .heudiconv in the current directory. This hidden directory
contains information about the contents of the DICOM images.

```
    >>> cd ./.heudiconv/imove/info

    >>> ls -1 *
    imove000.auto.txt
    imove000.edit.txt
    convertall.py
    dicominfo.tsv
    dicominfo_with_header_.tsv
    filegroup.json
    hdc_convertall.py
```

The file dicominfo.tsv is a tab separated file containing 25 pieces of
information for each DICOM images acquired. The 25 pieces of information
are listed here.

```

    >>> cd .heudiconv/imove000/info
    >>> hdc_add_header dicominfo_ses-1.tsv -o dicominfo_ses-1.csv
    >>> csvcut -n dicominfo_ses-1.csv

         1:
         2: total_files_till_now
         3: example_dcm_file
         4: series_id
         5: unspecified1
         6: unspecified2
         7: unspecified3
         8: dim1
         9: dim2
        10: dim3
        11: dim4
        12: TR
        13: TE
        14: protocol_name
        15: is_motion_corrected
        16: is_derived
        17: patient_id
        18: study_description
        19: referring_physician_name
        20: series_description
        21: sequence_name
        22: image_type
        23: accession_number
        24: patient_age
        25: patient_sex
        26: date

```

The fields created by HDC are written to a tsv file,
dicominfo_ses-1.tsv. HDC creates this file but it does not include any
header information. I have created a little script to add the header
information called hdc_add_header. You can then list the header
information with csvcut.

To obtain the values for each of the DICOM images you can use csvcut
with csvlook


```
>>> csvcut -c 4,21,8,9,10,12,13,15,16 dicominfo_ses-1.csv | csvlook

| series_id                                      | sequence_name | dim1 | dim2 | dim3 |    TR |     TE | is_motion_corrected | is_derived |
| ---------------------------------------------- | ------------- | ---- | ---- | ---- | ----- | ------ | ------------------- | ---------- |
| 2-MPRAGE_GRAPPA2                               | *tfl3d1_16ns  |  256 |  240 |  192 | 2.300 |   2.98 |               False |      False |
| 3-BOLD_resting 4X4X4 A>>P                      | *epfid2d1_64  |   64 |   64 |   35 | 2.000 |  25.00 |               False |      False |
| 4-rest_topup_A>>P                              | *epse2d1_64   |   64 |   64 |  140 | 2.400 |  38.00 |               False |      False |
| 5-rest_topup_P>>A                              | *epse2d1_64   |   64 |   64 |  140 | 2.400 |  38.00 |               False |      False |
| 6-Field_mapping 4X4X4 A>>P                     | *fm2d2r       |   64 |   64 |   35 | 0.488 |   4.92 |               False |      False |
| 7-Field_mapping 4X4X4 A>>P                     | *fm2d2r       |   64 |   64 |   35 | 0.488 |   7.38 |               False |      False |
| 8-mbep2d_bold 3mm L>>R                         | epfid2d1_64   |   72 |   64 |   64 | 0.570 |  30.00 |               False |      False |
| 9-mbep2d_bold 3mm L>>R                         | epfid2d1_64   |   72 |   64 |   64 | 0.570 |  30.00 |               False |      False |
| 10-mbep2d_bold 3mm R>>L (copy from bold L>>R)  | epfid2d1_64   |   72 |   64 |   64 | 0.570 |  30.00 |               False |      False |
| 11-mbep2d_bold 3mm R>>L (copy from bold L>>R)  | epfid2d1_64   |   72 |   64 |   64 | 0.570 |  30.00 |               False |      False |
| 12-T2 FLAIR SPACE NEW                          | *spcir_192ns  |  256 |  236 |  192 | 5.000 | 383.00 |               False |      False |
| 13-NODDI_DTI_120dir_12b0_AF4                   | epse2d1_128   |  128 |  128 |   80 | 3.500 | 106.00 |               False |      False |
| 14-NODDI_DTI_120dir_12b0_AF4                   | ep_b5#1       |  128 |  128 |   80 | 3.500 | 106.00 |               False |      False |
| 15-NODDI_DTI_120dir_12b0_AF4                   | ep_b5#1       |  128 |  128 |   80 | 3.500 | 106.00 |               False |      False |
| 16-NODDI_DTI_120dir_12b0_AF4 P>>A              | epse2d1_128   |  128 |  128 |   80 | 3.500 | 106.00 |               False |      False |
| 17-NODDI_DTI_120dir_12b0_AF4 P>>A              | ep_b5#1       |  128 |  128 |   80 | 3.500 | 106.00 |               False |      False |
| 18-NODDI_DTI_120dir_12b0_AF4 P>>A              | ep_b5#1       |  128 |  128 |   80 | 3.500 | 106.00 |               False |      False |
| 19-QSM_e6_p2_2mm                               | *swi3d6r      |  416 |  312 |  384 | 0.051 |  44.15 |               False |      False |
| 20-QSM_e6_p2_2mm                               | *swi3d6r      |  416 |  312 |  384 | 0.051 |  44.15 |               False |      False |
| 21-QSM_e6_p2_2mm                               | *swi3d6r      |  416 |  312 |  342 | 0.051 |  44.15 |               False |      False |
| 22-QSM_e6_p2_2mm                               | *swi3d6r      |  416 |  312 |  384 | 0.051 |  44.15 |               False |      False |
| 23-pcasl_wfu_4_0C R>>L EYES OPEN               | epfid2d1_56   |   70 |   56 |   43 | 4.000 |  11.00 |               False |      False |
| 24-pcasl_wfu_4_0C R>>L EYES OPEN               | epfid2d1_56   |   70 |   56 |   43 | 4.000 |  11.00 |               False |       True |
| 25-pcasl_wfu_4_0C L>>R (COPY SLICES FROM R>>L) | epfid2d1_56   |   70 |   56 |   43 | 4.000 |  11.00 |               False |      False |
| 26-pcasl_wfu_4_0C L>>R (COPY SLICES FROM R>>L) | epfid2d1_56   |   70 |   56 |   43 | 4.000 |  11.00 |               False |       True |

```

You will use the information in this file to create a BIDS protocol.
Your protocol will look something like this

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
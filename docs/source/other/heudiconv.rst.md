# Goal:

This page describes how to convert a set of DICOM images to NIFTI files in BIDS format using the NiPy tool heudiconv.  
[https://github.com/nipy/heudiconv](https://github.com/nipy/heudiconv)

# Quick Steps if you already have your hdc_study_protocol.py rules

    $ hdc_convert -d '{subject}/*/*/*.DCM' -f ./hdc_study_protocol.py -s <subject_id> -ss 1 -o <output_dir>

    You could simplify this even further by creating an alias for each study

# Quick Steps

https://github.com/theimagingcollective/nipype_workflows/wiki/DICOM-to-NIFTI-with-BIDS-directory-structure

1. Copy your HDC rules to your local directory. If you are starting from scratch then use (hdc_copy)
1. Find a DICOM image that you want to convert with hdc_find_dcm

      This step is only necessary to determine how deep your DICOM images reside.

      $ hdc_find_dcm <dirname>

         hfu66T1/20170821/MR0002/000150.DCM

1. Scan all DICOM images with HDC
    You may skip this step if you already have a set of heuristic rules to convert your DICOM images.

    $ hdc_scan -d '{subject}/*/*/*.DCM' -s <subject_id> -ss 1 -o output

1. Display DICOM information

    $ hdc_add_header output/.heudiconv/hfu66T1/info/dicominfo_ses-1.tsv

1. Create heuristic rules (if you haven't already done so.)

1. Convert DICOM to NIFTI files

    $ hdc_convert -d '{subject}/*/*/*.DCM' -f ./hdc_protocol.py -s <subject_id> -ss 1 -o output



# Background:

There are many tools that can convert DICOM files to NIFTI files (heudiconv, dcm2nii, unpacksdcmdir, etc.).  While the pros and cons of each tool can be debated, heudiconv will be used for our DICOM conversion. As an aside, many of us have found heudiconv is difficult to pronounce and remember for this reason we will refer to heudiconv as HDC (Heuristic DICOM Converter).  HDC will take a directory containing subdirectories and DICOM files and convert them to NIFTI format. HDC also has the option to output the data in BIDS format with JSON files created directly from the meta data in the DICOM files. HDC is an open-source NiPy tool. It is also distributed as a Docker container, which allows the easy distribution and use of HDC.  Craig has also converted the HDC Docker container to a singularity image so it can run on aging1a.

     In order to convert DICOM images with HDC you will need the following:
 
     1. HDC NiPy source code properly installed **OR**  Docker and the HDC Docker container, **OR** HDC singularity image 
     1. A set of DICOM images. These images can be contained with in a single directory, a directory containing subdirectories, or a tarball that contains the DICOM images.   
     1. A python module that describes the rules to describe which and how to convert DICOM images to NIFTI. 
 The HDC rules will be different for every study.  HDC also comes with a python module with a generic set of rules that will convert all of the DICOM images.

If you have been doing DICOM conversion with the dcm_convert bash scripts the process is very similar.  First you will scan the directory or tarball containing the DICOM images. The scanning reads the DICOM headers and creates a tab delimited text file about each DICOM files.  This information is then used to select which DICOM images will be converted.  What makes HDC superior to dcm_convert bash scripts is it can setup generic rules to based upon the information in the DICOM headers. This is different then dcm_convert (i.e. unpacksdcmdir) which needs a configuration file explicitly stating which DICOM images based upon Series number to convert.  For an established study it is expected that the rules will not change from subject to subject and you will be able to skip the scanning process all together.

HDC is also flexible enough that if you need to perform a very specific and unusual conversion then you can quickly write your own rules to convert exactly what you want into BIDS format.  At the moment, these rules are written as a Python module. I will describe how to do this later in the section call **Writing your own HDC Protcols**.

# Scanning your DICOM images

The first step in converting DICOM to NIFTI images is to determine what DICOM images are in your directory or tarball. This is done with the HDC command on aging1a as

/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 /cenc/software/heudiconv/nipy_heudiconv-2017-09-26-6bef64b746f6.img -f /cenc/software/heudiconv/hdc_convertall.py -c none -d "{subject}/*/*/*.DCM" -s **<subject_value>** -ss **<session_value>** -o **<output_dir>**

This command is long and arduous to type.  We have created an alias to simplify the process the alias is

alias hdc_scan='/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 /cenc/software/heudiconv/nipy_heudiconv-2017-09-26-6bef64b746f6.img -f /cenc/software/heudiconv/hdc_convertall.py -c none'

Notice that this alias fills in all the information except the parameters -d, -s, -ss, and -o.   These parameters will vary for each conversion and can not be specified before hand. A copy of the HDC help is at the bottom of this WIKI page.  I have copied the four parameters here for convenience.

  -d DICOM_DIR_TEMPLATE, --dicom_dir_template DICOM_DIR_TEMPLATE
                        location of dicomdir that can be indexed with subject
                        id {subject} and session {session}. Tarballs (can be
                        compressed) are supported in addition to directory.
                        All matching tarballs for a subject are extracted and
                        their content processed in a single pass

  -s [SUBJS [SUBJS ...]], --subjects [SUBJS [SUBJS ...]]
                        list of subjects. If not provided, DICOMS would first
                        be "sorted" and subject IDs deduced by the heuristic

  -ss SESSION, --ses SESSION
                        session for longitudinal study_sessions, default is
                        none

  -o OUTDIR, --outdir OUTDIR
                        output directory for conversion setup (for further
                        customization and future reference. This directory
                        will refer to non-anonymized subject IDs

As an example of how to scan a set of DICOM images exported from the PACS I will look at a specific example.  I have exported a set of DICOM images from the study with the Patient_Name of clbp01 and Patient_Id of clbp01.  When this exported from the PACS using a DICOM Receiver that Ricardo has setup  the DICOM images will be written to the specified directory of the DICOM Receiver in the directory <Patient_Name>_<Patient_ID>.  In my case, the data was written to the directory /bkraft1/dcm/incoming in the directory clbp01_clbp01.

Eventually, I would like to convert this to a BIDS format. The BIDS format stores the data (NIFTI images, JSON files, CSV files, etc) in a directory structure with a key-value pair. In this case the subject is clbp01 so eventually the data will be written to the directory sub-clbp01.  The sub is the key and the value is clbp01.  The value is essentially the acrostic that you will be using for your participant.  BIDS requires that only alphanumeric characters are uses [A-Z], [a-z], and [0-9]. No other characters may be used.

The first step in the conversion process is to rename the directory so the directory has subject in it's name.

hdc_scan -d '{subject}_{subject}/*/*/*.DCM' -s clbp01 -ss 1 -o /bkraft1/clbp/bids

This will scan the DICOM images and write out information about the DICOM images to the hidden directory .heudiconv in /bkraft1/clbp/bids

You can see what was written to the directory by going to /bkraft1/clbp/bids/.heudiconv/clbp01/info.

The file dicominfo_ses-1.tsv is a tab delimited file that contains information about each set of DICOM images it found. dicominfo_ses-1.tsv does not contain a header row.  I have written a simple function to add a header and dump out only a few of the columns for readability.

hdc_add_header dicominfo_ses-1.tsv -v -o dicominfo_ses-1.csv

This will add the header information and write the output to dicominfo_ses-1.csv. You can see a list of the headers with csvcut

 csvcut -n dicominfo_ses-1.csv
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

You can see a list of DICOM images with the command

csvcut -c series_id dicominfo_ses-1.csv| csvlook
| series_id                                    |
| -------------------------------------------- |
| 2-MPRAGE_GRAPPA2                             |
| 3-T2 FLAIR SPACE NEW                         |
| 4-mbep2d_bold 3mm L>>R                       |
| 5-mbep2d_bold 3mm L>>R                       |
| 6-mbep2d_bold 3mm R>>L (copy from bold L>>R) |
| 7-mbep2d_bold 3mm R>>L (copy from bold L>>R) |
| 8-pcasl_wfu_3_1 Rest 1ST                     |
| 9-pcasl_wfu_3_1 Rest 1ST                     |
| 10-pcasl_wfu_3_1 Rest 1ST                    |
| 11-pcasl_wfu_3_1 Rest 1ST                    |
| 12-pcasl_wfu_3_1 Rest 2ND                    |
| 13-pcasl_wfu_3_1 Rest 2ND                    |
| 14-pcasl_wfu_3_1 Rest 2ND                    |
| 15-pcasl_wfu_3_1 Rest 2ND                    |
| 16-pcasl_wfu_3_1 Pain 1ST                    |
| 17-pcasl_wfu_3_1 Pain 1ST                    |
| 18-pcasl_wfu_3_1 Pain 1ST                    |
| 19-pcasl_wfu_3_1 Pain 1ST                    |
| 20-pcasl_wfu_3_1 Pain 2ND                    |
| 21-pcasl_wfu_3_1 Pain 2ND                    |
| 22-pcasl_wfu_3_1 Pain 2ND                    |
| 23-pcasl_wfu_3_1 Pain 2ND                    |
| 24-mpcasl_wfu_3_1 8ph 1ST                    |
| 25-mpcasl_wfu_3_1 8ph 1ST                    |
| 26-mpcasl_wfu_3_1 8ph 1ST                    |
| 27-mpcasl_wfu_3_1 8ph 1ST                    |
| 28-mpcasl_wfu_3_1 8ph 2ND                    |
| 29-mpcasl_wfu_3_1 8ph 2ND                    |
| 30-mpcasl_wfu_3_1 8ph 2ND                    |
| 31-mpcasl_wfu_3_1 8ph 2ND                    |
| 32-mpcasl_wfu_3_1 8ph 3rd                    |
| 33-mpcasl_wfu_3_1 8ph 3rd                    |
| 34-mpcasl_wfu_3_1 8ph 3rd                    |
| 35-mpcasl_wfu_3_1 8ph 3rd                    |
| 36-mpcasl_wfu_3_1 8ph 4th                    |
| 37-mpcasl_wfu_3_1 8ph 4th                    |
| 38-mpcasl_wfu_3_1 8ph 4th                    |
| 39-mpcasl_wfu_3_1 8ph 4th                    |

The file <subject_value>_ses-<session_value>.edit.txt contains information about how the images will be converted.

cat clbp01_ses-1.edit.txt

{('run{item:03d}', ('nii.gz',), None): ['1-localizer',
                                        '2-MPRAGE_GRAPPA2',
                                        '3-T2 FLAIR SPACE NEW',
                                        '4-mbep2d_bold 3mm L>>R',
                                        '5-mbep2d_bold 3mm L>>R',
                                        '6-mbep2d_bold 3mm R>>L (copy from bold L>>R)',
                                        '7-mbep2d_bold 3mm R>>L (copy from bold L>>R)',
                                        '8-pcasl_wfu_3_1 Rest 1ST',
                                        '9-pcasl_wfu_3_1 Rest 1ST',
                                        '10-pcasl_wfu_3_1 Rest 1ST',
                                        '11-pcasl_wfu_3_1 Rest 1ST',
                                        '12-pcasl_wfu_3_1 Rest 2ND',
                                        '13-pcasl_wfu_3_1 Rest 2ND',
                                        '14-pcasl_wfu_3_1 Rest 2ND',
                                        '15-pcasl_wfu_3_1 Rest 2ND',
                                        '16-pcasl_wfu_3_1 Pain 1ST',
                                        '17-pcasl_wfu_3_1 Pain 1ST',
                                        '18-pcasl_wfu_3_1 Pain 1ST',
                                        '19-pcasl_wfu_3_1 Pain 1ST',
                                        '20-pcasl_wfu_3_1 Pain 2ND',
                                        '21-pcasl_wfu_3_1 Pain 2ND',
                                        '22-pcasl_wfu_3_1 Pain 2ND',
                                        '23-pcasl_wfu_3_1 Pain 2ND',
                                        '24-mpcasl_wfu_3_1 8ph 1ST',
                                        '25-mpcasl_wfu_3_1 8ph 1ST',
                                        '26-mpcasl_wfu_3_1 8ph 1ST',
                                        '27-mpcasl_wfu_3_1 8ph 1ST',
                                        '28-mpcasl_wfu_3_1 8ph 2ND',
                                        '29-mpcasl_wfu_3_1 8ph 2ND',
                                        '30-mpcasl_wfu_3_1 8ph 2ND',
                                        '31-mpcasl_wfu_3_1 8ph 2ND',
                                        '32-mpcasl_wfu_3_1 8ph 3rd',
                                        '33-mpcasl_wfu_3_1 8ph 3rd',
                                        '34-mpcasl_wfu_3_1 8ph 3rd',
                                        '35-mpcasl_wfu_3_1 8ph 3rd',
                                        '36-mpcasl_wfu_3_1 8ph 4th',
                                        '37-mpcasl_wfu_3_1 8ph 4th',
                                        '38-mpcasl_wfu_3_1 8ph 4th',
                                        '39-mpcasl_wfu_3_1 8ph 4th']}

You may edit this file to change what files are converted.


# Converting your DICOM images

After you have scanned your images you can convert them with the following command

hdc_scan -d '{subject}_{subject}/*/*/*.DCM' -s clbp01 -ss 1 -o /bkraft1/clbp/bids -c dcm2niix

This will convert the files as described in clbp01_ses-1.edit.txt.  It is unlikely that you would use this generic method of conversion for a study. The names of the NIFTI files are generically named.  We recommend for studies that you should define your own study protocol for conversion.  This process is relatively easy and only has to be done once.

# Writing your own HDC Protcols

This page will describe how to write the rules as a Python module.  Don't worry if you have never written any Python code before.  We have created a series of wrapper functions that have extended HDC from what is available on GITHUB that makes this process extremely easy.

Briefly the steps of writing the HDC python module with the rules you want to use is as simple as copying the template file that we have created for you. You then modify the data structures defined in the template.  Here is an example of the data structure, criteria, that you will need to modify

   sequences['t1w'] = criteria(bids_destination='sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w',
                                series_description='MPRAGE_GRAPPA2',  
                                sequence_name='tfl3d1_16ns',
                                dim1 = [256, 256],  
                                dim2 = [240, 240],  
                                dim3 = [192, 192],  
                                dim4 = [1, 1],  
                                TR = [2.300, 2.300],  
                                TE = [2.98, 2.98],  
                                is_derived = False,  
                                )

I will go in more detail about the contents of the data structure later. However, for now the most important aspects of the data structure is a Python namedtuple called criteria that we have defined.  The namedtuple functions similarly to a Python dictionary with key/value pairs. In the namedtuple, criteria, the keys are before the equal sign and the values are after it.  HDC defines 25 different fields in the DICOM header (keys) that you can use to select which DICOM images you want to convert to NIFTI.  In addition, we have also defined the HDC key, called bids_destination, that defines where the converted DICOM file will reside in the BIDS directory structure.

There are three types of keys in the namedtuple criteria that you may define: a numeric, string/regexp, and boolean criteria.  A **numeric criteria** is any key that is an integer or float.  The value for a numeric key are the acceptable limits of this key.  For example, if you are expecting an DICOM image to contain 192 slices +/- 3 slices you could set the dim3 key value to be [189,195].

dim3 = [189, 195]

If this was your only criteria for converting DICOM images to NIFTY images, this would convert any DICOM images in your data set that had a number of slices greater than or equal to 189 slices and less than or equal to 195 slices.  If you  wanted to be very specific and only wanted to convert DICOM images with just 192 slices you would set the minimum and maximum range equal to each other dim3 = [192, 192].

A **string/regexp** criteria are used for the keys that contain strings.  In the simplest case if you just wanted to know if the DICOM field contained a specific string  you just set the value of the key to the string you are searching for. For example, the DICOM field Series Description contains the series description of the images acquired on the scanner. For the HFPEF protocol the T1 weighted image contains MPRAGE_GRAPPA2 in the series description.  If I only wanted to convert the T1 weighted DICOM images I can set the value of the key series_description to "MPRAGE_GRAPPA2".

series_description='MPRAGE_GRAPPA2'

This was my only rule it would convert all DICOM images with the MPRAGE_GRAPPA2 in the series description.  The string I search for is case sensitive so if I just paste it in as a simple string it needs to match what is in the DICOM field exactly.   However, instead of just searching for simple strings we have enabled these strings to be regexp. This enables a user to search for very specific strings in the DICOM fields.

The third type of criteria a user can specify is the **boolean** criteria. The boolean criteria is a simple True or False condition that HDC defines in the namedtuple. For example, when images are acquired on the Siemens scanner the images will be saved to the DICOM database. Depending upon the type of sequence acquired additional images may also be written to the DICOM database.  For example, when a DTI image is acquired the raw images are saved but also FA image, ADC image, and color FA image. These images are calculated from the raw DICOM images acquired. HDC calls these images derived images. There is a criteria key called _is_derived that is a boolean criteria that labels each of the DICOM images as a derived image when the _is_derived key is set to True.  If you wanted to convert all of the raw images in the DICOM database you can set the _is_derived criteria to False.

is_derived = False

When this flag is set only the DICOM images that are acquired and not calculated will be converted.

The criteria that you define for each sequence that you want to convert are combined with the AND operator. That is if you wanted to be very specific about what images you convert you can combine these criteria and all of the criteria would need to be True if the DICOM images are going to be converted to NIFTI format.   For example, if you wanted to only convert the original T1 weighted image acquired on the HFPE scanner with exactly 192 slices you would set your sequence criteria in the Python module to

  sequences['t1w'] = criteria(bids_destination='sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w',  
                                series_description='MPRAGE_GRAPPA2',  
                                dim3 = [192, 192],  
                                is_derived = False,  
                                )

You can see that specifying the criteria like this is very easy and can be very specific.  The next challenge is how to know what criteria to use to only convert the images that you want.  I will explain this in the Step by Step Instruction below.


# Step by Step Instructions to convert DICOM images to NIFTI:

These instructions are going to assume that you are logged into aging1a, that your data is accessible to aging1a, and that you will be running HDC via the singularity image that Craig created.

## 1) Scan your DICOM images

I am going to assume that you know the contents of your imaging protocol (T1w, T2Flair, perfusion, DTI, etc.) and what you want to convert but not the specific details (number of slices, TE, TR, etc.) that you could use to selectively convert your DICOM images to NIFTI.  If this is the case then you need to scan your DICOM images to extract the details by scanning your DICOM images.

To scan your DICOM images on aging1a we will be using a singularity image that Craig created specifically for aging1a.  When he creates a singularity image he specifically tells it what data directories to include in the image.   The singularity image he has created includes /cenc, /gandg, and /bkraft1.  If your data is not contained in one of these directories this process won't work. If this is the case please contact Craig Hamilton about rebuilding the singularity image.

The command that you will run in your aging1a terminal is

/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 /cenc/software/heudiconv/nipy_heudiconv-2017-09-26-6bef64b746f6.img -d '{subject}*.tar*' -s 34P1029 -f heudiconv_convertall.py -c none -ss 1 -o output

You can see that this command is rather long and tedious to type.  To simplify the process we have created an alias in the TIC environment called hdc. This alias defines hdc as

alias hdc='/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 /cenc/software/heudiconv/nipy_heudiconv-2017-09-26-6bef64b746f6.img'

and allows you to replace the above command as

hdc -d '{subject}*.tar*' -s 34P1029 -f heudiconv_convertall.py -c none -ss 1 -o output

For the moment, I will ignore the details of the alias hdc and focus on the parameters that you need to pass into hdc.  First and foremost all of the parameters passed into hdc are directly from the heudiconv.py code. You can access the help for heudiconv.py by passing in the -h command (see the end of this Wiki for details).

The options used above are the most common options for HDC.

**-d <dicom_dir_template> is the DICOM_DIR_TEMPLATE that describes the location of dicomdir that can be indexed with subject id {subject} and session {session}. Tarballs and compressed tarballs are also supported in addition to directory. All matching tarballs for a subject are extracted and their content processed in a single pass.  **VERY IMPORTANT** if you are using the Z-shell with brace expansion turned on you must put the -d argument in quotes.  Failure to do so will result in the following error

zsh: no matches found: /data/{subject}*tar*

Your DICOM_DIR_TEMPLATE must contain a subject ID in it. This can either be in name of the directory or subdirectories or in the name of the tarball.  If your DICOM_DIR_TEMPLATE does not contain {subject} you will encounter a Python ValueError.

**-s <subject_id>**  is the subject ID that will be used to convert your data to BIDS format.  BIDS requires a subject ID. BIDS also requires that the subject ID only contains letters and numbers.

**-ss <session_id>** is the session ID.  The session ID, like the subject ID, must only contain letters and numbers. However, unlike the subject id it is optional.  The session ID does not have to be in your DICOM_DIR_TEMPLATE.

**-o** is the location of your output directory.  It may be a relative or absolute path.

**-f** <python_module> is the Python module that contains the heuristic rules for selecting which DICOM images will be converted to NIFTI.  Even if you are only scanning the DICOM images you must provide a Python module with heuristic rules.  HDC provides a generic set of heuristic rules for scanning all of the DICOM images.  This file name is called heudiconv_convertall.py.

**-c** <method> is the flag that tells HDC to either convert the selected DICOM images (dcm2niix) or scan the DICOM header (none).

**To Scan Your DICOM files issue this command **

hdc -d '{subject}*.tar*' -s 34P1029 -f heudiconv_convertall.py -c none -ss 1 -o output

the -c none tells HDC that we only want to scan the DICOM directories and not actually do the conversion.

Once you have scanned all the files you want to read the dicominfo.tsv file.  This file is located in the output directory that you specified here output/.heudiconv/{subject}/info/dicominfo.tsv.  If you specify a session while scanning -ss or --ses then the session number will be included in the dicominfo file such that dicominfo_ses-{session}.tsv   Unfortunately, the dicominfo.tsv file does not contain a header row. I have created  a helper function, heudiconv_add_header.py to add the header row and convert the TSV file into a CSV file.

This helper function has been aliased in the TIC environment to

alias hdc_add_header='/cenc/software/heudiconv/heudiconv_add_header.py'

You can add a header with the command

hdc_add_header <dicominfo_tsv_filename>

This will write the contents of dicominfo_tsv_filename to the file dicominfo.csv in the current directory. You have the option via the command line flag --csv_filename to change the name and location where the file is written.

Once you have the dicominfo.csv file it is easy to view and parse this file with csvcut and csvlook.  These tools have been installed on aging1a and are part of the csvkit toolkit. If you are not familiar with these tools you can find more information about them here [http://csvkit.readthedocs.io/en/1.0.2/](http://csvkit.readthedocs.io/en/1.0.2/)

The list of headers add are
  1: total_files_till_now  range
  2: example_dcm_file      (regex)
  3: series_id             (series_id  integer series number )
  4: unspecified1          (regex dicom directory)
  5: unspecified2          (regex)
  6: unspecified3          (regex)
  7: dim1                  (range)
  8: dim2                  (range)
  9: dim3                  (range)
 10: dim4                  (range)
 11: TR                    (range)
 12: TE                    (range)
 13: protocol_name         (regexp)
 14: is_motion_corrected   (boolean)
 15: is_derived            (boolean)
 16: patient_id            (regexp)
 17: study_description     (regexp)
 18: referring_physician_name  (regexp)
 19: series_description     (regexp)
 20: sequence_name  (regexp)
 21: image_type  (regexp)
 22: accession_number (regexp)
 23: patient_age (regexp)
 24: patient_sex (regexp)
 25: date (regexp)

An easy way to look at the contents of the CSV file you just created is with csvcut and csvlook
These headers match the fields you may search for in the

csvcut -c 17,4,20,21,8,9,10,11,12,13,15 dicominfo.csv | csvlook

I have created the alias hdc_csvlook for the above command.  Please note that this alias assumes that the dicominfo.csv exists in the current directory. This assumption can not be a

# Help from heudiconv.py

The help for heudiconv.py can be accessed by passing in the -h flag at the command line.  Here is the help of heudiconv.py for your convenience

usage: heudiconv [-h] [--version] [-d DICOM_DIR_TEMPLATE]
                 [-s [SUBJS [SUBJS ...]]] [-c {dcm2niix,none}] [-o OUTDIR]
                 [-a CONV_OUTDIR] [--anon-cmd ANON_CMD] -f HEURISTIC_FILE
                 [-q QUEUE] [-p] [-ss SESSION] [-b] [--overwrite] [--datalad]
                 [--dbg] [--command {treat-json,ls,populate-templates}]
                 [-g {studyUID,accession_number}] [--minmeta]
                 [files [files ...]]

Convert DICOM dirs based on heuristic info This script uses the dcmstack
package and dcm2niix tool to convert DICOM directories or tarballs into
collections of NIfTI files following pre-defined heuristic(s). It has multiple
modes of operation - If subject ID(s) is specified, it proceeds by extracting
dicominfo from each subject and writing a config file
$subject_id/$subject_id.auto.txt in the output directory. Users can create a
copy of the file called $subject_id.edit.txt and modify it to change the files
that are converted. This edited file will always overwrite the original file.
If there is a need to revert to original state, please delete this edit.txt
file and rerun the conversion - If no subject specified, all files under
specified directory are scanned, DICOMs are sorted based on study UID, and
layed out using specified heuristic Example: heudiconv -d rawdata/{subject} -o
. -f heuristic.py -s s1 s2 s3

positional arguments:
  files                 files (tarballs, dicoms) or directories containing
                        files to process. Specify one of the
                        --dicom_dir_template or files not both

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -d DICOM_DIR_TEMPLATE, --dicom_dir_template DICOM_DIR_TEMPLATE
                        location of dicomdir that can be indexed with subject
                        id {subject} and session {session}. Tarballs (can be
                        compressed) are supported in addition to directory.
                        All matching tarballs for a subject are extracted and
                        their content processed in a single pass
  -s [SUBJS [SUBJS ...]], --subjects [SUBJS [SUBJS ...]]
                        list of subjects. If not provided, DICOMS would first
                        be "sorted" and subject IDs deduced by the heuristic
  -c {dcm2niix,none}, --converter {dcm2niix,none}
                        tool to use for dicom conversion. Setting to "none"
                        disables the actual conversion step -- useful for
                        testing heuristics.
  -o OUTDIR, --outdir OUTDIR
                        output directory for conversion setup (for further
                        customization and future reference. This directory
                        will refer to non-anonymized subject IDs
  -a CONV_OUTDIR, --conv-outdir CONV_OUTDIR
                        output directory for converted files. By default this
                        is identical to --outdir. This option is most useful
                        in combination with --anon-cmd
  --anon-cmd ANON_CMD   command to run to convert subject IDs used for DICOMs
                        to anonymmized IDs. Such command must take a single
                        argument and return a single anonymized ID. Also see
                        --conv-outdir
  -f HEURISTIC_FILE, --heuristic HEURISTIC_FILE
                        python script containing heuristic
  -q QUEUE, --queue QUEUE
                        select batch system to submit jobs to instead of
                        running the conversion serially
  -p, --with-prov       Store additional provenance information. Requires
                        python-rdflib.
  -ss SESSION, --ses SESSION
                        session for longitudinal study_sessions, default is
                        none
  -b, --bids            flag for output into BIDS structure
  --overwrite           flag to allow overwrite existing files
  --datalad             Store the entire collection as DataLad dataset(s).
                        Small files will be committed directly to git, while
                        large to annex. New version (6) of annex repositories
                        will be used in a "thin" mode so it would look to
                        mortals as just any other regular directory (i.e. no
                        symlinks to under .git/annex). For now just for BIDS
                        mode.
  --dbg                 do not catch exceptions and show exception traceback
  --command {treat-json,ls,populate-templates}
                        custom actions to be performed on provided files
                        instead of regular operation.
  -g {studyUID,accession_number}, --grouping {studyUID,accession_number}
                        How to group dicoms (default: by studyUID)
  --minmeta             Exclude dcmstack's meta information in sidecar jsons

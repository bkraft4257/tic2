#!/bin/python

import argparse
import glob


subject_id=${1}
session_id=${2-1}

subject=sub-${subject_id}
session=ses-${session_id}

conn_input=${ACTIVE_CONN_PATH}/

bold_mni_preproc=$ACTIVE_CONN_PATH/${subject}/${session}/func/${subject}_${session}_task-rest_acq-epi_rec-fmap_bold_space-MNI152NLin2009cAsym_preproc.nii.gz

t1w_gm_probtissue=$ACTIVE_CONN_PATH/${subject}/${session}/anat/${subject}_${session}_T1w_class-GM_probtissue.nii.gz
t1w_wm_probtissue=$ACTIVE_CONN_PATH/${subject}/${session}/anat/${subject}_${session}_T1w_class-WM_probtissue.nii.gz
t1w_csf_probtissue=$ACTIVE_CONN_PATH/${subject}/${session}/anat/${subject}_${session}_T1w_class-CSF_probtissue.nii.gz

ln -f ${bold_mni_preproc} ${conn_input}

ln -f ${t1w_gm_probtissue} ${conn_input}
ln -f ${t1w_wm_probtissue} ${conn_input}
ln -f ${t1w_gm_probtissue} ${conn_input}

cd ${conn_input}
echo 
pwd
echo
ls
echo




def _argparse():
    """
    Copy files from fmriprep and netprep for CONN.
    """

    parser = argparse.ArgumentParser(prog='study_switcher')


    usage = 'usage: %prog [options] arg1 arg2'

    parser = argparse.ArgumentParser(prog='heudiconv_add_header')

    # parser.add_argument('tsv_filename', help='DICOM TSV info file created the heurdiconv.py')

    parser.add_argument('-s', '--subject', help='Participant Label', default=ACTIVE_ACROSTIC_REGEX)
    parser.add_argument('-ss', '--session', help='Session Label', default=1)


    parser.add_argument('study',
                        help='Switch to a different study.',
                        choices=STUDY_CHOICES,
                        type=str,
                        default=None,
                        )

    parser.add_argument("-d", "--default", help="Set selected study as default.",
                        action="store_true",
                        default=False)

    parser.add_argument("-v", "--verbose", help="Display contents of study_switcher output_file.",
                        action="store_true",
                        default=False)

    return parser.parse_args()


def _select_output_file(default_flag):

    if default_flag:
        output_file = DEFAULT_STUDY_SWITCHER_OUTPUT_FILENAME;
    else:
        output_file = STUDY_SWITCHER_OUTPUT_FILENAME;

    return output_file


def main():

    in_args = _argparse()

    output_filename = _select_output_file(in_args.default)

    if in_args.study is not None:
        _write_study_switcher_script(in_args.study,
                                     output_filename)

    if in_args.verbose or in_args.study is None:

        print(f'\n\n>> cat {output_filename} .... \n\n')

        with open(output_filename, 'r') as file:
            print(file.read())

    return


# ====================================================================================================================
# region Command Line Interface

if __name__ == '__main__':
    sys.exit(main())

# endregion
# Heuristic DICOM Converter (HDC)

### TypeError: 'NoneType' object is not iterable

If you see this error it means that your -d option is not set properly. For

```
>> hdc_scan -s mcf901 -ss 1

        INFO: Running heudiconv version 0.5.dev1
        Traceback (most recent call last):
          File "/opt/conda/envs/neuro/bin/heudiconv", line 11, in <module>
            load_entry_point('heudiconv==0.5.dev1', 'console_scripts', 'heudiconv')()
          File "/opt/conda/envs/neuro/lib/python2.7/site-packages/heudiconv/cli/run.py", line 120, in main
            process_args(args)
          File "/opt/conda/envs/neuro/lib/python2.7/site-packages/heudiconv/cli/run.py", line 244, in process_args
            args.subjs, grouping=args.grouping)
          File "/opt/conda/envs/neuro/lib/python2.7/site-packages/heudiconv/parser.py", line 155, in get_study_sessions
            for f in files_opt:
        TypeError: 'NoneType' object is not iterable
```

The alias hdc_scan is

```
hdc_scan='/usr/local/bin/singularity run -w -B /cenc -B /gandg -B /bkraft1 \
                   $HDC_SINGULARITY_IMAGE -f $TIC_PATH/studies/_new_study_template/hdc_convertall.py -c none'

```

The -d option is not set.  A standard pattern after being exported from BMEPACS via a DICOM receiver that Ricardo has setup is
{subject}/2*/*/*.DCM.  If you are using the zsh remember to put this quotes.
# BIDS Validator

On aging1a bids-validator is located here /usr/local/bin/bids-validator.
It may be accessed with the command bids-validator.

## Goal

The bids_validator checks that your data is BIDS compliant and allows
other data processing applications to be easily applied to the data. You
may find other BIDS apps at http://bids-apps.neuroimaging.io/



## bids_validator -h

Usage: bids-validator <dataset_directory> [options]

Options:
  --help, -h            Show help                                      [boolean]
  --version, -v         Show version number                            [boolean]
  --ignoreWarnings      disregard non-critical issues                  [boolean]
  --ignoreNiftiHeaders  disregard NIfTI header content during validation
                                                                       [boolean]
  --verbose             Log more extensive information about issues.   [boolean]
  --config, -c          Optional configuration file. See
                        https://github.com/INCF/bids-validator for more info.

This tool checks if a dataset in a given directory is compatible with the Brain
Imaging Data Structure specification. To learn more about Brain Imaging Data
Structure visit http://bids.neuroimaging.io
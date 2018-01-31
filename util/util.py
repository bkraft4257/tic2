#!/aging1/software/anaconda/bin/python
"""
"""

import os  # system functions
import subprocess
import arrow
from datetime  import datetime, strftime


def tic_subprocess(callCommand,
                   verbose_flag=False,
                   debug_flag=False,
                   nohup_flag=False,
                   wait_flag=True):

    iiDateTime = datetime.datetime.now()
    timeStamp = iiDateTime.strftime('%Y%m%d%H%M%S')

    callCommand = list(map(str, callCommand))

    if nohup_flag:

        if debug_flag:
            print('Timestamp: %s ' % timeStamp)

        callCommand = ["nohup"] + callCommand

        stdout_log_file = 'nohup.stdout.' + timeStamp + '.log'
        stderr_log_file = 'nohup.stderr.' + timeStamp + '.log'

        if verbose_flag or debug_flag:
            print(' ')
            print(' '.join(callCommand))
            print(stdout_log_file)
            print(' ')

        # http://stackoverflow.com/questions/6011235/run-a-program-from-python-and-have-it-continue-to-run-after-the-script-is-kille

        subprocess.Popen(callCommand,
                         stdout=open(stdout_log_file, 'w'),
                         stderr=open(stderr_log_file, 'w'),
                         preexec_fn=os.setpgrp,
                         )

        if verbose_flag or debug_flag:
            print(' ')

    else:

        if verbose_flag:
            print(' ')
            print(' '.join(callCommand))
            print(' ')

        pipe = subprocess.Popen(callCommand, stdout=subprocess.PIPE)

        if wait_flag:
            pipe.wait()

        if debug_flag:
            output = pipe.communicate()[0]
            print(' ')
            print(output)
            print(' ')

    return

def freeview(fileList, display_flag=True, verbose_flag=False):
    freeviewCommand = "freeview "

    for ii in fileList:

        if (ii[0] != None) and os.path.isfile(ii[0]):

            if ((ii[0].endswith(".nii.gz") or ii[0].endswith(".nii")) and
                    (ii[1] != None)):
                freeviewCommand = freeviewCommand + " " + str(ii[0]) + str(ii[1])

    if display_flag:
        DEVNULL = open(os.devnull, 'wb')
        pipe = subprocess.Popen([freeviewCommand], shell=True,
                                stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL, close_fds=True)


def fslview(fileList, verbose_flag=False):
    for ii in fileList:

        if os.path.isfile(ii):

            if (ii.endswith(".nii.gz") or ii.endswith(".nii")):

                fslviewCommand = ['fslview', str(ii)]

                if verbose_flag:
                    print(fslviewCommand)

                DEVNULL = open(os.devnull, 'wb')
                pipe = subprocess.Popen(fslviewCommand, shell=True,
                                        stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL, close_fds=True)

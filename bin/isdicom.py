#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
"""

import sys


def isdcm(filename):
    # when importing isdicom.py, it is a module, so __name__ is isdicom
    #  this is the 'enclosing namespace'
    #  we need to call it as 'isdicom.isdcm("filename"), from the python shell,
    #  since it is in the  namespace "isdicom".  You can't call a module from
    # the python command line.  It gets "executed" when it is imported, and
    #  we don't want the execution to occur on import, only when calling the
    #  function within it (as isdicom.isdcm()).  The __main__ check below
    #  prevents execution on import, only executing when called from the bash
    #  shell with sys.argv being supplied by bash.

    #  when calling from the shell, treating isdicom as a function, the namespace
    #  is __main__, so the code at the bottom is executed,

    #    print('isdicm:  __name__ is',__name__)
    #    print('filename is',filename)

    marker = b"    "

    with open(filename, "rb") as fp:
        fp.seek(0x80)
        marker = fp.read(4)

    if marker == b"DICM":
        #        print('True')
        return True
    else:
        return False


if __name__ == "__main__":
    # when using isdicom.py from the bash shell, as a module, the
    #  namespace is __main__
    #  it is called as:
    #      $ python isdicom 000001.DCM
    #
    #  if we call it from the python shell as:
    #     >>> isdicom("000001.DCM")
    #  we get the error "TypeError: 'module' object is not callable
    #

    #    print('main:  __name__ is',__name__)

    #    print('argv1 is',sys.argv[1])

    isIt = isdcm(sys.argv[1])

    print(isIt)
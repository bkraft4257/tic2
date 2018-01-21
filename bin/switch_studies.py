#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__version__ = "0.0.0"


import os

env_variable='STUDY_IMAGE_PROCESSING'

print(os.getenv(env_variable))
os.environ[env_variable] = 'TEST'
print(os.getenv(env_variable))


env_variable='STUDY_IMAGE_PROCESSING_2'
print(os.getenv(env_variable))
os.putenv("VARIABLE", "123")
print(os.getenv(env_variable))

#! /usr/bin/env python

"""
add root dir to sys.path
"""

import sys
import os


def add_sys_path():
    dirname = os.path.dirname(__file__)
    abs_dirpath = os.path.abspath(dirname)
    root_path = os.path.abspath(os.path.join(
        abs_dirpath, '../../'
    ))
    sys.path.insert(0, root_path)

add_sys_path()

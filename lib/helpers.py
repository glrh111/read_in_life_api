#! /usr/bin/env python
# coding: utf-8

import os
import sys

def get_root_path():
    dirname = os.path.dirname(__file__)
    abs_dirpath = os.path.abspath(dirname)
    root_path = os.path.abspath(os.path.join(
        abs_dirpath, '../'
    ))
    return root_path

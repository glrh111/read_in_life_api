#! /usr/bin/env python
# coding: utf-8

import os
import sys
import string
import time

def get_root_path():
    dirname = os.path.dirname(__file__)
    abs_dirpath = os.path.abspath(dirname)
    root_path = os.path.abspath(os.path.join(
        abs_dirpath, '../'
    ))
    return root_path


def validator_f_str_min_length(length=6):
    def wocao(value):
        return len(value) >= length, 'value length should bigger than {}'.format(length)
    return wocao


def validator_f_str_in_sequence(char_str):
    def wocao(value):
        available = all(
            map(
                lambda x: x in char_str,
                value
            )
        )
        return available, 'value alphabet should be {}'.format(char_str)
    return wocao


def validator_str_is_number_or_a_to_z_or_punctuation(value):
    """if a-zA-Z0-9!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    return validator_f_str_in_sequence(
        string.lowercase + string.uppercase + string.digits + string.punctuation
    )(value)


def validator_str_is_number_or_a_to_z(value):
    """if a-zA-Z0-9"""
    return validator_f_str_in_sequence(
        string.lowercase + string.uppercase + string.digits
    )(value)


def check_field_available(value, validator_list):
    """check field
     usage:

         available, msg = check_field_available('dddddd', [
            validator_f_str_min_length(6),
            validator_str_in_sequence('abcd')
        ])

    """
    available, msg = True, ''
    for f in validator_list:
        available, msg = f(value)
        if not available:
            break

    return available, msg if not available else ''


def timestamp_by_13():
    return int(time.time() * 1000)


if __name__ == '__main__':
    print validator_f_str_in_sequence('abcdef#')('def#$')

    print check_field_available('dddddd', [
        validator_f_str_min_length(6),
        validator_f_str_in_sequence('abcd')
    ])
#!/usr/bin/env python3

'''
h1b/util.py

Share utilities for the DPH project.
created: APR 2018
'''

from pathlib import Path
from os import environ as env

PRIMARY = 'h1b_kaggle.csv'


def datapath(fname=PRIMARY):
    '''
    Return the primary dataset according to H1B_DATA env variable and the
    primary data file name.
    '''
    return Path(env.get('H1B_DATA', './data')) / fname


def first_n_lines(n, fs):
    '''
    Yield the first `n' lines of filestream `fs' (really, yeild the first `n'
    items in iterable `fs').
    '''
    for _ in range(n):
        yield next(fs)

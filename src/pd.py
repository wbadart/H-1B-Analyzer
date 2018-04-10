#!/usr/bin/env python3

'''
src/pd.py

Utilities for reading in raw data into pandas data frames.

- Elvis Yu
- Luke Duane
- Will Badart
created: MAR 2018
'''

from pandas import read_csv
from pathlib import Path

KAGGLE_CATEGORICALS = {
    'CASE_STATUS',
    'EMPLOYER_NAME',
    'SOC_NAME',
    'JOB_TITLE',
    'WORKSITE',
}


def from_kaggle(path=Path('data/h1b_kaggle.csv')):
    '''Get the kaggle data as data frame.'''
    df = read_csv(path, index_col=0)
    for categorical in KAGGLE_CATEGORICALS:
        df[categorical] = df[categorical].astype('category')
    df.FULL_TIME_POSITION = df.FULL_TIME_POSITION.apply(lambda x: x == 'Y')
    return df

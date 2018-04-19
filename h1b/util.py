#!/usr/bin/env python3

'''
h1b/util.py

Share utilities for the DPH project.
created: APR 2018
'''

import pandas as pd
from pathlib import Path
from os import environ as env

CATEGORICAL_COLUMNS = {
    'CASE_STATUS', 'EMPLOYER_NAME', 'SOC_NAME', 'JOB_TITLE', 'WORKSITE'}
PRIMARY = 'h1b_kaggle.csv'


def datapath(fname=PRIMARY):
    '''
    Return the primary dataset according to H1B_DATA env variable and the
    primary data file name.
    '''
    return (Path(env.get('H1B_DATA', './data')) / fname).resolve()


def load_dataframe(fname=PRIMARY):
    '''
    Load the primary dataset into a DataFrame, format the individual Series
    according to domain knowledge, and return the frame.
    '''
    df = pd.read_csv(datapath(fname)).drop(['Unnamed: 0'], axis=1)
    for categorical in CATEGORICAL_COLUMNS:
        df[categorical] = df[categorical].astype('category')
    df.FULL_TIME_POSITION = df.FULL_TIME_POSITION == 'Y'
    return df

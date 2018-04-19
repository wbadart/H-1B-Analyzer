#!/usr/bin/env python3

'''
h1b/description2.py

Generate descriptive statistics over the primary dataset.
created: MAR 2018
'''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from .util import datapath, PRIMARY

SEP = '=' * 20

PLOTS = ['employers', 'salary', 'year']
STATS = ['totals', 'salary', 'employers', 'positions', 'year']

pd.options.display.float_format = '{:,.2f}'.format


def reject_outliers(data, m=2):
    '''
    https://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list#16562028
    '''
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / mdev if mdev else 0.
    return data[s < m]


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-f', '--file', default=PRIMARY,
                        help='location of dataset w/in data directory '
                        '(default:{})'.format(PRIMARY))
    parser.add_argument('-s', '--stats', choices=STATS, nargs='+', default=[],
                        help='statistics to generate')
    parser.add_argument('-p', '--plots', choices=PLOTS, nargs='+', default=[],
                        help='plots to generate')
    parser.add_argument('--allstats', action='store_true',
                        help='generate all statistics (overrides -s)')
    parser.add_argument('--allplots', action='store_true',
                        help='generate all plots (overrides -p)')
    args = parser.parse_args()
    df = pd.read_csv(datapath(args.file)).drop(['Unnamed: 0'], axis=1)

    # =========
    # Do stats
    # =========

    if 'totals' in args.stats or args.allstats:
        print('TOTAL ROWS: {:,}'.format(df.shape[0]))
        print('MISSING DATA PER COLUMN:')
        print(df.isnull().sum())
        print(SEP)

    if 'salary' in args.stats or args.allstats:
        print('SALARY DESCRIPTION:')
        print(df.PREVAILING_WAGE.describe())
        print('WITHOUT OUTLIERS:')
        print(reject_outliers(df.PREVAILING_WAGE.dropna()).describe())
        print(SEP)

    if 'employers' in args.stats or args.allstats:
        print('TOP EMPLOYERS:')
        print(df.EMPLOYER_NAME
                .value_counts()
                .sort_values(ascending=False)
                .head(5))
        print(SEP)

    if 'positions' in args.stats or args.allstats:
        print('TOP JOB TITLES:')
        print(df.JOB_TITLE.value_counts().sort_values(ascending=False).head(5))
        print(SEP)

    if 'year' in args.stats or args.allstats:
        print('APPLICATIONS BY YEAR:')
        print(df.YEAR.value_counts())
        print(SEP)

    # =========
    # Do plots
    # =========

    if 'employers' in args.plots or args.allplots:
        df.EMPLOYER_NAME \
            .value_counts() \
            .sort_values(ascending=False) \
            .head(5) \
            .sort_values() \
            .plot(kind='barh',
                  title='Top 5 Employers Overall by Application Volume')
        plt.show()

    if 'salary' in args.plots or args.allplots:
        plt.title('Overall Distribution of Salaries')
        reject_outliers(df.PREVAILING_WAGE.dropna()).hist(bins=20)
        plt.show()

    if 'year' in args.plots or args.allplots:
        df.YEAR.value_counts().plot(kind='bar')
        plt.show()


if __name__ == '__main__':
    from sys import exit
    exit(main())

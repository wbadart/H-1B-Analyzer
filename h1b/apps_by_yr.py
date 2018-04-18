#!/usr/bin/env python3

'''
src/apps_by_yr.py

Show volume of applications by year.

- Elvis Yu
- Luke Duane
- Will Badart
created: MAR 2018
'''

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter as FMT
from collections import Counter
from csv import reader


def main():
    plt.title('H-1B Applications by Year')
    plt.xlabel('Year')
    plt.ylabel('# Applications')

    with open('data/h1b_kaggle.csv') as fs:
        r = reader(fs)
        next(r)
        counts = Counter(tup[7] for tup in r)
    del counts['NA']

    axes = sorted(counts.most_common(), key=lambda t: t[0])
    x = [t[0] for t in axes]
    y = [int(t[1]) for t in axes]

    ax = plt.subplot(111)
    fmt = lambda x, pos: '{:,d}'.format(int(x))
    ax.yaxis.set_major_formatter(FMT(fmt))

    ax.bar(x, y)
    plt.savefig('byyear.png')


if __name__ == '__main__':
    from sys import exit
    exit(main())

#!/usr/bin/env python3

'''
src/gen_report.py

Generate the term paper .tex file using analysis of data set.

- Elvis Yu
- Luke Duane
- Will Badart
created: MAR 2018
'''

import logging
from collections import Counter
from csv import reader
from sys import stdout

LABEL_INDEX = 1
LOG = logging.getLogger(__name__)


def mkclasscounts(path, label_index=LABEL_INDEX):
    '''Generate the class counts for data at `path'.'''
    LOG.info('Couting data labels...')
    with open(path) as fs:
        r = reader(fs)
        next(r)  # Skip column labels
        return Counter(tup[label_index] for tup in r)


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Generate term paper in LaTeX format')
    parser.add_argument('template', metavar='TEMPLATE',
                        help='path to .tex template')
    parser.add_argument('-o', '--output',
                        help='path to output .tex file (default:stdout)')
    parser.add_argument('-d', '--data', default='data/h1b_kaggle.csv',
                        help='path to h-1b data (default:data/h1b_kaggle.csv')
    args = parser.parse_args()
    LOG.setLevel(logging.DEBUG)

    lines = []
    with open(args.template) as fs:
        line = next(fs)
        while not line.strip().startswith('%GENTABLE'):
            lines.append(line)
            line = next(fs)
        counts = mkclasscounts(args.data, LABEL_INDEX)
        for cls, ct in counts.most_common():
            lines.append('    {} & {:,d} \\\\\n'.format(cls, ct))
        lines.append('     \hline')
        lines.append('     TOTAL & {:,d} \\\\\n'.format(sum(counts.values())))
        for line in fs:  # Get the rest of the template
            lines.append(line)

    with (open(args.output, 'w') if args.output is not None else stdout) as fs:
        for line in lines:
            fs.write(line)


if __name__ == '__main__':
    from sys import exit
    exit(main())

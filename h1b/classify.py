#!/usr/bin/env python3

'''
h1b/classify.py

Predict the CASE_STATUS of applications from the primary dataset.
created: MAR 2018
'''


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    args = parser.parse_args()
    print(args)


if __name__ == '__main__':
    from sys import exit
    exit(main())

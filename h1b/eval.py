#!/usr/bin/env python3

'''
src/eval.py

Evaluate some models.
'''

from functools import partial
from multiprocessing import cpu_count, Pool

from .nb import NaiveBayes
from .pd import from_kaggle


def check(nb, i, tup):
    label = tup.CASE_STATUS
    tup.CASE_STATUS = None
    print('Classifying instance %d...' % i)
    return nb.classify(tup) == label


def main():
    df = from_kaggle()
    train = df.sample(100000)
    test = df.sample(100000)

    nb = NaiveBayes(train)
    model_eval = partial(check, nb)

    with Pool(processes=cpu_count()) as p:
        results = p.starmap(model_eval, test.iterrows())

    print(sum(results) / len(results))


if __name__ == '__main__':
    from sys import exit
    exit(main())

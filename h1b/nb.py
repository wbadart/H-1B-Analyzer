#!/usr/bin/env python3

'''
src/nb.py

Attempt to predict H-1B case status with Naive Bayes.

- Elvis Yu
- Luke Duane
- Will Badart
created: MAR 2018
'''

from collections import Counter, defaultdict
from functools import lru_cache, partial, reduce
from operator import mul

from pandas import read_csv
from pandas.api.types import is_categorical

from .pd import from_kaggle


class NaiveBayes(object):
    '''
    Encapsulate the probability calculations for running NB algorithm.
    '''

    def __init__(self, df, label_cls='CASE_STATUS'):
        self._df = df
        self._label_cls = label_cls

    def classify(self, tup):
        '''
        Attempt to label the tuple.
        '''
        return max(self.label_df.values, key=partial(self.label_prob, tup))

    def label_prob(self, tup, label):
        '''
        Give the probability of the label given tuple `tup'.
        '''
        masked_idxs = {
            i for i, c in enumerate(self._df)
            if c == self._label_cls or not is_categorical(self._df[c])}

        prior_prob = self.label_df.value_counts()[label] / len(self._df)

        probs = (self.probability(ft, val, label)
                 for i, (ft, val) in enumerate(zip(self._df, tup))
                 if i not in masked_idxs)

        return prior_prob * reduce(mul, probs)

    def probability(self, feature, value, label):
        '''
        Probability of `label' given `feature' = `value'.
        '''
        matching = self.counts[feature][value][label]
        return matching / self._df[self.label_df == label].shape[0]

    @property
    @lru_cache(maxsize=1)
    def counts(self):
        '''
        Count the labels by feature value.
        '''
        counts = {f: defaultdict(Counter) for f in self._df.columns}
        for _, tup in self._df.iterrows():
            for feat, val in zip(self._df.columns, tup):
                counts[feat][val][tup[self._label_cls]] += 1
        return counts

    @property
    def label_df(self):
        '''
        Labels as a data frame.
        '''
        return self._df[self._label_cls]


def probability(df, feature, value, label, label_cls='CASE_STATUS'):
    '''Give the probability of `label' given feature=value.'''
    matching = len(df[(df[feature] == value) & (df[label_cls] == label)])
    return matching / df[df[label_cls] == label].shape[0]


def label_prob(df, tup, label, label_cls='CASE_STATUS'):
    '''Probability of tuple `tup' having `label' given data `df'.'''
    masked_cols = df.columns.drop(label_cls)
    masked_tup = [d for i, d in enumerate(tup)
                  if i != df.columns.get_loc(label_cls)]
    prior_prob = len(df[df[label_cls] == label]) / len(df)
    probs = (probability(df, ft, val, label)
             for ft, val in zip(masked_cols, masked_tup))
    return prior_prob * reduce(mul, probs)


def classify(df, tup, label_cls='CASE_STATUS'):
    '''Attempt to classify the tuple given the present data.'''
    return max(df[label_cls].values, key=partial(label_prob, df, tup))


df = from_kaggle()
test = [
    "CERTIFIED-WITHDRAWN",
    "VMS COMMUNICATIONS LLC",
    "CHIEF EXECUTIVES",
    "CHIEF OPERATING OFFICER",
    True,
    159370,
    2016,
    "MIAMI, FLORIDA",
    -80.1917902,
    25.7616798
]
# def main():
#     df = from_kaggle()


# if __name__ == '__main__':
#     from sys import exit
#     exit(main())

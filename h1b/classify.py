#!/usr/bin/env python3

'''
h1b/classify.py

Predict the CASE_STATUS of applications from the primary dataset.
created: MAR 2018
'''

from functools import partial
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

# from .cluster import cluster_strings
from .util import load_dataframe, PRIMARY

MODELS = {
    'GaussianNB': GaussianNB,
    'DecisionTreeClassifier': DecisionTreeClassifier,
    'MLPClassifier': partial(MLPClassifier, hidden_layer_sizes=(10,)),
}

NB_FEATURES = [
    # 'EMPLOYER_NAME',
    # 'SOC_NAME',
    # 'JOB_TITLE',
    # 'JOB_CLUSTER',
    'FULL_TIME_POSITION',
    'PREVAILING_WAGE',
    'YEAR',
    # 'WORKSITE',
    'lon', 'lat',
]


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-f', '--file', default=PRIMARY,
                        help='location of dataset w/in data directory '
                        '(default:{})'.format(PRIMARY))
    args = parser.parse_args()
    df = load_dataframe(args.file).dropna()
    df.CASE_STATUS = df.CASE_STATUS == 'CERTIFIED'
    # df = df.assign(JOB_CLUSTER=cluster_strings('KMeans', 12, df.JOB_TITLE))
    X_train, X_test, y_train, y_test = train_test_split(
        df[NB_FEATURES], df.CASE_STATUS)  # , stratify=df.CASE_STATUS)

    for model_cls in MODELS.values():
        print('===', model_cls, '===')
        model = model_cls()
        model.fit(X_train, y_train)
        y_predicted = model.predict(X_test)

        print(confusion_matrix(y_test, y_predicted))
        print(accuracy_score(y_test, y_predicted))
        print()


if __name__ == '__main__':
    from sys import exit
    exit(main())

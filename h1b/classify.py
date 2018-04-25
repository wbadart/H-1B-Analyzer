#!/usr/bin/env python3

'''
h1b/classify.py

Predict the CASE_STATUS of applications from the primary dataset.
created: MAR 2018
'''

import sklearn.metrics as metrics

from itertools import product, repeat
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import pydotplus
from IPython.display import Image, display

# from .cluster import cluster_strings
from .util import load_dataframe, PRIMARY, Timer

MODELS = {
    'GaussianNB': (GaussianNB, {}),

    'DecisionTreeClassifier': (DecisionTreeClassifier, {
        'criterion': ('gini', 'entropy'),
        'splitter': ('best', 'random')}),

    'MLPClassifier': (MLPClassifier, {
        'hidden_layer_sizes': range(2, 100, 20),
        'activation': ('relu', 'identity', 'logistic', 'tanh'),
        'solver': ('adam', 'lbfgs', 'sgm')}),
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


def parameter_combinations(params):
    '''
    Framework for generating all possible combinations of model parameters.
    '''
    kv_pairs = [
        [(k, v) for k, v in zip(repeat(param), vals)]
        for param, vals in params.items()]
    return product(*kv_pairs)


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-m', '--models', nargs='+', choices=list(MODELS),
                        default=[],
                        help='models to run over the data (default:all)')
    parser.add_argument('-f', '--file', default=PRIMARY,
                        help='location of dataset w/in data directory '
                        '(default:{})'.format(PRIMARY))
    args = parser.parse_args()

    df = load_dataframe(args.file).dropna()
    df.CASE_STATUS = df.CASE_STATUS == 'CERTIFIED'
    # df = df.assign(JOB_CLUSTER=cluster_strings('KMeans', 12, df.JOB_TITLE))

    X_train, X_test, y_train, y_test = train_test_split(
        df[NB_FEATURES], df.CASE_STATUS)  # , stratify=df.CASE_STATUS)

    filename = 'Tree1.dot'
    num_tree = 2

    models = {name: MODELS[name] for name in args.models} or MODELS
    for model_cls, all_options in models.values():
        for params in parameter_combinations(all_options):
            print(getattr(model_cls, '__name__', model_cls), params)
            model = model_cls(**dict(params))

            with Timer() as t:
                model.fit(X_train, y_train)
            print('train time:', t, 's')

            with Timer() as t:
                y_predicted = model.predict(X_test)
            print('test time: ', t, 's')
            print(metrics.confusion_matrix(y_test, y_predicted))
            print('accuracy: ', metrics.accuracy_score(y_test, y_predicted))
            print('f1:       ', metrics.f1_score(y_test, y_predicted))
            print('precision:', metrics.precision_score(y_test, y_predicted))
            print('recall:   ', metrics.recall_score(y_test, y_predicted))
            print('auc:      ', metrics.auc(y_test, y_predicted))
            print()

            if model_cls.__name__ == 'DecisionTreeClassifier':
                tree.export_graphviz(model, out_file=filename, max_depth=7, feature_names=NB_FEATURES)
                filename = 'Tree' + str(num_tree) + '.dot'
                num_tree += 1
            

if __name__ == '__main__':
    from sys import exit
    exit(main())

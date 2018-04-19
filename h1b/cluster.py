#!/usr/bin/env python3

'''
h1b/cluster.py

Find clusterings of the many thousands of job titles within the dataset.
created: APR 2018
'''

import matplotlib.pyplot as plt
import numpy as np

from collections import Counter, defaultdict
from csv import reader
from pprint import pprint

from nltk.tokenize import word_tokenize
from sklearn.cluster import AgglomerativeClustering, KMeans, SpectralClustering
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD

from .util import datapath, PRIMARY

ALGS = {
    'AgglomerativeClustering': AgglomerativeClustering,
    'KMeans': KMeans,
    'SpectralClustering': SpectralClustering}
N_CLUSTERS = 8


def cluster(algname, n_clusters, data):
    '''
    Produce a clustering of the data according to the algorithm's `fit_predict'
    method and the `n_clusters' parameter.
    '''
    if algname not in ALGS:
        raise RuntimeError(
            'invalid algname %r. Must be one of %r' % (algname, ALGS))
    return ALGS[algname](n_clusters=n_clusters).fit_predict(data)


def cluster_keywords(clustering, data):
    '''
    Count the occurrences of job title keywords in each cluster.
    '''
    clusters = defaultdict(set)
    for c, job_title in zip(clustering, data):
        clusters[c].add(job_title)
    return clusters


def cluster_strings(algname, n_clusters, data):
    '''
    Performing the clustering, including the vectorization step of the process.
    '''
    c = CountVectorizer(tokenizer=word_tokenize).fit(
        np.random.choice(data, min(len(data), 20000)))
    svd = TruncatedSVD().fit_transform(c.transform(data))
    return svd, cluster(algname, n_clusters, svd)


def wordcount(title_set):
    return Counter(
        w for title in title_set for w in word_tokenize(title) if w.isalpha())


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-n', '--clusters', type=int, default=N_CLUSTERS,
                        help='number of clusters '
                        '(default:{})'.format(N_CLUSTERS))
    parser.add_argument('--alg', choices=list(ALGS), default='KMeans',
                        help='clustering algorithm to run (default:KMeans)')
    parser.add_argument('-f', '--file', default=PRIMARY,
                        help='location of dataset w/in data directory '
                        '(default:{})'.format(PRIMARY))
    parser.add_argument('-o', metavar='OUTPUT',
                        help='plot output file (if unset, do not plot, '
                        'just print clusterings)')
    args = parser.parse_args()
    colors = np.random.random((args.n, 3))

    with datapath(args.file).open() as fs:
        data = list(set(
            r[4].replace('AND ', '').replace('OF ', '') for r in reader(fs)))

    vec = CountVectorizer(tokenizer=word_tokenize).fit_transform(data)
    svd = TruncatedSVD().fit_transform(vec)

    fig, axes = plt.subplots(2, 3)
    fig.subplots_adjust(wspace=1)

    for i, ax in enumerate(np.array(axes).flatten()):
        clustering = cluster(args.alg, N_CLUSTERS - i, svd)
        labeled = np.append(svd, clustering.reshape(len(data), 1), axis=1)

        for c, titles in cluster_keywords(clustering, data).items():
            if not args.o:
                print('{}: {!r}'.format(c, titles))

            wc = wordcount(titles)
            t = labeled[labeled[:, 2] == c]
            ax.scatter(t[:, 0], t[:, 1], c=colors[c],
                       label=', '.join(w for w, _ in wc.most_common(3)))

        ax.set_title(f'{N_CLUSTERS - i} Clusters')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

    if args.o:
        plt.savefig(args.o)


if __name__ == '__main__':
    from sys import exit
    exit(main())

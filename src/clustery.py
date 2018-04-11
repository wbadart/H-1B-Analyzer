#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from collections import Counter, defaultdict
from csv import reader
from fileinput import input as fileinput
from pprint import pprint
from wbutil import lmap

from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD

N_CLUSTERS = 12
COLORS = np.random.random((N_CLUSTERS, 3))


def centroid(a):
    return a.mean(axis=0)


def wordcount(title_set):
    return Counter(w for title in title_set
                   for w in word_tokenize(title) if w.isalpha())


def difference(data):
    '''WIP'''
    vocab = {w for r in data for w in word_tokenize(r)}

    def _impl(a):
        others = vocab - a
        pass


def main():
    with fileinput() as fs:
        data = list(set(
            r[4].replace('AND ', '').replace('OF ', '') for r in reader(fs)))

    vec = CountVectorizer(tokenizer=word_tokenize).fit_transform(data)
    svd = TruncatedSVD().fit_transform(vec)
    fig, axes = plt.subplots(2, 5)
    fig.subplots_adjust(wspace=1)

    for i, ax in enumerate(np.array(axes).flatten()):
        clustering = SpectralClustering(
            n_clusters=N_CLUSTERS - i).fit_predict(svd)
        labeled = np.append(svd, clustering.reshape(len(data), 1), axis=1)

        clusters = defaultdict(set)
        for c, r in zip(clustering, data):
            clusters[c].add(r)
        pprint(clusters)

        for c, titles in clusters.items():
            # others = set(data) - titles
            wc = wordcount(titles)
            t = labeled[labeled[:, 2] == c]
            ax.scatter(t[:, 0], t[:, 1], c=COLORS[c],
                       label=', '.join(w for w, _ in wc.most_common(3)))

        ax.legend(loc='lower center', bbox_to_anchor=(0.0, -0.3))

    # plt.title('Clustering of %d Job Titles' % len(data))
    plt.show()


if __name__ == '__main__':
    from sys import exit
    exit(main())

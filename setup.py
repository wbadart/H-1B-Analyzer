#!/usr/bin/env python3

'''
setup.py
created: APR 2018
'''

from setuptools import setup, find_packages


setup(name='h1b',
      author='Wenhao Yu, Luke Duane, Will Badart',
      author_email='wyu1@nd.edu, lduane@nd.edu, wbadart@nd.edu',
      version='1.0.0',
      packages=find_packages(),
      url='https://github.com/wbadart/H-1B-Analyzer',
      license='MIT',
      zip_safe=False,
      description=('Apply data science techniques to the analysis of the H-1B '
                   'visa program'),

      install_requires=[
          'matplotlib',
          'numpy',
          'pandas',
          'pydotplus',
          'sklearn',
      ],

      entry_points={
          'console_scripts': [
              'h1b.cluster = h1b.cluster:main',
              'h1b.describe = h1b.description:main',
              'h1b.classify = h1b.classify:main',
          ],
      })

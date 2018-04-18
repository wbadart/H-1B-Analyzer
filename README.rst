
Determining Predictors of H-1B Salary and Approval (Project *DPH*)
==================================================================

Project Documentation
---------------------

**Contributors:** - Wenhao Yu (netid: *wyu1*) - Luke Duane (netid:
*lduane*) - Will Badart (netid: *wbadart*)

This project aims to provide meaningful analyses of the factors that
drive H-1B visa approval, and provide insightful, tangential analyses
which provide business value to enterprises sponsoring H-1B employees.
The project has been excecuted for Notre Dame *CSE 40647/ 60647 - Data
Science* as specified in the `project
instructions <http://www.meng-jiang.com/teaching/CSE647Spring18-Project.pdf>`__.

Installation
------------

Running the project requires `Python
3 <https://www.python.org/downloads/release/python-365/>`__. To install
the project to your system as a package, as well as its dependencies,
run:

::

    $ pip3 install git+https://github.com/wbadart/H-1B-Analyzer.git

This will also add the project’s several entry points to your path, for
running the individual analyses directly from the command line (see
`Usage <#Usage>`__).

Generating the Report
---------------------

The source code of the report is available under
```docs/main.tex`` <./docs/main.tex>`__ if you need to compile it to
anything other than a PDF. To compile, simple enter the documentation
folder and run ``make`` (requires ``pdflatex`` to be installed and
available on your ``PATH``).

::

    $ pwd
    /path/to/H-1B-Analyzer
    $ cd docs
    $ make

Otherwise, the complete compiled report is already checked into the
repository as
```docs/Determining Predictors of H-1B Salary and Approval.pdf`` <./docs/Determining%20Predictors%20of%20H-1B%20Salary%20and%20Approval.pdf>`__.

Usage
-----

WIP

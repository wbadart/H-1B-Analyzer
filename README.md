# H-1B-Analyzer
Use data science techniques to analyze H-1B visa application data. CSE 40647/60647

## Installation

To interact with the project, clone the repository to an appropriate workning
directory:

    $ git clone https://github.com/wbadart/H-1B-Analyzer

Running the scripts in `src/` require [Python 3](https://python.org) and a
couple thrid-party packages, which can by installed via pip like so:

    $ pip install --user -r requirements.txt


## Usage

The commands to generate the report are exposed by the Makefile:

    $ make report

Will place `milestone.pdf` in the current directory. The `pdflatex` command it
uses will also put secondary output files in the current working directory.
These can be removed with

    $ make clean

To reset the repository state (remove `pdflatex` output and report PDF) use
`make clean-all`.


## Contributors

- Wenhao (Elvis) Yu *wyu1*
- Luke Duane *lduane*
- Will Badart *wbadart*

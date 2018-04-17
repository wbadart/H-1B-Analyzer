##
# Makefile
#
# Central location for all code building and report
# generation rules and commands.
#
# - Elvis Yu
# - Luke Duane
# - Will Badart
# created: MAR 2018
##

all:
	pdflatex main

report:
	python3 src/apps_by_yr.py
	python3 src/gen_report.py docs/milestone.tex.tmpl -o milestone.tex
	pdflatex milestone.tex

clean:
	rm -f byyear.png
	rm -f *.{tex,aux,log,out}

clean-all: clean
	rm -f *.pdf

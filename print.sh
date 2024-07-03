#!/bin/sh
cd pandoc
printf "this item belongs to ${1}\n\nin the fridge since ${2}" > label.md
pandoc label.md -t html5 -c print-styles.css --pdf-engine weasyprint -o label.pdf

evince label.pdf

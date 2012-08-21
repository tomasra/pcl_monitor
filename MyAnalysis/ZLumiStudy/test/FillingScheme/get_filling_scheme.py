#!/usr/bin/env python

import sys

from filling_scheme_tools import GetFillingScheme

if len(sys.argv) < 3:
	print "Usage: get_filling_scheme.py <run-number> <output-file>"
	sys.exit(1)

runNumber = int(sys.argv[1])
outputFile = sys.argv[2]

print "Getting filling scheme for run", runNumber
fs = GetFillingScheme(run_number=runNumber)

out = open(outputFile, "w")

for bx in fs.active_bx_pattern:
	out.write(str(int(bx)) + "\n")


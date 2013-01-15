#!/bin/env python

import os
import datetime
import sys

if len(sys.argv) != 4:
    print "Incorrect number of arguments. Please specify the 3 arguments as GT1, GT2 and destination directory, respectively."
GT1 = sys.argv[1]
GT2 = sys.argv[2]
RunningDir = "/afs/cern.ch/user/a/alcaprod/Alca/GlobalTag/CMSSW_4_4_2_patch8/src/"
command = "cd "+RunningDir+"; export TNS_ADMIN=/afs/cern.ch/cms/DB/conddb; gtCompare.py "+GT1+" "+GT2+" --dump"
destination = sys.argv[3]

print command
os.system(command+" > test.txt")

outputFile = open(destination, "w")

outputFile.write('<html>')
outputFile.write('<body>')
outputFile.write('<verbatim>')
outputFile.write('Time of last comparison: ' + str(datetime.date.today()) + '<br>')
outputFile.write('Command used: \"'+command+'\"<br><br>')
outputFile.write('The last IOVs of the tags listed here are different:<br>')

found = False
missingTags = [""]
for line in open("test.txt"):
    if line.find("rcd") != -1:
        if line.find("not in") == -1:
            found = True
            outputFile.write(line.replace('[94m', '<br><font color=\"blue\">').replace('[0m', '</font><br>').rstrip())
        else:
            missingTags.append(line)
    elif found:
        outputFile.write(line.replace('[94m', '<br><font color=\"blue\">').replace('[0m', '</font><br>').rstrip())
        found = False
    else:
        found = False

outputFile.write("")
outputFile.write('<br><br><br>The tags listed here are contained only in one of the two GTs:<br>')

for tag in missingTags:
    outputFile.write(tag.rstrip()+'<br>')

outputFile.write('</verbatim>')
outputFile.write('</body>')
outputFile.write('</html>')
outputFile.close()

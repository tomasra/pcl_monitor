#!/bin/env python

"""
This script saves a list of the last IOV for all the tags in a given GT.
This list is compared with the previous file to see if there was any new IOV appended.
It sends a mail with the list of new IOVs. It sends no mail in case no difference is found.
"""

import sys
from Tools.MyCondTools.gt_tools import *
from ConfigParser import ConfigParser

if len(sys.argv) != 2:
    print "Usage: ./gtMonitor.py GTNAME"
    sys.exit()

# read a global configuration file
cfgfile = ConfigParser()
cfgfile.optionxform = str
CONFIGFILE = "GT_branches/Common.cfg"
print 'Reading configuration file from ',CONFIGFILE
cfgfile.read([ CONFIGFILE ])

# get the releases currently managed
gtconnstring           = cfgfile.get('Common','GTConnectString')
passwdfile             = cfgfile.get('Common','Passwd')

# print "passwdfile:", passwdfile
# print "gtconnstring:", gtconnstring

globaltag = sys.argv[1]
# globaltag = "GR_R_52_V7"

mailFileName = "gtMonitorMail.txt"
mailFile = open(mailFileName, "w")
mailFile.write("New appends for GT " + globaltag + "\n\n")

outputFileName = globaltag+"_lastIOVs.txt"
outputFile = open(outputFileName, "w")

statusandoutput = tagtreeList(globaltag, gtconnstring, passwdfile)

if statusandoutput[0] != 0:
    print "Error listing tags for GT " + globaltag
    mailFile.write("Error listing tags for GT " + globaltag + "\n")
    # sys.exit()

outputLines = []
for line in statusandoutput[1].split("\n"):
    elem = line.split()
    if len(elem) > 6:
        tag = elem[2].split(":")[1]
        connectionString = elem[6].split("pfn:")[1]
        # Do not use Frontier because of cache problems (running two times in a row may connect to different instances and give different results).
        connectionString = connectionString.replace("frontier://FrontierProd/", "oracle://cms_orcon_adg/")

        iovs = listIov(connectionString, tag, passwdfile)
        # print "tag:",tag
        # print iovs
        if iovs[0] != 0:
            print "Error in listIov for tag: " + tag
            mailFile.write("Error in listIov for tag: " + tag + "\n")
            continue
        # Read the next to last element. The last one is text with the number of IOVs.
        lastIOV = iovs[1].split("\t")[-2].split()[0]
        if iovs[1].split("\t")[-1].find("Total") == -1:
            lastIOV = iovs[1].split("\t")[-1].split()[0]
            # print "last line =", iovs[1].split("\t")[-1]
        outputText = "tag: " + tag + " lastIOV= " + lastIOV + "\n"
        outputLines.append(outputText)
        # print outputText

for line in outputLines:
    outputFile.write(line)
outputFile.close()

try:
    # Read the files again
    newFile = open(outputFileName).readlines()
    oldFile = open(outputFileName.replace(".txt", "_previous.txt")).readlines()
    # Check that the number of tags is the same
    if len(newFile) != len(oldFile):
        mailFile.write("Error: number of tags in old and new file differ for GT " + globaltag + ". No comparison will be done.\n")
        print "Error: number of tags in old and new file differ for GT " + globaltag + ". No comparison will be done."
        raise
    # Check the last IOVs for all tags
    for i in range(len(oldFile)):
         oldTag = oldFile[i].split()[1]
         oldIOV = oldFile[i].split()[-1]
         newTag = newFile[i].split()[1]
         newIOV = newFile[i].split()[-1]
         # print "old tag: "+oldTag+" IOV: "+oldIOV
         # print "new tag: "+newTag+" IOV: "+newIOV
         # print "Checking tag " + oldTag
         if oldTag != newTag:
             mailFile.write("Error: tags out of order\n")
             print "Error: tags out of order."
             raise
         if oldIOV != newIOV:
             mailFile.write("New IOV " + newIOV + " appended for tag " + oldTag + ". Previous IOV was " + oldIOV + "\n")
             # print "New IOV " + newIOV + " appended for tag " + oldTag + ". Previous IOV was " + oldIOV
             # print "oldFile[",i,"] =", oldFile[i]
             # print "newFile[",i,"] =", newFile[i]
except:
    pass

mailFile.close()
# Send mail if needed
if len(open(mailFileName).readlines()) > 2:
    print "Sending mail"
    os.system("mail -s \"GT Monitoring\" \"marco.de.mattia@cern.ch\" < \""+mailFileName+"\"")
    # os.system("mail -s \"GT Monitoring\" \"cms-alca-globaltag@cern.ch\" < \""+mailFileName+"\"")

# Move the new file to old
os.system("mv "+globaltag+"_lastIOVs.txt "+globaltag+"_lastIOVs_previous.txt")

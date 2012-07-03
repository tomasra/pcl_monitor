#!/bin/env python

"""
This script saves a list of the last IOV for all the tags in a given GT.
This list is compared with the previous file to see if there was any new IOV appended.
It sends a mail with the list of new IOVs. It sends no mail in case no difference is found.
Tags are divided in cathegory A, cathegory C and not cathegory A,C and the lists are separated in the mail.
The list of records and labels in cathegory A and C are defined in cathegoryA and cathegoryC here.
"""

cathegoryA = ["L1TriggerKeyRcd",
              "L1TriggerKeyListRcd",
              "L1GtTriggerMaskAlgoTrigRcd",
              "L1GtTriggerMaskVetoAlgoTrigRcd",
              "L1GtTriggerMaskTechTrigRcd",
              "L1GtTriggerMaskVetoTechTrigRcd",
              "L1GtPrescaleFactorsAlgoTrigRcd",
              "L1GtPrescaleFactorsTechTrigRcd",
              "L1GtPsbSetupRcd",
              "L1GtParametersRcd",
              "L1GctJetFinderParamsRcd",
              "L1HfRingEtScaleRcd",
              "L1HtMissScaleRcd",
              "L1JetEtScaleRcd",
              "L1MuCSCTFConfigurationRcd",
              "L1MuDTTFParametersRcd",
              "L1RPCConfigRcd",
              "L1RPCConeDefinitionRcd",
              "L1RPCHsbConfigRcd",
              "L1RPCBxOrConfigRcd",
              "CSCL1TPParametersRcd",
              "RunInfoRcd",
              "SiStripDetVOffRcd",
              "SiStripBadChannelRcd",
              "SiStripPedestalsRcd",
              "SiStripNoisesRcd",
              "SiStripLatencyRcd",
              "SiStripThresholdRcd",
              "SiStripFedCablingRcd",
              "EcalDCSTowerStatusRcd",
              "DTCCBConfigRcd",
              "DTHVStatusRcd",
              "EcalTPGSlidingWindowRcd",
              "EcalTPGFineGrainStripEERcd",
              "EcalTPGPedestalsRcd",
              "EcalTPGLutIdMapRcd",
              "EcalTPGFineGrainTowerEERcd",
              "EcalTPGWeightIdMapRcd",
              "EcalTPGSpikeRcd",
              "EcalTPGWeightGroupRcd",
              "EcalTPGFineGrainEBIdMapRcd",
              "EcalTPGLinearizationConstRcd",
              "EcalTPGLutGroupRcd",
              "EcalTPGFineGrainEBGroupRcd",
              "EcalTPGPhysicsConstRcd",
              "EcalTPGStripStatusRcd",
              "EcalTPGTowerStatusRcd",
              "EcalTPGCrystalStatusRcd",
              "EcalPedestalsRcd"
              ]

cathegoryC = ["BeamSpotObjectsRcd",
              "EcalLaserAPDPNRatiosRcd",
              "SiStripBadFiberRcd"]


def findCathegory(rcd, label):
    """Returns True if the tag is in cathegory A."""
    for elem in cathegoryA:
        if elem.find(rcd) != -1 and elem.find(label) != -1:
            return "A"
    for elem in cathegoryC:
        if elem.find(rcd) != -1 and elem.find(label) != -1:
            return "C"
    return "B"


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

# create the collection of tags
tagCollection = GTEntryCollection()
# --------------------------------------------------------------------------
# fill the collection
if not confFileFromDB(globaltag, globaltag+".conf", gtconnstring, passwdfile):
    print error("*** Error" + " original GT conf file: " + globaltag + " doesn't exist!")
    sys.exit(5)
fillGTCollection(globaltag+".conf", globaltag, tagCollection)

outputLines = []
# loop over all records and compare the tag names and the # of payloads
for index in range(0, len(tagCollection._tagOrder)):
    entry = tagCollection._tagList[tagCollection._tagOrder[index]]
    connectionString = "oracle://cms_orcon_adg/" + entry._account
    iovs = listIov(connectionString, entry._tag, passwdfile)
    if iovs[0] != 0:
        print "Error in listIov for tag: " + entry._tag
        mailFile.write("Error in listIov for tag: " + entry._tag + "\n")
        continue
    # Read the next to last element. The last one is text with the number of IOVs.
    lastIOV = iovs[1].split("\t")[-2].split()[0]
    if iovs[1].split("\t")[-1].find("Total") == -1:
        lastIOV = iovs[1].split("\t")[-1].split()[0]
    outputLabel = "\"\""
    if entry._label != "":
        outputLabel = entry._label
    outputText = "tag: " + entry._tag + ", rcd: " + entry._record + ", label: " + outputLabel + ", lastIOV: " + lastIOV + "\n"
    outputLines.append(outputText)

# Save all the tags and the last IOVs to an output file
for line in outputLines:
    outputFile.write(line)
outputFile.close()

# Compare the old list with the new one and prepare the mail with the changes.
cathegoryATags = []
cathegoryCTags = []
cathegoryNotACTags = []
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
        oldFileSplit = oldFile[i].split(",")
        newFileSplit = newFile[i].split(",")
        oldTag = oldFileSplit[0].split()[1]
        oldIOV = oldFileSplit[-1].split()[1]
        newTag = newFileSplit[0].split()[1]
        newIOV = newFileSplit[-1].split()[1]
        oldRcd = oldFileSplit[1].split()[1]
        oldLabel = ""
        if len(oldFileSplit[2].split()) > 1 and oldFileSplit[2].find("\"\"") == -1:
            oldLabel = oldFileSplit[2].split()[1]
        # print "old tag: "+oldTag+" IOV: "+oldIOV
        # print "new tag: "+newTag+" IOV: "+newIOV
        # print "Checking tag " + oldTag
        if oldTag != newTag:
            mailFile.write("Error: tags out of order\n")
            print "Error: tags out of order."
            raise
        if oldIOV != newIOV:
            # mailFile.write("New IOV " + newIOV + " appended for tag " + oldTag + ". Previous IOV was " + oldIOV + "\n")
            outputLine = oldTag + " (rcd: "+oldRcd+", label: "+oldLabel+") : new IOV " + newIOV + " appended. Previous IOV was " + oldIOV + "\n"
            cathegory = findCathegory(oldRcd, oldLabel)
            if cathegory == "A": cathegoryATags.append(outputLine)
            elif cathegory == "C": cathegoryCTags.append(outputLine)
            else: cathegoryNotACTags.append(outputLine)
            # print "New IOV " + newIOV + " appended for tag " + oldTag + ". Previous IOV was " + oldIOV
            # print "oldFile[",i,"] =", oldFile[i]
            # print "newFile[",i,"] =", newFile[i]

except:
    pass

if len(cathegoryNotACTags) > 0:
    mailFile.write("Cathegory B and D tags updated (Require approval):\n\n")
    for line in cathegoryNotACTags:
        mailFile.write(line)

if len(cathegoryCTags) > 0:
    mailFile.write("\n\nCathegory C tags updated (PCL):\n\n")
    for line in cathegoryCTags:
        mailFile.write(line)

if len(cathegoryATags) > 0:
    mailFile.write("\n\nCathegory A tags updated:\n\n")
    for line in cathegoryATags:
        mailFile.write(line)

mailFile.close()
# Send mail if needed
if len(open(mailFileName).readlines()) > 2:
    print "Sending mail"
    # os.system("mail -s \"GT Monitoring\" \"marco.de.mattia@cern.ch\" < \""+mailFileName+"\"")
    os.system("mail -s \"GT Monitoring\" \"cms-alca-globaltag@cern.ch\" < \""+mailFileName+"\"")

# Move the new file to old
os.system("mv "+globaltag+"_lastIOVs.txt "+globaltag+"_lastIOVs_previous.txt")

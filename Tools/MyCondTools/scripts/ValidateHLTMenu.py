#!/bin/env python

# This script dumps the content of the AlCaRecoTriggerBits tag provided in input and checks that all the hlt selection paths are selecting some triggers
# by looking at the HLT menu also provided as input. It does the mapping between AlCaRecos and Primary Datasets with the AlCaRecoMatrix.
# The AlCaRecoMatrix is read from the wiki file /afs/cern.ch/cms/CAF/CMSALCA/ALCA_GLOBAL/GTDoc/doc/AlCaRecoMatrix.wiki.
# It produces an output file called validation.txt with the list of matched triggers including prescales.

import sys
import os

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print "Usage: ValidateHLTMenu.py HLTMenu AlCaRecoHLTpathsTag [RunNumber]"
    print "Example: ./ValidateHLTMenu.py /online/collisions/2012/7e33/v2.1/HLT AlCaRecoHLTpaths8e29_5e33_v2_prompt"
    print "If no run number is provided the number 1000000 will be used."
    sys.exit()

HLTMenuName = sys.argv[1]
AlCaRecoHLTPathsTag = sys.argv[2]
runNumber = 1000000
if len(sys.argv) == 4:
    RunNumber = sys.argv[3]

# os.system("cmscond_2XML -c frontier://PromptProd/CMS_COND_31X_HLT -t AlCaRecoHLTpaths8e29_5e33_v2_prompt -b 1000000")
# os.system("edmConfigFromDB --configName /online/collisions/2012/7e33/v2.1/HLT > hlt.py")
# os.system("cat hlt.py | hltDumpStream > dumpStream.txt")
os.system("cmscond_2XML -c frontier://PromptProd/CMS_COND_31X_HLT -t "+AlCaRecoHLTPathsTag+" -b " + str(runNumber))
os.system("edmConfigFromDB --configName "+HLTMenuName+" > hlt.py")
os.system("cat hlt.py | hltDumpStream > dumpStream.txt")

# print "Validating AlCaRecoTriggerBits with HLT menu"
# print "Extract the list of PDs and associated triggers from the menu"

# Need to check: trigger names matching the ones in the AlCaRecoTriggerBits, if they are prescaled, if all the PDs required in the alcareco matrix match or not.

outputFile = open("validation.txt", "w")

def findHLTPath(PrimaryDataset, HLTpath, HLTMenu):
    matchingTriggers = []
    # print PrimaryDataset, HLTpath
    for PD in HLTMenu:
        # Some of them have the stream name instead
        if PD[0].find("dataset "+PrimaryDataset) != -1:
            for path in PD:
                if path.find(HLTpath.rstrip("*")) != -1:
                    matchingTriggers.append(path.rstrip("\n"))

    if len(matchingTriggers) == 0:
        # print "\nError: no matching triggers found for selection string " + HLTpath + "\n"
        outputFile.write("\nError: no matching triggers found for selection string " + HLTpath + "\n\n")
    else:
        # print "The following matching triggers were found in the Primary Dataset " + PD[0].split()[1] + " for trigger selection string \"" + HLTpath + "\":\n"
        outputFile.write("The following matching triggers were found in the Primary Dataset " + PD[0].split()[1] + " for trigger selection string \"" + HLTpath + "\":\n\n")
        for trigger in matchingTriggers:
            # print trigger
            outputFile.write(trigger+"\n")


# read the AlCaRecoMatrix and prepare a dictionary of AlCaReco-PD
AlCaRecoMatrix = {}
for line in open("/afs/cern.ch/cms/CAF/CMSALCA/ALCA_GLOBAL/GTDoc/doc/AlCaRecoMatrix.wiki"):
    if line.find("*Primary Dataset*") != -1:
        continue
    splittedLine = line.split("|")
    if len(splittedLine) > 2:
        for AlCaReco in splittedLine[2].split(","):
            AlCaRecoMatrix[AlCaReco.strip().strip("!")] = splittedLine[1].strip().strip("!")

# Read the trigger menu and prepare a list of triggers for each PD
HLTMenu = []
for line in open("dumpStream.txt"):
    if line.startswith("    dataset "):
        HLTMenu.append([])
    if len(HLTMenu) > 0:
        HLTMenu[len(HLTMenu)-1].append(line)

# Read the AlCaRecoTriggerBits xml dump and find the triggers in the menu
isAlCaRecoName = True
for line in open("AlCaRecoHLTpaths8e29_5e33_v2_prompt.xml"):
    if line.find("CharStar v=") != -1:
        element = line.split('"')[1]
        if isAlCaRecoName:
            AlCaReco = element
            isAlCaRecoName = False
        else:
            # print "\n\n---------------------------------------------------------------------------------------------------"
            # print "Checking AlCaReco: \"" + AlCaReco + "\" with selection string: \"" + element + "\""
            # print "---------------------------------------------------------------------------------------------------\n"
            outputFile.write("\n\n---------------------------------------------------------------------------------------------------\n")
            outputFile.write("Checking AlCaReco: \"" + AlCaReco + "\" with selection string: \"" + element + "\"\n")
            outputFile.write("---------------------------------------------------------------------------------------------------\n\n")
            isAlCaRecoName = True

            # Some of the AlCaRecos have no keys
            triggerSelectionStringList = element.rstrip(";").rstrip()
            if triggerSelectionStringList == "":
                # print "This AlCaReco has no keys. It is either disabled or accepting everything. Listing all the triggers available in the PD"
                outputFile.write("This AlCaReco has no keys. It is either disabled or accepting everything. Listing all the triggers available in the PD\n")
            else:
                if AlCaReco in AlCaRecoMatrix:
                    for triggerSelectionString in triggerSelectionStringList.split(";"):
                        findHLTPath(AlCaRecoMatrix[AlCaReco], triggerSelectionString, HLTMenu)
                else:
                    # print "This AlCaReco is not in the matrix"
                    outputFile.write("This AlCaReco is not in the matrix\n")

outputFile.close()

print "Comparison done. Please, check the validation.txt file for details."

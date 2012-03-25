#!/usr/bin/env python

import os, sys
from subprocess import Popen, PIPE # , check_call


testDir = "/afs/cern.ch/user/a/alcaprod/Alca/RelIntegration"
# Release used to do cmsenv and run the cmstc script
relForTC = "CMSSW_5_2_0"

# Dictionary {release, architecture} to allow the correct SCRAM_ARCH to be set
relArch = {}
relArch["CMSSW_6_0_X"] = "slc5_amd64_gcc462"
relArch["CMSSW_5_2_X"] = "slc5_amd64_gcc462"
relArch["CMSSW_4_4_X"] = "slc5_amd64_gcc434"
relArch["CMSSW_4_1_X"] = "slc5_amd64_gcc434"


def findLastRelease(release):
    """Find the last release. matching the first two numbers of the passed release name.
    It assumes the list returned by scram list CMSSW is sorted with the most recent release at the bottom"""
    print release
    cmd = "export SCRAM_ARCH="+relArch[release]+"; scram list CMSSW"
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        print "Error in getting list of releases"
    else:
        lastRelease = ""
        for line in stdout.split("\n"):
            tokens = line.split()
            if len(tokens) == 2 and tokens[0] == "CMSSW":
                if tokens[1].find(release[0:-1]) != -1:
                    lastRelease = tokens[1]

        print "lastRelease = " + lastRelease
        return lastRelease

def checkCall(cmd):
    """In python2.4 there is no subprocess.check_call and lxbuild shows only that version..."""
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
    p.communicate()
    if p.returncode != 0:
        raise p.returncode


print "Checking all tagsets waiting for AlCa sign-off"

outputFileName = testDir+"/TagsetTest.txt"
outputFile = open(outputFileName, "w")

# Takes longer, dependent on the format of the "Pending_signatures" string
# cmd = "cmstc tagssign --all | grep Calibration_and_Alignment"
# Takes less time, dependent on the user name
cmd = "cd "+testDir+"; rm -rf "+relForTC+"; export SCRAM_ARCH=slc5_amd64_gcc462; scram project CMSSW "+relForTC+"; cd "+relForTC+"/src/; cvs co -r V00-13-00 Utilities/ReleaseScripts/scripts/cmstc.py; cvs co -r V00-13-00 Utilities/ReleaseScripts/scripts/cmstc; scram b; "
cmd += "cd "+testDir+"/"+relForTC+"/src; eval `scram r -sh`; cmstc tagssign -u demattia"

# Save the list of all tagsets waiting for signoff
p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
stdout, stderr = p.communicate()
if p.returncode != 0:
    outputFile.write("Error in retrieving tagset list\n")
    outputFile.write(stderr)
    sys.exit(1)

# Build a dictionary of release - list of tagsets
tagsets = {}
for line in stdout.split("\n"):
    if line.startswith("Release"):
        continue
    tokens = line.split()
    if len(tokens) == 7:
        if tokens[0] not in tagsets:
            tagsets[tokens[0]] = [tokens[1:]]
        else:
            tagsets[tokens[0]].append(tokens[1:])

# Build a proper list of tags sorted from the oldest to the newest so that only the most recent tag will be tested
# and run the validation for each release
separator = "\n\n----------------------------\n\n"

print tagsets

for release in tagsets:

    lastRelease = findLastRelease(release)
    cmd = "cd "+testDir+"; export SCRAM_ARCH="+relArch[release]+"; rm -rf "+lastRelease+"; scramv1 project CMSSW "+lastRelease

    enterDirCmd = "export SCRAM_ARCH="+relArch[release]+"; cd "+testDir+"/"+lastRelease+"/src; eval `scramv1 runtime -sh`;"
    # check_call(cmd + "; " + enterDirCmd, shell=True)
    checkCall(cmd + "; " + enterDirCmd)

    # Checkout the tags (including checkdeps) and prepare the list of tested tagsets.
    try:
        outputFile.write("Running validation for release cycle " + release + ". Using release " + lastRelease + "\n")
        list = []
        tagsetList = []
        for line in tagsets[release]:
            list.append(line[1] + " " + line[2])
            tagsetList.append(line[0])
        for tag in sorted(list):
            outputFile.write("Checking out tag "+ tag + "\n")
            cmd = enterDirCmd+" addpkg " + tag
            try:
                # check_call(cmd, shell=True)
                checkCall(cmd)
            except:
                outputFile.write("failed checkout for " + cmd + "\n")
                raise
    except:
        outputFile.write("There was a problem with the checkout of a tagset, skip this release\n")
        outputFile.write(separator)
        continue
    cmd = enterDirCmd+" checkdeps -a"
    try:
         # check_call(cmd, shell=True)
         checkCall(cmd)
    except:
        outputFile.write("Error with checkdeps, skipping this release\n")
        outputFile.write(separator)
        continue

    # Compile
    success = False
    cmd = enterDirCmd+" scram b"
    compile_p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
    stdout, stderr = compile_p.communicate()
    if compile_p.returncode != 0:
        outputFile.write("\nError: The tagset does not compile\n")
        outputFile.write(stderr)
    else:
        outputFile.write("\nCompilation succesful\n")
        success = True

    # Test done, write the list of tagsets and give green light in case of success.
    outputFile.write("\nTested tagsets:\n")
    # Remove duplicates
    tagsetList = list(set(tagsetList))
    for element in tagsetList:
        outputFile.write(element+"\n")
    if success:
        outputFile.write("\nCan be signed-off\n")
    outputFile.write(separator)

outputFile.close()
os.system("mail -s \"Tagset validation\" \"marco.de.mattia@cern.ch\" < \""+outputFileName+"\"")
os.system("mail -s \"Tagset validation\" \"cms-alca-globaltag@cern.ch\" < \""+outputFileName+"\"")

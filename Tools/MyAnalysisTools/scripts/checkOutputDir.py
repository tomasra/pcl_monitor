#!/usr/bin/env python

import os
import sys
import commands
import shutil
import time
from optparse import OptionParser, Option, OptionValueError
from ConfigParser import ConfigParser
from Tools.MyAnalysisTools.color_tools import *
import FWCore.ParameterSet.Config as cms

class JobEntry:
    def __init__(self):
        self.fileNames = []
        self.nEvents = []
        self.maxIndex = -1
        return

    def addFile(self, filen, nev):
        self.fileNames.append(filen)
        self.nEvents.append(nev)
        return

    def findMaxNevIndex(self):
        maxNev = -1
        for index in range(0, len(self.fileNames)):
            if self.nEvents[index] > maxNev:
                self.maxIndex = index
                maxNev = self.nEvents[index]
        #print "Max index: " + str(self.maxIndex)
        return

    def deleteOthers(self):
        for index in range(0, len(self.fileNames)):
            if index != self.maxIndex:
                print "rfrm " + self.fileNames[index]
            

def findJobNumber(fileName, isCrab):
    nUnderscores = len(fileName.split("_"))
    jobNumberIndex = 0
    if isCrab:
        jobNumberIndex = nUnderscores - 3
    jobNumber = int(fileName.split("_")[jobNumberIndex])        
    return jobNumber


if __name__     ==  "__main__":

    # define the command line options
    parser = OptionParser()

    
    # this tell to the script if we read from castor or eos
    parser.add_option("-s", "--store-type", dest="storage",
                      help="type of storage: castor - eos", type="str", metavar="<storage type>",default="eos")

    # this defines the file name forma blabla_#Job_#file_bla.root
    crabMode = True

    (options, args) = parser.parse_args()

    outdir = args[0]
    
    print "reading from " + options.storage
    print "output dir: " + outdir

    # list of files to be checked
    filenames = []


    if options.storage == "castor":
        rfdir_cmd = "rfdir " + outdir        
        outCastorDir_out = commands.getstatusoutput(rfdir_cmd)
        if outCastorDir_out[0] == 0:
            castorLines = outCastorDir_out[1].split("\n")
            if len(castorLines) != 0:
                for castorFileLine in castorLines:
                    #print castorFileLine
                    if "root" in castorFileLine:
                        fileName = castorFileLine.split()[8]
                        filenames.append(fileName)
        else:
            print outCastorDir_out[1]
            sys.exit(1)
    elif options.storage == "eos":
        ls_cmd = "cmsLs " + outdir
        ls_out = commands.getstatusoutput(ls_cmd)
        if ls_out[0] == 0:
            eosLines = ls_out[1].split('\n')
            if len(eosLines) != 0:
                for eosLine in eosLines:
                    if 'root' in eosLine:
                        fileName = eosLine.split()[4]
                        baseName =  os.path.basename(fileName)
                        filenames.append(baseName)
        else:
            print ls_out[1]
            sys.exit(1)
    else:
        "***Error: storage-type: " + options.storage + " not supported!"
        sys.exit(1)

    #print filenames



    jobNumbers = []
    duplicatedJobs = []



    for fileName in filenames:
        jobNumber = findJobNumber(fileName, crabMode)
        if jobNumber in jobNumbers:
            print "Warning duplicated file for job #: " + str(jobNumber)
            if not jobNumber in duplicatedJobs:
                duplicatedJobs.append(jobNumber)
        else:
            jobNumbers.append(jobNumber)


    for fileName in filenames:
        jobNumber = findJobNumber(fileName, crabMode)
        if jobNumber in duplicatedJobs:
            print "Duplicated Job # " + str(jobNumber)
            print " file: " + outdir + "/" + fileName
                    

    print "# of jobs: " + str(len(jobNumbers))
    print "# of files: " + str(len(filenames))
    sys.exit(0)




    nOutFile = 0
    outCastorDir_out = commands.getstatusoutput(rfdir_cmd)
    jobNumbers = []
    duplicatedJobs = []
    if outCastorDir_out[0] == 0:
        castorLines = outCastorDir_out[1].split("\n")
        if len(castorLines) != 0:
            for castorFileLine in castorLines:
                if "root" in castorFileLine:
                    fileName = castorFileLine.split()[8]
                    # print "        - " + fileName

                    if jobNumber in jobNumbers:
                        print "   warning duplicated file for job #: " + str(jobNumber)
                        if not jobNumber in duplicatedJobs:
                            duplicatedJobs.append(jobNumber)
                    jobNumbers.append(jobNumber)
                    
                    nOutFile += 1

        duplicatedFiles = []
        duplicatedNEvents = []
        duplicatedJobForStep2 = []
        
        if len(duplicatedJobs) != 0:
            castorLines = outCastorDir_out[1].split("\n")
            if len(castorLines) != 0:
                for castorFileLine in castorLines:
                    if "root" in castorFileLine:
                        fileName = castorFileLine.split()[8]
                        # print "        - " + fileName
                        jobNumber = int(fileName.split("_")[1])
                        if jobNumber in duplicatedJobs:
                            nEvents = 0
                            print "- duplicated file: " + outdir + fileName
                            ev_cmd = "edmEventSize -v rfio:" + outdir + fileName
                            ev_out = commands.getstatusoutput(ev_cmd)
                            if ev_out[0] == 0:
                                if not "contains no Events" in ev_out[1]:
                                    print ev_out[1].split("\n")[1]
                                    nEvents = int(ev_out[1].split("\n")[1].split()[3])
                            else:
                                print ev_out[1]
                            duplicatedFiles.append(outdir + fileName)
                            duplicatedNEvents.append(nEvents)
                            duplicatedJobForStep2.append(jobNumber)

            eventMap = {}

            for index in range(0, len(duplicatedFiles)):
                fileName = duplicatedFiles[index]
                numEvents = duplicatedNEvents[index]
                jobNumber = duplicatedJobForStep2[index] 
                print str(jobNumber) + " " + fileName + " " + str(numEvents)
                if not jobNumber in eventMap:
                    eventMap[jobNumber] = JobEntry()
                eventMap[jobNumber].addFile(fileName, numEvents)

            for jobr in eventMap.keys():
                #print jobr
                eventMap[jobr].findMaxNevIndex()
                eventMap[jobr].deleteOthers()
                 
    print "# of files: " + str(nOutFile)
    print "# of duplicated files: " + str(len(duplicatedJobs))

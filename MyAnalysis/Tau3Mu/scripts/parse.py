#!/usr/bin/env python

import os
import sys
import commands
from optparse import OptionParser, Option, OptionValueError
#from Tools.MyAnalysisTools.color_tools import *



if __name__     ==  "__main__":


    parser = OptionParser()
    parser.add_option("-t", "--tag", dest="tag",
                      help="tag name", type="str", metavar="<tag>")


    #    parser.add_option("--no-edm", action="store_true",dest="noedm",default=False, help="use on non-edm files")
    (options, args) = parser.parse_args()      


    baseDir = args[0]
    if baseDir[len(baseDir)-1] != '/':
        baseDir += '/'

    filenames = []
    
    ls_cmd = 'ls ' + baseDir
    ls_out = commands.getstatusoutput(ls_cmd)
    if ls_out[0] == 0:
        lsLines = ls_out[1].split("\n")
        if len(lsLines) != 0:
            for lsLine in lsLines:
                if 'LSFJOB' in lsLine:
                    filenames.append(baseDir + lsLine + "/STDOUT")
                    #print baseDir + lsLine + "/STDOUT"
    else:
        print ls_out[1]


    listofmodules = []
    path = 1
    if path == 1:
        pathname = 'HLT_Tau2Mu_ItTrack_v1'
        listofmodules.append('hltTriggerType')
        listofmodules.append('hltL1sL1DoubleMu0or33HighQ')
        listofmodules.append('hltTauTo2MuL3Filtered')
        listofmodules.append('hltDisplacedmumuFilterDoubleMuTau2Mu')
        listofmodules.append('hltTau2MuTkMuMuTkFilter')
    else:
        pathname = 'HLT_Tau2Mu_RegPixTrack_v1'
        listofmodules.append('hltTriggerType')
        listofmodules.append('hltL1sL1DoubleMu0or33HighQ')
        listofmodules.append('hltTauTo2MuL3Filtered')
        listofmodules.append('hltDisplacedmumuFilterTauTo2Mu')
        listofmodules.append('hltTauTo2MuTrackFilter')

    nevents = {}
    for module in listofmodules:
        nevents[module] = 0
    read = False
    for fileName in filenames:
        #print fileName
        outFile = file(fileName, "r")
        data = outFile.readlines()
        for line in data:
            if 'Modules in Path: ' + pathname in line:
                read = True
            if 'hltBoolEnd' in line:
                read = False
            if read:
                if 'TrigReport' in line:
                    if len(line.split()) == 8:
                        if line.split()[7] in listofmodules:
                            #print line.split()[7]
                            #print "#events: " + line.split()[4]
                            nevents[line.split()[7]] += int(line.split()[4])
    print pathname
    print nevents

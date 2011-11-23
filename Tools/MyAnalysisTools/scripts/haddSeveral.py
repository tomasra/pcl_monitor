#!/usr/bin/env python

import os
import sys
import commands
from optparse import OptionParser, Option, OptionValueError
from Tools.MyAnalysisTools.color_tools import *



if __name__     ==  "__main__":

    parser = OptionParser()
    parser.add_option("-t", "--tag", dest="tag",
                      help="tag name", type="str", metavar="<tag>")


    #    parser.add_option("--no-edm", action="store_true",dest="noedm",default=False, help="use on non-edm files")
    (options, args) = parser.parse_args()      


    baseDir = args[0]
    if baseDir[len(baseDir)-1] != '/':
        baseDir += '/'

    partialFiles = []
    partialTxtFiles = []
    tag = options.tag

    modulo = 50
    index = 0
    counter = 0
    outfilename = 'haddPartial-' + tag + "-" + str(counter) + '.txt'
    rootfilename =  'haddPartial-' + tag + "-" + str(counter) + '.root'
    outfile = open(outfilename, 'w')
    if "castor" in baseDir:
        protocol = 'root://castorcms/'
        rfdir_cmd = 'rfdir ' + baseDir
        rfdir_out = commands.getstatusoutput(rfdir_cmd)
        if rfdir_out[0] == 0:
            castorLines = rfdir_out[1].split("\n")
            if len(castorLines) != 0:
                for castorFileLine in castorLines:
                    if "root" in castorFileLine:
                        fileName = castorFileLine.split()[8]
                        print str(index) + '- ' + fileName
                        outfile.write(protocol + baseDir + fileName + '\n')
                        if (index % modulo == 0 and index != 0) or index == len(castorLines) - 1:
                            print 'close file: ' + outfilename
                            outfile.close()
                            partialFiles.append(rootfilename)
                            partialTxtFiles.append(outfilename)
                            if index != len(castorLines) - 1:
                                counter += 1
                                outfilename = 'haddPartial_' + tag + "-" + str(counter) + '.txt'
                                rootfilename =  'haddPartial-' + tag + "-" + str(counter) + '.root'
                                outfile = open(outfilename, 'w')
                                print 'open file: ' + outfilename
                            
                        index += 1        
                            
                        # print fileName

        else:
            print rfdir_out[1]

        successfulFileName = "hadd-" + tag + ".txt"
        successfulFile = open(successfulFileName, 'w')
        for idFile in range(0, len(partialFiles)):
            hadd_cmd = "hadd " + partialFiles[idFile] + " @" + partialTxtFiles[idFile] 
            print hadd_cmd
            hadd_out = commands.getstatusoutput(hadd_cmd)
            if hadd_out[0] == 0:
                successfulFile.write(partialFiles[idFile] +'\n') 
            else:
                print hadd_out[1]

        successfulFile.close()
        
        hadd_cmd = "hadd hadd-" + tag + ".root @" + successfulFileName 
        hadd_out = commands.getstatusoutput(hadd_cmd)
        if hadd_out[0] == 0:
            print "done"
        else:
            print hadd_out[1]
                                                

         

        # use root://castorcms//castor/cern.ch/bla/myfile


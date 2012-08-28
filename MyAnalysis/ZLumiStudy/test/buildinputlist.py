#!/usr/bin/env python

import os
import sys
import commands
import shutil
import time
from optparse import OptionParser, Option, OptionValueError
from ConfigParser import ConfigParser

if __name__     ==  "__main__":
    
    # define the command line options
    parser = OptionParser()

    
    # this tell to the script if we read from castor or eos
    parser.add_option("-s", "--store-type", dest="storage",
                      help="type of storage: castor - eos", type="str", metavar="<storage type>",default="eos")

    # this tell to the script if we read from castor or eos
    parser.add_option("-n", "--name", dest="name",
                      help="name of the file", type="str", metavar="<filename>")


    # this defines the file name forma blabla_#Job_#file_bla.root
    crabMode = True

    (options, args) = parser.parse_args()

    outdir = args[0]
    print outdir
    
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
        print ls_out
        if ls_out[0] == 0:
            eosLines = ls_out[1].split('\n')
            print eosLines
            if len(eosLines) != 0:
                for eosLine in eosLines:
                    if 'root' in eosLine:
                        fileName = eosLine.split()[4]
                        baseName =  os.path.basename(fileName)
                        filenames.append(baseName)
                    else:
                        print "root is not in eosLine"
        else:
            print ls_out[1]
            sys.exit(1)

    elif options.storage == "local":
        ls_cmd = "ls -1 " + outdir
        ls_out = commands.getstatusoutput(ls_cmd)
        if ls_out[0] == 0:
            lsLines = ls_out[1].split('\n')
            if len(lsLines) != 0:
                for lsLine in lsLines:
                    if 'root' in lsLine:
                        fileName = lsLine.split()[0]
                        baseName =  os.path.basename(fileName)
                        filenames.append(baseName)
        else:
            print ls_out[1]
            sys.exit(1)

    else:
        "***Error: storage-type: " + options.storage + " not supported!"
        sys.exit(1)

    #print filenames


    cmsPfn_cmd = "cmsPfn " + outdir
    cmsPfn_out = commands.getstatusoutput(cmsPfn_cmd)
    pfnBase = ""
    if cmsPfn_out[0] == 0:
        pfnBase = cmsPfn_out[1] 
    else:
        print cmsPfn_out[1]
        sys.exit(1)
        
    # write the file
    configfile = open(options.name, 'wb')
    configfile.write('{\n')
    configfile.write('inputDir = TString("' + pfnBase + '");\n')
    for filename in filenames:
        configfile.write('fileBaseNames.push_back("' + filename.split(".")[0]+'");\n')
    configfile.write('}\n')
    configfile.close()

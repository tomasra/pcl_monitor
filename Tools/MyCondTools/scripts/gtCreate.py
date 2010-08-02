#!/usr/bin/env python
import os
import sys
from optparse import OptionParser
import commands
from stat import *
from ConfigParser import ConfigParser
from datetime import datetime





#GTACCOUNT = 
if __name__     ==  "__main__":

    # set the command line options
    parser = OptionParser()

    parser.add_option("--online", action="store_true",dest="online")

    (options, args) = parser.parse_args()
    #print "OPTIONS: ", options
    #print "ARGS: ", args

    # create the top level directory
    logdirname = "log"
    if not os.path.exists(logdirname):
        print " directory", logdirname," doesn't exist: creating it"
        os.mkdir(logdirname)

    logfile  = open (logdirname + '/gtCreationLog.txt', 'a')

    for gt in args:
        if ".conf" in gt:
            gt = gt.rstrip(".conf")
        # the config file is:
        CONFIGFILE = gt + '.conf'

        # if online manipulate the cfg  
        if options.online:
            
            conffile = open(CONFIGFILE, "r")
            inlines = conffile.readlines()
            conffile.close()


            newconffile = open(CONFIGFILE, "w")
            for line in inlines:
                if line.rstrip() == 'connect=sqlite_file:' + gt + '.db':
                    newline = '#' + line
                    line = newline
                elif line.rstrip() == '#connect=oracle://cms_orcon_prod/CMS_COND_31X_GLOBALTAG':
                    # print line
                    line =  line.strip('#')
        
                newconffile.write(line)

            newconffile.close()


        print '--- Create GT: ' + gt
        execstring = 'createglobaltag ' + CONFIGFILE + ' ' + gt
        evaloutands = commands.getstatusoutput(execstring)
        print evaloutands[1]
        today = datetime.today()
        if options.online:
            logfile.write("GT (online) " + gt + " created on: " + str(today) + "\n")
        else:
            logfile.write("GT " + gt + " created on: " + str(today) + "\n")
        print ''



    logfile.close()

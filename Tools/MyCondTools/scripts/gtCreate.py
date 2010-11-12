#!/usr/bin/env python
import os
import sys
from optparse import OptionParser
import commands
from stat import *
from ConfigParser import ConfigParser
from datetime import datetime
import shutil
from Tools.MyCondTools.color_tools import *
from Tools.MyCondTools.gt_tools import *





#GTACCOUNT = 
if __name__     ==  "__main__":

    # set the command line options
    usage = "usage: %prog [options] gt1 gt2 ..."
    version="%prog $Revision: $"
    parser = OptionParser(usage=usage, version=version)

    parser.add_option("-o", "--online", action="store_true",dest="online",help="write to oracle")
    parser.add_option("-r", "--remote", action="store_true",dest="remote",help="run the command in the CMS network")

    (options, args) = parser.parse_args()

    # read the configuration file
    config = ConfigParser()
    config.optionxform = str
    config.read(['GT_branches/Common.cfg'])
    GTSQLITESTORE = config.get('Common','GTStoreArea')
    gtconnstring  = config.get('Common','GTConnectString')
    passwdfile    = config.get('Common','Passwd')


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


            # check that the new GT is not already in oracle
            if gtExists(gt, gtconnstring, passwdfile):
                print error("***Error: GT: " + gt + " is already in oracle: cannot be modified!!!")
                continue



        # the config file is:
        CONFIGFILE = gt + '.conf'

        # if online manipulate the cfg to change the connection string
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

        # actually creates the GT
        print '--- Create GT: ' + gt
        execstring = 'createglobaltag ' + CONFIGFILE + ' ' + gt
        evaloutands = commands.getstatusoutput(execstring)
        today = datetime.today()
        print evaloutands[1]
        print "GT created on: " + str(today)

        # write the log if operation was succesful
        if evaloutands[0] ==0:
            if options.online:
                logfile.write("GT (online) " + gt + " created on: " + str(today) + "\n")
            else:
                logfile.write("GT " + gt + " created on: " + str(today) + "\n")
                # move the sqlite to the store area
                newsqlite = gt + '.db'
                sqlitefile = GTSQLITESTORE+'/'+gt+'.db'
                if os.path.exists(newsqlite):
                    shutil.move(newsqlite, sqlitefile)

        print ''



    logfile.close()

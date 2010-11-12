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


def editConfFileConnect(filename, newfilename, globaltag, newconnect):
    # read the original file
    conffile = open(filename, "r")
    inlines = conffile.readlines()
    conffile.close()

    # create the new file
    newconffile = open(newfilename, "w")
    for line in inlines:
        if line.rstrip() == 'connect=sqlite_file:' + globaltag + '.db':
            newline = '#' + line
            line = newline
        elif line.rstrip() == '#connect=oracle://cms_orcon_prod/CMS_COND_31X_GLOBALTAG':
            # print line
            line =  line.strip('#')
            
        newconffile.write(line)

    newconffile.close()
    return


#GTACCOUNT = 
if __name__     ==  "__main__":

    
    # ---------------------------------------------------------
    # --- read command line options
    # description
    usage = "usage: %prog [options] gt1 gt2 ..."
    revision = '$Revision: 1.4 $'
    vnum = revision.lstrip('$Revision: ').rstrip(' $')
    version="%prog version: " + vnum
    description = "Create one or more GTs starting from the conf file. The destination can be an sqlite or can be modified to write to oracle"

    # instantiate the parser
    parser = OptionParser(usage=usage, version=version, description=description)

    # set the command line options
    parser.add_option("-o", "--online", action="store_true",dest="online",help="write to oracle")
    parser.add_option("-r", "--remote", action="store_true",dest="remote",help="run the command in the CMS network")

    # read options and arguments
    (options, args) = parser.parse_args()

    # ---------------------------------------------------------
    # --- read the configuration file
    config = ConfigParser()
    config.optionxform = str
    config.read(['GT_branches/Common.cfg'])
    GTSQLITESTORE          = config.get('Common','GTStoreArea')
    gtconnstring           = config.get('Common','GTConnectString')
    passwdfile             = config.get('Common','Passwd')
    remotedir              = config.get('Common','cmsArea')
    remoteversion          = config.get('Common','cmsCMSSWVersion')
    remotemachine          = config.get('Common','cmsMachine')
    # ---------------------------------------------------------
    # --- create log file if needed and open it
    logdirname = "log"
    if not os.path.exists(logdirname):
        print " directory", logdirname," doesn't exist: creating it"
        os.mkdir(logdirname)



    # ---------------------------------------------------------
    # --- create the GT list
    gtlist = []
    for gt in args:
        if ".conf" in gt:
            gt = gt.rstrip(".conf")

        # check that the new GT is not already in oracle
        if gtExists(gt, gtconnstring, passwdfile):
            print error("***Error: GT: " + gt + " is already in oracle: cannot be modified!!!")
        elif not os.path.exists(gt+".conf"):
            print error("***Error: GT: " + gt + " doesn't have a conf file!!!")
        else:
            gtlist.append(gt)

    # ---------------------------------------------------------
    # --- if exectution is remote just send the command over ssh
    if options.remote:
        remote_cmd = "ssh " + remotemachine + ' "cd ' + remotedir + remoteversion + '/src/; source env.sh; gtCreate.py'
        if options.online:
            remote_cmd += " --online"
        for gt in gtlist:
            remote_cmd += " " + gt
        remote_cmd += '"'
        #print remote_cmd
        
        statandout = commands.getstatusoutput(remote_cmd)
        print statandout[1]
        if statandout[0] == 0:

            # parse the output and log
            logfile  = open (logdirname + '/gtCreationLog.txt', 'a')
            listoflines = statandout[1].split('\n')
            gtDates = dict
            for line in listoflines:
                # line = "GT TEST01 created on: 2010-11-12 14:31:16.442039"
                if "created on" in line:
                    gtname = line.split(" ")[1]
                    gtday = line.split(" ")[4]
                    gttime = line.split(" ")[5]
                    print gtname + " " + gtday + " " + gttime
                    if options.online:
                        logfile.write("GT (oracle) " + gtname + " created on: " + gtday + " " + gttime + "\n")
                    else:
                        logfile.write("GT " + gtname + " created on: " + gtday + " " + gttime + "\n")
            logfile.close()
            sys.exit(0)
        else:
            sys.exit(1)
    # ---------------------------------------------------------
    # --- actually run the creation part
    for gt in gtlist:

        # the config file is:
        CONFIGFILE = gt + '.conf'

        # if online manipulate the cfg to change the connection string
        if options.online:
            editConfFileConnect(CONFIGFILE, CONFIGFILE, gt, "")

        # actually creates the GT
        print '--- Create GT: ' + gt
        execstring = 'createglobaltag ' + CONFIGFILE + ' ' + gt
        evaloutands = commands.getstatusoutput(execstring)
        today = datetime.today()
        print evaloutands[1]
        print "GT " + gt + " created on: " + str(today)

        # write the log if operation was succesful
        logfile  = open (logdirname + '/gtCreationLog.txt', 'a')
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


    

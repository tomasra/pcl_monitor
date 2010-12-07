#!/usr/bin/env python

import os
import sys
from optparse import OptionParser, Option, OptionValueError
import commands
#from datetime import date

from Tools.MyCondTools.color_tools import *
from Tools.MyCondTools.gt_tools import *


from ConfigParser import ConfigParser



if __name__     ==  "__main__":
    parser = OptionParser()

    parser.add_option("-r", "--release", dest="releases",
                      help="CMSSW release cycle", type="str",
                      metavar="<release>",action="append")

    parser.add_option("-t", "--tag", dest="tags",
                      help="tag name", type="str",
                      metavar="<tag>",action="append")

    parser.add_option("-c", "--connect", dest="connects",
                      help="connect string", type="str",
                      metavar="<connect>",action="append")
    

    
    (options, args) = parser.parse_args()
    

    # read a global configuration file
    cfgfile = ConfigParser()
    cfgfile.optionxform = str



    CONFIGFILE = "GT_branches/Common.cfg"
    print 'Reading configuration file from ',CONFIGFILE
    cfgfile.read([ CONFIGFILE ])

    # get the releases currently managed
    swBaseDir         = cfgfile.get('Common','cmsswBaseArea')
    swScramArch       = cfgfile.get('Common','scramArch')
    passwd             = cfgfile.get('Common','Passwd')



    objects = args

    for cycle in options.releases:
        # get the list of available release
        releases = getReleaseList('pre,final')
        #print releases
        maxRel = getLastRelease(releases, cycle)
        print maxRel    
        # get list of plugin libraries
        objectRecords = getObjectsAndRecords(swBaseDir, swScramArch, maxRel)    


        for obj in objects:
            if obj in objectRecords:
                print "--- Release: " + cycle
                print "    Obj: " + obj
                for j in range(0, len(objectRecords[obj])):
                    rcd = objectRecords[obj][j]
                    print "            [" + str(j) + "] rcd: " + rcd

        for i in range(0, len(options.tags)):
            listiovout = listIov(options.connects[i], options.tags[i], passwd)
            obj = ""
            if listiovout[0] == 0:
                iovtable = IOVTable()
                iovtable.setFromListIOV(listiovout[1])
                obj = iovtable.containerName()
            else:
                print listiovout[1]
                sys.exit(1)

            if obj in objectRecords:
                print "--- Release: " + cycle
                print "    Tag: " + options.tags[i] + " connect: " + options.connects[i]
                print "    Obj: " + obj
                for j in range(0, len(objectRecords[obj])):
                    rcd = objectRecords[obj][j]
                    print "            [" + str(j) + "] rcd: " + rcd
            else:
                print "   Obj: " + obj + " not found!"
            #print tag

            #def listIov(connect, tag, passwd):


             
#     for obj in args:
#         for 
#         print objectRecords
#         print "AlignmentSurfaceDeformations: rcds -> "
#         print objectRecords["AlignmentSurfaceDeformations"]

        





#foreach plug ($CMSSW_RELEASE_BASE/lib/$SCRAM_ARCH/pluginCondCore*Plugins.so )
#>> nm -C $plug | grep "vtable for DataProxy<" | sed "s/^.* DataProxy<//g" | sed 's/>$//g'
#>> end

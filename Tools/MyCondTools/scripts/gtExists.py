#!/usr/bin/env python

import os
import sys
from optparse import OptionParser, Option, OptionValueError
#import coral
#from CondCore.TagCollection import Node,tagInventory,CommonUtils,entryComment

# tools for color printout
from Tools.MyCondTools.color_tools import *
from Tools.MyCondTools.gt_tools import *

from ConfigParser import ConfigParser
    
if __name__     ==  "__main__":
    parser = OptionParser()
    (options, args) = parser.parse_args()

    # read a global configuration file
    cfgfile = ConfigParser()
    cfgfile.optionxform = str

    CONFIGFILE = "GT_branches/Common.cfg"
    print 'Reading configuration file from ',CONFIGFILE
    cfgfile.read([ CONFIGFILE ])

    # get the releases currently managed
    gtconnect         = cfgfile.get('Common','GTConnectString')
    authpath             = cfgfile.get('Common','Passwd')
    # authpath  = "/afs/cern.ch/cms/DB/conddb"

    for globaltag in args:
        if gtExists(globaltag, gtconnect, authpath):
            print "GT: " + globaltag + ' ' + ok("IS") + " already in oracle!"
        else:
            print "GT: " + globaltag + ' ' + error("NOT") + " in oracle!"

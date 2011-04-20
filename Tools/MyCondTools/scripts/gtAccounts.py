#!/usr/bin/env python

import os
import sys
from ConfigParser import ConfigParser
from copy import copy
from optparse import OptionParser, Option, OptionValueError
#import coral
#from CondCore.TagCollection import Node,tagInventory,CommonUtils,entryComment
from operator import itemgetter


import commands

# tools for color printout
from Tools.MyCondTools.color_tools import *
from Tools.MyCondTools.gt_tools import *
from Tools.MyCondTools.odict import *



if __name__     ==  "__main__":

    # ---------------------------------------------------------
    # --- set the command line options
    parser = OptionParser()

    
    
    #    parser.add_option("-t", "--globaltag", dest="gt",
    #                      help="Global-Tag", type="str", metavar="<globaltag>")
    #parser.add_option("--local", action="store_true",dest="local",default=False)

    (options, args) = parser.parse_args()

    
    # read a global configuration file
    cfgfile = ConfigParser()
    cfgfile.optionxform = str


    # FIXME: configure this
    CONFIGFILE = "GT_branches/Common.cfg"
    print 'Reading configuration file from ',CONFIGFILE
    cfgfile.read([ CONFIGFILE ])

    # get the releases currently managed
    known_releases         = cfgfile.get('Common','Releases').split(',')
    gtconnstring           = cfgfile.get('Common','GTConnectString')
    passwdfile             = cfgfile.get('Common','Passwd')
    swBaseDir              = cfgfile.get('Common','cmsswBaseArea')
    swScramArch            = cfgfile.get('Common','scramArch')

    # read the cfg file containing comments
    commentfile = ConfigParser(dict_type=OrderedDict)
    commentfile.optionxform = str
    COMMENTFILENAME = "GT_branches/Comments.cfg"


    # ---------------------------------------------------------------------------
    # --- check options and expand wildcards and aliases


    accountlist = []
    for gt in args:
        print gt
        filename = gt + ".conf"
        tagCollection = GTEntryCollection()
        # fill the collection
        fillGTCollection(filename, gt, tagCollection)
        for tagentry in tagCollection._tagList :
            if not tagentry.account() in accountlist:
                accountlist.append(tagentry.account())
    

    # --------------------------------------------------------------------------
    accountlist.sort()
    #print accountlist

    for account in accountlist:
        print account

    
    sys.exit(0)



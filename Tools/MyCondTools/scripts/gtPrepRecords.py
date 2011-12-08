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

    
    
    #     parser.add_option("-c", "--compare-to-list", dest="list",
    #                       help="list to compare with", type="str", metavar="<list-file>")
    #     parser.add_option("--local", action="store_true",dest="local",default=False)

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

    accountmap = {}
    for gt in args:
        print gt
        filename = gt + ".conf"
        tagCollection = GTEntryCollection()
        # fill the collection
        fillGTCollection(filename, gt, tagCollection)
        for tagentry in tagCollection._tagList :
            if tagentry.isInPrepAccount():
                if tagentry.account() not in accountmap:
                    accountmap[tagentry.account()] = list()
                # map the entryes by account
                accountmap[tagentry.account()].append(tagentry)
    

    # --------------------------------------------------------------------------
    for account in accountmap.keys():
        taglist = list()
        print "------- Account:",account
        for tag in accountmap[account]:
            if not tag.tagName() in taglist:
                taglist.append(tag.tagName())
                print '       tag:',tag.tagName(),"\t\tobj:",tag._object
            

    sys.exit(0)





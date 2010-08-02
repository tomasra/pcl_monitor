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

    # set the command line options
    parser = OptionParser()

    
    parser.add_option("-s", "--scenario", dest="scenario",
                      help="GT scenario: ideal - mc - startup - data - craft09",
                      type="str", metavar="<scenario>",action="append")
    parser.add_option("-r", "--release", dest="releases",
                      help="CMSSW release", type="str",
                      metavar="<release>",action="append")
    # to substitute a tag or a record you need to specify one of these
    parser.add_option("-t", "--tag", dest="oldtag",
                      help="tag", type="str", metavar="<tag>",default="NONE")
    parser.add_option("--rcd", dest="record",
                      help="record and optionally label", type="str", metavar="<record>[,<label>]",default="NONE")
    

    parser.add_option("--new-tag", dest="newtag",
                      help="new tag", type="str", metavar="<new-tag>",default="NONE")
    parser.add_option("--new-connect", dest="newconnect",
                      help="new connect", type="str", metavar="<new-connect>",default="NONE")
    parser.add_option("--new-account", dest="newaccount",
                      help="new account", type="str", metavar="<new-account>",default="NONE")
    parser.add_option("--new-rcd", dest="newrecord",
                      help="new record", type="str", metavar="<new-record>",default="NONE")
    parser.add_option("--new-object", dest="newobject",
                      help="new object", type="str", metavar="<new-object>",default="NONE")
    parser.add_option("--new-leaf", dest="newleaf",
                      help="new leaf", type="str", metavar="<new-leaf>",default="NONE")
    parser.add_option("--new-label", dest="newlabel",
                      help="new label", type="str", metavar="<new-label>",default="")



    parser.add_option("-c", "--comment", dest="comment",
                      help="comment", type="str", metavar="<comment>",default="NONE")

    
    parser.add_option("--list", action="store_true",dest="list",default=False)
    parser.add_option("--check", action="store_true",dest="check",default=False)
    parser.add_option("--reset", action="store_true",dest="reset",default=False)
    
    
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
    known_releases = cfgfile.get('Common','Releases').split(',')
    # wild-card for releases
    if 'all' in options.releases:
        options.releases = known_releases

    # read the cfg file containing comments
    commentfile = ConfigParser(dict_type=OrderedDict)
    commentfile.optionxform = str
    COMMENTFILENAME = "GT_branches/Comments.cfg"
    # cvs update 
    outandstat = commands.getstatusoutput("cd GT_branches/; cvs update -A Comments.cfg")
    if outandstat[0] != 0:
        print outandstat[1]
    print 'Reading updated comment file from ',COMMENTFILENAME
    commentfile.read([ COMMENTFILENAME ])

    # ---------------------------------------------------------------------------
    # --- check options and expand wildcards and aliases

    # force comments to be added for new tags
    if options.newtag != 'NONE' and options.comment == 'NONE':
        # check that the comment has not yet been entered
        if not commentfile.has_option("TagComments",options.newtag):
            print warning("***Warning") + " no comments for tag: " + options.newtag

    if 'all' in options.scenario:
        options.scenario = ['DESIGN','MC','START',"GR_R","CRAFT09"]
    elif 'mc' in options.scenario:
        options.scenario = ['DESIGN','MC','START']
 
    basedir = "GT_branches/"
    gtConfList = []

    #print "------------------------"
    for gttype in options.scenario:
        for release in options.releases:
            print "--- Scenario: " + gttype + " release: " + release
            gtConf = 'GT_' + release + "_" + gttype + ".cfg"
            CONFIGFILE = basedir + gtConf            
            if os.path.isfile(CONFIGFILE):
                print '    configuration file: ',CONFIGFILE
                gtConfList.append(CONFIGFILE)
            else:
                print "    cfg: " + CONFIGFILE + " doesn't exist!"



    # loop on the configuration files and update them
    for cfg in gtConfList:
        if not os.path.isfile(cfg):
            print "Cfg: " + CONFIGFILE + " doesn't exist!"
            sys.exit(1)
            

        diffconfig = ConfigParser(dict_type=OrderedDict)
        diffconfig.optionxform = str

        print "---------------------------------------------------------------"
        print 'Reading configuration file from ',cfg
        diffconfig.read(cfg)

        #print "FILENAME: " + diffconfig.filename

        # get the old GT name
        OLDGT = diffconfig.get('Common','OldGT')
        oldfilename = OLDGT + '.conf'
        print "--- GT: " + OLDGT
        # create the collection of tags
        tagCollection = GTEntryCollection()

        # --------------------------------------------------------------------------
        fillGTCollection(oldfilename, OLDGT, tagCollection)

        if options.oldtag != "NONE" or options.record != "NONE":
            oldentry = GTEntry()
            # build the record ID
            if options.record != "NONE":
                rcdandlbl = options.record.split(',')
                if len(rcdandlbl) == 1:
                    rcdandlbl.append('')
                rcdId = RcdID ([rcdandlbl[0],rcdandlbl[1]])
                if not tagCollection.hasRcdID(rcdId):
                    print str(rcdId) + " not found in this GT"
                    continue
                oldentry = tagCollection.getByRcdID(rcdId)
            elif options.oldtag != "NONE":
                # check that the tag/record is in the GT
                if not tagCollection.hasTag(options.oldtag):
                    print "tag " + options.oldtag + " not found in this GT"
                    continue
                # get the old entry for this tag
                oldentry = tagCollection.getByTag(options.oldtag)

            if options.list:
                # some useful printout for this tag
                print " -- List: " + str(oldentry)
                print "     cfg string:"
                print "     " + oldentry.getCfgFormat()
            elif options.newtag != 'NONE' or  options.newconnect != 'NONE' or  options.newaccount != 'NONE':
                newentry = oldentry
                if  options.newtag != 'NONE':
                    newentry.setTagName(options.newtag)
                if options.newconnect != 'NONE':
                    newentry.setConnect(options.newconnect)
                if options.newaccount != 'NONE':
                    newentry.setAccount(options.newaccount)
                # check the tag
                isOnline = False
                if  diffconfig.get('Common','Environment') != 'offline':
                    isOnline = True
                passwdfile =  diffconfig.get('Common','Passwd')
                gttype =  diffconfig.get('Common','GTType')
                outputAndStatus = listIov(newentry.getOraclePfn(isOnline), newentry.tagName(), passwdfile)
                if outputAndStatus[0] != 0:
                    print ' -----'
                    print error("***Error:") + " list IOV failed for tag: " + str(newentry)
                    print outputAndStatus[1]
                    print ''
                    sys.exit(1)
                else:
                    iovtable = IOVTable()
                    iovtable.setFromListIOV(outputAndStatus[1])
                    iovtable.checkConsitency(gttype)
                    print "tag check: done"
                diffconfig.set('AddRecord',newentry.tagName(), newentry.getCfgFormat())
                # write the comment to the file
                if options.comment != 'NONE':
                    if options.newtag != 'NONE':
                        if (not commentfile.has_option("TagComments",options.newtag)):
                            # this is a comment saved in the central file since associated to a tag
                            commentfile.set("TagComments",options.newtag,options.comment)
                    else:
                        # this comment is added only to the particular scenario file
                        prevcomment = diffconfig.get("Comments", "Changes")
                        diffconfig.set("Comments", "Changes",prevcomment + "<br> - " + options.comment)

                configfile = open(cfg, 'wb')
                diffconfig.write(configfile)

            if options.check:
                isOnline = False
                if  diffconfig.get('Common','Environment') != 'offline':
                    isOnline = True
                passwdfile =  diffconfig.get('Common','Passwd')
                gttype =  diffconfig.get('Common','GTType')
                print "--- list IOV: " 
                outputAndStatus = listIov(oldentry.getOraclePfn(isOnline), oldentry.tagName(), passwdfile)
                print outputAndStatus[1]
        elif options.reset:
            
            print warning("*** Warning, reset GT conf file: " + cfg)
            confirm = raw_input('Proceed? (y/N)')
            confirm = confirm.lower() #convert to lowercase
            if confirm != 'y':
                continue

            print "Resetting: " + cfg
            
            newconfig = ConfigParser(dict_type=OrderedDict)
            newconfig.optionxform = str
            # starting tag
            newconfig.add_section("Common")
            newconfig.set("Common",'OldGT', diffconfig.get('Common','NewGT'))
            newconfig.set("Common",'NewGT', 'PIPPO')
            newconfig.set("Common",'Passwd', diffconfig.get('Common','Passwd'))
            newconfig.set("Common",'Environment', diffconfig.get('Common','Environment'))
            newconfig.set("Common",'GTType', diffconfig.get('Common','GTType'))
            
            newconfig.add_section("Tags")
            newconfig.add_section("Connect")
            newconfig.add_section("Account")
            newconfig.add_section("AddRecord")
            newconfig.add_section("RmRecord")

            newconfig.add_section("TagManipulation")
            newconfig.set("TagManipulation",'check', 'new')

            newconfig.add_section("Comments")
            newconfig.set("Comments","Release",diffconfig.get("Comments","Release"))
            newconfig.set("Comments","Scope",diffconfig.get("Comments","Scope"))
            newconfig.set("Comments","Changes",'')

            

            
        else:
            # no old entry is specified: a new tag must be created from command line options
            if options.newtag == 'NONE' or options.newconnect == 'NONE' or options.newaccount == 'NONE' or options.newobject == 'NONE' or options.newrecord == 'NONE'  or options.newleaf == 'NONE':
                print error("***Error:") + " specify <newtag> <newrecord> <newconnect> <newaccount> <newobject> <newleaf> [ <newlabel> ] to create a new entry!"
                sys.exit(1)

            # create the new entry
            newentry = GTEntry()
            newentry.setEntry( options.newtag, 'Calibration', options.newconnect,
                              options.newaccount, options.newobject, options.newrecord,
                              options.newleaf, options.newlabel)
            # check the tag
            isOnline = False
            if  diffconfig.get('Common','Environment') != 'offline':
                isOnline = True
            passwdfile =  diffconfig.get('Common','Passwd')
            gttype =  diffconfig.get('Common','GTType')
            outputAndStatus = listIov(newentry.getOraclePfn(isOnline), newentry.tagName(), passwdfile)
            if outputAndStatus[0] != 0:
                print ' -----'
                print error("***Error:") + " list IOV failed for tag: " + str(newentry)
                print outputAndStatus[1]
                print ''
                sys.exit(1)
            else:
                iovtable = IOVTable()
                iovtable.setFromListIOV(outputAndStatus[1])
                iovtable.checkConsitency(gttype)
                print "tag check: done"

            diffconfig.set('AddRecord',newentry.tagName(), newentry.getCfgFormat())
                
            print newentry



            # write the comment to the file
            if options.comment != 'NONE':
                if options.newtag != 'NONE':
                    if (not commentfile.has_option("TagComments",options.newtag)):
                        # this is a comment saved in the central file since associated to a tag
                        commentfile.set("TagComments",options.newtag,options.comment)
                else:
                    # this comment is added only to the particular scenario file
                    prevcomment = diffconfig.get("Comments", "Changes")
                    diffconfig.set("Comments", "Changes",prevcomment + "<br> - " + options.comment)



        configfile = open(cfg, 'wb')
        if not options.reset:
            diffconfig.write(configfile)
        else:
            newconfig.write(configfile)
            
        # write the comment file
        commfile = open(COMMENTFILENAME, 'wb')
        commentfile.write(commfile)
        # cvs commit
        outandstat = commands.getstatusoutput("cd GT_branches/; cvs commit -m \"\" Comments.cfg")
        if outandstat[0] != 0:
            print outandstat[1]
            

        
# TODO:
# 1. leggi da cfg file
# 4. update del cfg file da cvs e il commit dopo la modifica
# 8. meccanismo per rimuovere un record
# 10. shortcuts per connect string: fprep fprod oprep oprod pprod fonline


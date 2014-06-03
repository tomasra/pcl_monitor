#!/usr/bin/env python

import os
import sys
from ConfigParser import ConfigParser
from copy import copy
from optparse import OptionParser, Option, OptionValueError
#import coral
#from CondCore.TagCollection import Node,tagInventory,CommonUtils,entryComment
from operator import itemgetter
import Tools.MyCondTools.RunInfo as RunInfo


import commands
import calendar

# tools for color printout
from Tools.MyCondTools.color_tools import *
from Tools.MyCondTools.gt_tools import *
from Tools.MyCondTools.odict import *

def dump2XML(gt, pfn, tag, passwd, begin, end = -1):
    scratch = os.environ["SCRATCH"]
    cmscond_cmd = "export TNS_ADMIN=/afs/cern.ch/cms/DB/conddb; cmscond_2XML -c " + pfn + " -t " + tag + " -b " + str(begin) + " -P " + passwd
    if end != -1:
        cmscond_cmd += " -e " + str(end)
    command = "cd " + scratch + " ; " + cmscond_cmd + "; mv " + tag + ".xml " + tag + "_" + gt + ".xml"

    outandstat = commands.getstatusoutput(command)
    if outandstat[0] != 0:
        print outandstat[1]
    return scratch + "/" + tag + "_" + gt + ".xml"

def diffXML(filename1, filename2):
    command = "diff " + filename1 + " " + filename2
    outandstat = commands.getstatusoutput(command)
                  
    difflines  = outandstat[1].split('\n')
    nLines = len(difflines)
    # print self._tagName
    for line in difflines:
        if "root setup=" in line:
            continue
        if "XmlKey name" in line:
            continue
        if "2,3c2,3" in line:
            continue
        if "2c2" in line:
            continue
        if "---" in line:
            continue
        #print line
        return False
    return True

def resetQueue(cfgName, cfgFile, newVersion):
    # print confirmation message
    print fg
    warning("*** Warning, reset GT conf file: " + cfgName)
    confirm = raw_input('Proceed? (y/N)')
    confirm = confirm.lower() #convert to lowercase
    if confirm != 'y':
        return

    print "Resetting: " + cfgName
            
    newconfig = ConfigParser(dict_type=OrderedDict)
    newconfig.optionxform = str
    # starting tag
    newconfig.add_section("Common")
    newconfig.set("Common",'OldGT', cfgFile.get('Common','NewGT'))

    # new GT name
    newgtname = cfgFile.get('Common','NewGT').split('_V')[0] + '_V' + newVersion

    if newgtname == cfgFile.get('Common','NewGT'):
        print "New tag : " + newgtname + " equal to old tag: " + cfgFile.get('Common','NewGT') + " skipping the reset"
        return
            
    newconfig.set("Common",'NewGT', newgtname)
    newconfig.set("Common",'Passwd', cfgFile.get('Common','Passwd'))
    newconfig.set("Common",'Environment', cfgFile.get('Common','Environment'))
    newconfig.set("Common",'GTType', cfgFile.get('Common','GTType'))
            
    newconfig.add_section("Tags")
    newconfig.add_section("Connect")
    newconfig.add_section("Account")
    newconfig.add_section("AddRecord")
    newconfig.add_section("RmRecord")

    newconfig.add_section("TagManipulation")
    newconfig.set("TagManipulation",'check', 'new')

    newconfig.add_section("Comments")
    newconfig.set("Comments","Release",cfgFile.get("Comments","Release"))
    newconfig.set("Comments","Scope",cfgFile.get("Comments","Scope"))
    newconfig.set("Comments","Changes",'')
    
    newconfig.add_section("Pending")
    if cfgFile.has_section("Pending"):
        for item in cfgFile.items("Pending"):
            newconfig.set("Pending",item[0],item[1])
            
            
    # write the file
    configfile = open(cfgName, 'wb')
    newconfig.write(configfile)
    configfile.close()
    cvsCommit(cfgName,'reset for new GT')
    return


def getEntryByTag(gtCollection, tagName, entry):
    if not tagCollection.hasTag(tagName):
        print warning("***Warning ") + "tag " + tagName + " not found in this GT"
        return False
    # get the old entry for this tag
    print tagCollection.getByTag(tagName)
    entry = tagCollection.getByTag(tagName)
    print entry
    return True


def getEntryByRcd(gtCollection, rcdAndLabel, entry):
    rcdandlbl = options.record.split(',')
    if len(rcdandlbl) == 1:
        rcdandlbl.append('')
    rcdId = RcdID ([rcdandlbl[0],rcdandlbl[1]])
    if not tagCollection.hasRcdID(rcdId):
        print warning("***Warning ") + str(rcdId) + " not found in this GT"
        return False
    print tagCollection.getByRcdID(rcdId)
    entry = tagCollection.getByRcdID(rcdId)
    print entry
    return True

def checkIOV(newentry, gttype, isOnline, passwd):              
    # list IOV            
    outputAndStatus = listIov(newentry.getOraclePfn(isOnline), newentry.tagName(), passwd)
    if outputAndStatus[0] != 0:
        print ' -----'
        print error("***Error:") + " list IOV failed for tag: " + str(newentry)
        print "         account: " + newentry._account
        print outputAndStatus[1]
        print ''
        sys.exit(1)
    else:
        iovtable = IOVTable()
        iovtable.setFromListIOV(outputAndStatus[1])
        iovtable.checkConsitency(gttype)
        print "tag check: done"


if __name__     ==  "__main__":

    # ---------------------------------------------------------
    # --- set the command line options
    parser = OptionParser()

    parser.add_option("--dump", action="store_true",dest="dump",default=False, help="dump the entry in the GT")
    parser.add_option("--account", action="store_true",dest="checkaccount",default=False, help="check also the account name")
    parser.add_option("--ignore-suffix", action="append",dest="ignoredsuffixes",default=[], help="add an account suffix to the list of ignored suffixes (for archival accounts)")
    
    parser.add_option("--frontier", action="store_true",dest="frontier",default=False, help="use frontier instead of oracle")
    
    parser.add_option("-r", "--run-number", dest="runnumber",
                      help="run #: determines which IOV to dump. If not specified the last IOV + 1 will be used.",
                      type="int", metavar="<run #>")

    (options, args) = parser.parse_args()

    print args
    
    # read a global configuration file
    cfgfile = ConfigParser()
    cfgfile.optionxform = str


    # FIXME: configure this
    CONFIGFILE = "GT_branches/Common.cfg"
    print 'Reading configuration file from ',CONFIGFILE
    cfgfile.read([ CONFIGFILE ])
    passwdfile             = cfgfile.get('Common','Passwd')
    gtconnstring           = cfgfile.get('Common','GTConnectString')

    runinfotag = 'runinfo_31X_hlt' # FIXME: get it from the cfg


    globaltag1 = args[0]
    sqlite_name = args[1]    
    # print "Compare "
    # print "      GT 1: " + globaltag1 + " with GT 2: " + globaltag2

    filename1 = globaltag1 + '.conf'


    # create the collection of tags
    tagCollection1 = GTEntryCollection()

    # --------------------------------------------------------------------------
    # fill the collection
    if not confFileFromDB(globaltag1, filename1, gtconnstring, passwdfile):
        print error("*** Error" + " original GT conf file: " + filename1 + " doesn't exist!")
        sys.exit(5)

    fillGTCollection(filename1, globaltag1, tagCollection1)



    print "    GT 1: " + globaltag1 + " has " + str(tagCollection1.size()) + " entries"

    # loop over all records and compare the tag names and the # of payloads
    
    for entry1 in tagCollection1._tagList:
        
        #print entry1
        statandout = exportIov("oracle://cms_orcon_adg/"+entry1.account(), entry1.tagName(),sqlite_name,passwdfile)
        if statandout[0] == 0:
            print "export successful for ", entry1
            newEntry = entry1
            newEntry._pfn = sqlite_name
            newEntry._account = ''
            newEntry._connstring = sqlite_name

            #tagCollection1.modifyEntryConnection(entry1.tagName(),sqlite_name)
            tagCollection1.replaceEntry(newEntry)


    tagCollection1.dumpToConfFile(globaltag1+"_NEW.conf", globaltag1, "PIPPO", sqlite=sqlite_name)
    

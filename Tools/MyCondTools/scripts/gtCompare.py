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
    globaltag2 = args[1]
    
    # print "Compare "
    # print "      GT 1: " + globaltag1 + " with GT 2: " + globaltag2

    filename1 = globaltag1 + '.conf'
    filename2 = globaltag2 + '.conf'

    # create the collection of tags
    tagCollection1 = GTEntryCollection()
    tagCollection2 = GTEntryCollection()

    # --------------------------------------------------------------------------
    # fill the collection
    if not confFileFromDB(globaltag1, filename1, gtconnstring, passwdfile):
        print error("*** Error" + " original GT conf file: " + filename1 + " doesn't exist!")
        sys.exit(5)

    if not confFileFromDB(globaltag2, filename2, gtconnstring, passwdfile):
        print error("*** Error" + " original GT conf file: " + filename2 + " doesn't exist!")
        sys.exit(5)

    fillGTCollection(filename1, globaltag1, tagCollection1)
    fillGTCollection(filename2, globaltag2, tagCollection2)

    recordList =  list(set(tagCollection1._tagByRcdAndLabelId.keys()) | set(tagCollection2._tagByRcdAndLabelId.keys()))



    print "    GT 1: " + globaltag1 + " has " + str(tagCollection1.size()) + " entries"
    print "    GT 2: " + globaltag2 + " has " + str(tagCollection2.size()) + " entries"
    print "    Total number fo records:", len(recordList)

    if options.dump:
        if options.runnumber != None:
            # prepare the IOV to dump also for lumibased and timebased tags
            # build the lumiid
            h = options.runnumber<<32
            lumiid = (h|1)
            # build the timestamp
            try:
                runInfo = RunInfo.getRunInfoStartAndStopTime(runinfotag, '', options.runnumber)

            except Exception as error:
                print "*** Error can not find run: " + str(options.runnumber) + " in RunInfo: " + str(error)
                raise Exception("Error can not find run: " + str(options.runnumber) + " in RunInfo: " + str(error))
            nsec = calendar.timegm(runInfo.getDate(runInfo._startTime).timetuple())
            timeid = nsec<<32
            
    nchanges = 0

    if len(options.ignoredsuffixes) != 0:
        print "will ognore the following account suffixes: ", options.ignoredsuffixes

    
    # loop over all records and compare the tag names and the # of payloads
    for rcdId in recordList:
        entry1 = None
        if not tagCollection1.hasRcdID(rcdId):
            print blue(str(rcdId))
            print "     not in GT 1!!!"
            continue
        else:
            entry1 = tagCollection1.getByRcdID(rcdId)

        entry2 = None
        if not tagCollection2.hasRcdID(rcdId):
            print blue(str(rcdId))
            print "     not in GT 2!!!"
            continue
        else:
            entry2 = tagCollection2.getByRcdID(rcdId)
            
        account1 = entry1.account()
        account2 = entry2.account()

        if len(options.ignoredsuffixes) != 0:
            if account1.split('_')[-1] in options.ignoredsuffixes:
                separator = '_'
                account1 = separator.join(account1.split('_')[:-1])
            if account2.split('_')[-1] in options.ignoredsuffixes:
                separator = '_'
                account2 = separator.join(account2.split('_')[:-1])

            
        if entry1.tagName() != entry2.tagName() or (account1 != account2 and options.checkaccount):

            match = False

            if options.dump:
                pfn1 = entry1.getOraclePfn(False)
                pfn2 = entry2.getOraclePfn(False)
                if(options.frontier):
                    pfn1 = entry1.pfn()
                    pfn2 = entry2.pfn()

                outputAndStatus1 = listIov(pfn1, entry1.tagName(), passwdfile)
                outputAndStatus2 = listIov(pfn2, entry2.tagName(), passwdfile)

                if outputAndStatus1[0] == 0 and outputAndStatus2[0] == 0: 
                    iovtable1 = IOVTable()
                    iovtable1.setFromListIOV(outputAndStatus1[1]) 
                    lastiov1 = iovtable1.lastIOV()

                    iovtable2 = IOVTable()
                    iovtable2.setFromListIOV(outputAndStatus2[1]) 
                    lastiov2 = iovtable2.lastIOV()


                    # 1 - Check the tokens fo the last IOV
                    if lastiov1.token() == lastiov2.token():
                        match = True

                    # 2 - Dump the last IOV in xml and compare
                    else:                     
                        if entry1.rcdID()[0] != "SiPixelGainCalibrationOfflineRcd" and entry1.rcdID()[0] != "DQMReferenceHistogramRootFileRcd":
                            iovtotest1 = lastiov1.since() + 1
                            iovtotest2 = lastiov2.since() + 1
                            if options.runnumber != None:
                                if iovtable1.timeType() == "runnumber" and iovtable2.timeType() == "runnumber":
                                    iovtotest1 = options.runnumber
                                    iovtotest2 = options.runnumber
                                elif iovtable1.timeType() == "lumiid" and iovtable2.timeType() == "lumiid":
                                    iovtotest1 = lumiid
                                    iovtotest2 = lumiid
                                elif iovtable1.timeType() == "timestamp" and iovtable2.timeType() == "timestamp":
                                    iovtotest1 = timeid
                                    iovtotest2 = timeid

                            endiov = -1
                            if options.runnumber != None:
                                endiov = iovtotest2

                            #print entry1.rcdID()[0]
                            #print iovtotest1
                            #print endiov
                            difffile1 = dump2XML(globaltag1, pfn1, entry1.tagName(), passwdfile, iovtotest1, endiov)
                            difffile2 = dump2XML(globaltag2, pfn2, entry2.tagName(), passwdfile, iovtotest2, endiov)

                            if diffXML(difffile1, difffile2):
                                match = True
                                os.remove(difffile1)
                                os.remove(difffile2)

                        




            

                    
            if not match:
                print blue(str(entry1.rcdID()))
                print "     tag 1: " + entry1.tagName() + " -> 2: " + entry2.tagName()
                if options.checkaccount:
                    print "     account 1: " + entry1.account() + " -> 2: " + entry2.account()
                nchanges += 1
                
             
#         else:
#             # check the # of IOVs
#             outputAndStatus1 = listIov(entry1.pfn(), entry1.tagName(), passwdfile)
#             outputAndStatus2 = listIov(entry2.pfn(), entry2.tagName(), passwdfile)

#             iovtable1 = IOVTable()
#             iovtable1.setFromListIOV(outputAndStatus1[1])

#             iovtable2 = IOVTable()
#             iovtable2.setFromListIOV(outputAndStatus2[1])

#             if iovtable1.size() != iovtable2.size():
#                 print entry1.rcdID()
#                 print "     # IOVs 1: " + str(iovtable1.size()) + " -> 2: " + str(iovtable2.size()) + "   delta = " + str(iovtable2.size() - iovtable1.size())

    print "# of changes: " + str(nchanges)

    
    sys.exit(0)

    

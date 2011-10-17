#!/usr/bin/env python

import os
import sys
from ConfigParser import ConfigParser
from copy import copy
from optparse import OptionParser, Option, OptionValueError
#import coral
#from CondCore.TagCollection import Node,tagInventory,CommonUtils,entryComment
from operator import itemgetter
from datetime import date
import commands

# tools for color printout
from Tools.MyCondTools.color_tools import *
from Tools.MyCondTools.gt_tools import *


def createGTConfiguration(queueCfg, force, gtName):
    # --------------------------------------------------------------------------
    # ---  Parse the configration file
    
    # check that the file exists
    if not os.path.isfile(queueCfg):
        print error("*** Error" + " cfg file: " + queueCfg + " doesn't exist!")
        return 1

    # update for possible modifications
    cvsUpdate(queueCfg)

    diffconfig = ConfigParser()
    diffconfig.optionxform = str

    print 'Reading configuration file from ',queueCfg
    diffconfig.read(['GT_branches/Common.cfg', queueCfg, 'GT_branches/Comments.cfg'])


    # --------------------------------------------------------------------------
    # --- general configuration
    ACCOUNT = 'CMS_COND_31X_GLOBALTAG'
    if diffconfig.has_option('Common','AccountGT'):
        ACCOUNT =  diffconfig.get('Common','AccountGT')

    gtconnstring = diffconfig.get('Common','GTConnectString')

    passwdfile = 'None'
    if diffconfig.has_option('Common','Passwd'):
        passwdfile = diffconfig.get('Common','Passwd')


    OLDGT = diffconfig.get('Common','OldGT')
    NEWGT = diffconfig.get('Common','NewGT')

    if gtName != None:
        print 'Forcing GT name to: ' + gtName
        NEWGT = gtName

    # check that the new GT is not already in oracle
    if gtExists(NEWGT, gtconnstring, passwdfile):
        newfilename = NEWGT + ".conf"
        if(not os.path.exists(newfilename)):
            # get the file from oracle
            print "conf file: " + newfilename + " not found, getting it from oracle!"
            confFileFromDB(NEWGT, newfilename, gtconnstring, passwdfile)
        print error("***Error: GT: " + NEWGT + " is already in oracle: cannot be modified!!!")
        return 2

    isOnline = False
    if diffconfig.has_option('Common','Environment'):
        envir = diffconfig.get('Common','Environment')
        if envir == 'online':
            isOnline = True

    gttype = 'data'
    if diffconfig.has_option('Common','GTType'):
        gttype = diffconfig.get('Common','GTType')
    
    if OLDGT == NEWGT:
        print error("*** Error") + " new and old GT names are the same, old: " + OLDGT + " new: " +  NEWGT
        return 3

    # reads the tags to be substituted and create a dict
    replacetags = dict()
    if diffconfig.has_section('Tags'):
        REPLACETAGS = diffconfig.items('Tags')
        replacetags = dict(REPLACETAGS)

    globalSuffixForTags = ''
    if diffconfig.has_option('Tags','GlobalSuffix'):
        globalSuffixForTags = diffconfig.get('Tags','GlobalSuffix')



    replaceconnect = dict()
    if diffconfig.has_section('Connect'):
        REPLACECONNECT = diffconfig.items('Connect')
        replaceconnect = dict(REPLACECONNECT)

    replaceaccount = dict()
    if diffconfig.has_section('Account'):
        REPLACEACCOUNT = diffconfig.items('Account')
        replaceaccount = dict(REPLACEACCOUNT)


    NEWSUBFIX = ''
    if diffconfig.has_option('Account','GlobalSubfix'):
        NEWSUBFIX = diffconfig.get('Account','GlobalSubfix')


    checkOnTags = 'None'
    if diffconfig.has_option('TagManipulation','check'):
        checkOnTags = diffconfig.get('TagManipulation','check')
        if passwdfile == 'None':
            print error("***Error:") + " need to specify \'Passwd\' in [Common]"
            return 4


    checkOnOnlineConnect = 'None'
    if diffconfig.has_option('TagManipulation','checkOnlineConnect'):
        checkOnOnlineConnect = diffconfig.get('TagManipulation','checkOnlineConnect')


    duplicateTags = 'None'
    duplicateSuffix = ''
    if diffconfig.has_option('TagManipulation','duplicate'):
        duplicateTags = diffconfig.get('TagManipulation','duplicate')
        duplicateSuffix = diffconfig.get('TagManipulation','duplicateSuffix')

    closeIOV = False
    closeIOVTillRun = -1
    if diffconfig.has_option('TagManipulation','closeIOV'):
        if diffconfig.get('TagManipulation','closeIOV') == 'all':
            closeIOVTillRun = diffconfig.get('TagManipulation','closeIOVtoRUN')
            closeIOV = True



    # write the comment file in twiki format
    scope = ''
    release = ''
    changes = ''

    docGenerator = None        
    if diffconfig.has_section('Comments'):
        scope = diffconfig.get('Comments','Scope')
        release = diffconfig.get('Comments','Release')
        changes = diffconfig.get('Comments','Changes')
        docGenerator = GTDocGenerator(NEWGT, OLDGT, scope, release, changes)
        #if diffconfig.has_option('Comments','Class'):
        #    docGenerator.addToBranchList(diffconfig.get('Comments','Class'))
        
        
    # read the new records from cfg
    newentries = []
    if diffconfig.has_section("AddRecord"):
        newrecords = diffconfig.items('AddRecord')
        #print newrecords
        #print "New records to be added:"
        for record in newrecords:
            newentry = GTEntry()
            newentry.setFromCfgLine(record)
            newentries.append(newentry)
            if diffconfig.has_option('TagComments', newentry.tagName()):
                docGenerator.addChange(diffconfig.get('TagComments', newentry.tagName()))
            #print "   " + str(newentry)


    # read Rcd to be removed
    rmentries = []
    if diffconfig.has_section("RmRecord"):
        rmrecords = diffconfig.items('RmRecord')
        for record in rmrecords:
            labels =  record[1].split(',')
            print labels
            for label in labels:
                #label = record[1]
                if record[1] == 'None':
                    label = ''
                rcdId = RcdID([record[0], label])
                rmentries.append(rcdId)


    CONNREP= ''
    if diffconfig.has_option('Connect','GlobalConnectReplace'):
        CONNREP= diffconfig.get('Connect','GlobalConnectReplace')
        #print "- Replacing connect string with: " + CONNREP

    #try:
    #    CONNREP= diffconfig.get('Connect','GlobalConnectReplace')
    #except:
    #    print "  - No \'GlobalConnectReplace\' fount in config file"


    oldfilename = OLDGT + '.conf'
    newconffile  = NEWGT + ".conf"


    if not confFileFromDB(OLDGT, oldfilename, gtconnstring, passwdfile):
        print error("*** Error" + " original GT conf file: " + oldfilename + " doesn't exist!")
        return 5

    if os.path.isfile(newconffile) and not force:
        print warning("*** Warning, the new GT conf file: " + newconffile + " already exists!")
        confirm = raw_input('Overwrite? (y/N)')
        confirm = confirm.lower() #convert to lowercase
        if confirm != 'y':
            return 6



    # create the collection of tags
    tagCollection = GTEntryCollection()


    # --------------------------------------------------------------------------
    fillGTCollection(oldfilename, OLDGT, tagCollection)


    # --------------------------------------------------------------------------
    # manipulate the tag collection according to cfg file

    if(len(replacetags) != 0):
        print "Replace tags:"
        for oldtag, newtag in replacetags.iteritems():
            tagCollection.modifyEntryTag(oldtag, newtag)
            if diffconfig.has_option('TagComments', newtag):
                docGenerator.addChange(diffconfig.get('TagComments', newtag))

    if(len(replaceconnect) != 0):
        print "Replace connect:"
        for tag, connect in replaceconnect.iteritems():
            if tag != 'GlobalConnectReplace':
                tagCollection.modifyEntryConnection(tag, connect)

    if(len(replaceaccount) != 0):
        print "Replace accounts:"
        for tag, account in replaceaccount.iteritems():
            if tag != 'GlobalSubfix':
                tagCollection.modifyEntryAccount(tag, account)

    if(len(newentries) != 0):        
        print "Insert entries:"
        for nentry in newentries:
            tagCollection.insertEntry(nentry)

    if(len(rmentries) != 0):
        print "Remove entries:"
        for rcd in rmentries:
            tagCollection.removeEntry(rcd)


    if(NEWSUBFIX != ''):
        tagCollection.addAccountSubfix(NEWSUBFIX)


    if(CONNREP != ''):
        tagCollection.glbConnectReplace(CONNREP)


    # --------------------------------------------------------------------------
    # the tag collection from now on is up-to-date

    tagstobeappendedwithsubf = []

    if globalSuffixForTags != '':
        print "Will append subfix: " + globalSuffixForTags + ' for all tags!'
        tagstobeappendedwithsubf = tagCollection._tagOrder

    # loop over all entries in the collection
    for tagidx in range(0,len(tagstobeappendedwithsubf)):
        theTag1 = tagCollection._tagList[tagstobeappendedwithsubf[tagidx]]
        oldtag = theTag1._tag
        newtag = oldtag + globalSuffixForTags
        if theTag1._account != 'CMS_COND_31X_FROM21X':
            # change the tag name in the tag collection
            tagCollection.modifyEntryTag(oldtag, newtag)

    tagstobeduplicated = []





    if duplicateTags == 'all':
        print "Will duplicate all tags!"
        tagstobeduplicated = tagCollection._tagOrder
    elif duplicateTags != 'None' :
        for tagname in duplicateTags.split(','):
            tag = tagCollection.getByTag(tagname)
            print "Will duplicate tag: " + str(tag)
            tagstobeduplicated.append(tagCollection._tagByTag[tagname])


    failedToDuplicateTag = []
    falisedToDuplicateIOV = []

    # DUPLICATE
    # loop over all entries in the collection
    for tagidx in range(0,len(tagstobeduplicated)):
        theTag1 = tagCollection._tagList[tagstobeduplicated[tagidx]]
        if theTag1._account == 'CMS_COND_31X_FROM21X':
            continue
        oldtag = theTag1._tag
        newtag = oldtag + duplicateSuffix
        statusandout = duplicateIovTag(theTag1.getOraclePfn(isOnline), oldtag, newtag, passwdfile)
        if statusandout[0] == 0:
            # change the tag name in the tag collection
            tagCollection.modifyEntryTag(oldtag, newtag)
            if closeIOV == True:
                # duplicate the last payload and close the IOV 
                standoutdupl = duplicateIov(theTag1.getOraclePfn(isOnline), newtag, closeIOVTillRun, passwdfile)
                if standoutdupl[0] != 0:
                    falisedToDuplicateIOV.append(theTag1)
        else:
            failedToDuplicateTag.append(theTag1)



    # run checks on tags if requested

    tagstobechecked = []

    if checkOnTags == 'all':
        print '-- Check all tags...'
        tagstobechecked = tagCollection._tagOrder
    if checkOnTags == 'new':
        print '-- Check new/modified tags...'    
        tagstobechecked = tagCollection._newTags

    tagstobecheckedforonlineconn = []
    if checkOnOnlineConnect == 'all':
        print '-- Check all tags for HLT connect...'
        tagstobecheckedforonlineconn = tagCollection._tagOrder
    if checkOnOnlineConnect == 'new':
        print '-- Check new/modified tags for HLT connect...'    
        tagstobecheckedforonlineconn = tagCollection._newTags



    # loop over all entries in the collection
    for tagidx in range(0,len(tagstobechecked)):
        theTag = tagCollection._tagList[tagstobechecked[tagidx]]
        if theTag._account == "CMS_COND_31X_FROM21X":
            #print "skip tag: " + str(theTag)
            continue

        outputAndStatus = listIov(theTag.getOraclePfn(isOnline), theTag._tag, passwdfile)
        if outputAndStatus[0] != 0:
            print ' -----'
            print error("***Error:") + " list IOV failed for tag: " + str(theTag)
            #print outputAndStatus[1]
            print ''
        else:
            iovtable = IOVTable()
            iovtable.setFromListIOV(outputAndStatus[1])
            iovtable.checkConsitency(gttype)
            print '.',

    if len(tagstobechecked) != 0:
        print 'done'



    # loop over all entries in the collection
    for tagidx in range(0,len(tagstobecheckedforonlineconn)):
        theTag = tagCollection._tagList[tagstobecheckedforonlineconn[tagidx]]
        if not theTag.isOnlineConnect():
            print error("***Error ") + str(theTag) + " has connect: " + theTag._connstring


    # printout from tag manipulation:
    if len(failedToDuplicateTag) != 0:
        print "Failed to duplicate the following tags:"
        for tag in failedToDuplicateTag:
            print "   ", tag



    # printout from tag manipulation:
    if len(falisedToDuplicateIOV) != 0:
        print "Failed to duplicate IOV for the following tags:"
        for tag in falisedToDuplicateIOV:
            print "   ", tag


    # Print notifiation of records from prep account
    tagCollection.printTagsInPrep()

    # generate the documentation
    if tagCollection.tagsInPrep():
        docGenerator.isForProd(False)

    # document the last valid run # for a snapshot (reading from runinfo)
    if diffconfig.has_option('Comments','Snapshot'):
        if diffconfig.get('Comments','Snapshot'):
            # we add a worning for the users to the 'Scope' section
            lastvalidrun = -1
            if closeIOV:
                lastvalidrun = closeIOVTillRun
            else:
                # this is a frozen snapshot: take last run from RunInfoRcd
                # FIXME
                runinforcd = RcdID(['RunInfoRcd', ''])
                if tagCollection.hasRcdID(runinforcd):
                    runinfo = tagCollection.getByRcdID(runinforcd)
                    outputAndStatus = listIov(runinfo.getOraclePfn(isOnline), runinfo.tagName(), passwdfile)
                    if outputAndStatus[0] == 0:
                        iovtable = IOVTable()
                        iovtable.setFromListIOV(outputAndStatus[1])
                        lastvalidrun = iovtable.lastIOV().since()
                    else:
                        print outputAndStatus[1]
            docGenerator.snapshotValidity(date.today(), lastvalidrun)


    # write the doc in wiki format
    docGenerator.printWikiDoc()

    # --------------------------------------------------------------------------
    # Write the new conf file

    tagCollection.dumpToConfFile(newconffile,NEWGT,ACCOUNT)
    #------------------------------------------------------------------------------


    cvsCommit(queueCfg, NEWGT)

    print "-----------------------------------------"
    print newconffile+' ready. Please have a look:'
    print "tkdiff " + oldfilename + " " + newconffile + ' &'

    return 0
    



if __name__     ==  "__main__":
    # --------------------------------------------------------------------------
    # --- set the command line options and parse arguments
    parser = OptionParser()

    # this options forces the overwrite of the conf file if it already exists
    parser.add_option("-f","--force",
                      action="store_true",
                      dest="force",
                      help="Forces overwrite of the conf file (if already existing)",
                      default=False)

    parser.add_option("-t", "--global-tag",
                      dest="newgt",
                      help="Overwrite name of the new GT",
                      type="str",
                      metavar="<new GT>")

    (options, args) = parser.parse_args()

    # thsi is the configuration file for the GT branch
    for CONFIGFILE in args:
        returnValue = createGTConfiguration(CONFIGFILE, options.force, options.newgt)
        if returnValue != 0:
            sys.exit(returnValue)
            
    sys.exit(0)
    


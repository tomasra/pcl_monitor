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

# tools for color printout
from color_tools import *

import commands

from gt_tools import *


#if __name__     ==  "__main__":

# set the command line options
parser = OptionParser()

parser.add_option("--force", action="store_true",dest="force",default=False)

parser.add_option("-t", "--global-tag", dest="newgt",
                  help="Overwrite new GT name",
                  type="str", metavar="<new GT>")

# parser.add_option("-s", "--scenario", dest="scenario",
#                   help="GT scenario: ideal - mc - startup - data - craft09",
#                   type="str", metavar="<scenario>",action="append")

(options, args) = parser.parse_args()

# read the configuration file
# CONFIGFILE=sys.argv[1]
CONFIGFILE=args[0]


if not os.path.isfile(CONFIGFILE):
    print error("*** Error" + " cfg file: " + CONFIGFILE + " doesn't exist!")
    sys.exit(1)

diffconfig = ConfigParser()
diffconfig.optionxform = str

print 'Reading configuration file from ',CONFIGFILE
diffconfig.read([ CONFIGFILE, 'GT_branches/Comments.cfg'])

# this is for [COMMON] part of the myconf.conf


#------------------------------------------------------
# general configuration
ACCOUNT = 'CMS_COND_31X_GLOBALTAG'
if diffconfig.has_option('Common','AccountGT'):
    ACCOUNT =  diffconfig.get('Common','AccountGT')

OLDGT = diffconfig.get('Common','OldGT')
NEWGT = diffconfig.get('Common','NewGT')

if options.newgt != None:
    print 'Forcing GT name to: ' + options.newgt
    NEWGT = options.newgt



passwdfile = 'None'
if diffconfig.has_option('Common','Passwd'):
    passwdfile = diffconfig.get('Common','Passwd')

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
    sys.exit(1)

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
        sys.exit(1)


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

# if docGenerator != None:
#     if closeIOV:
#         docGenerator


#     #print "scope: " + scope
#     #print 'release: ' + release
#     #print 'changes: ' + changes
#     if not os.path.exists('doc/'):
#         print " directory \"doc\" doesn't exist: creating it"
#         os.mkdir('doc/')
#     docfilename = 'doc/' + NEWGT + '.wiki'
#     docfile = open(docfilename,'w')
#     docstring = '| [[http://condb.web.cern.ch/condb/listTags/?GlobalTag=' + NEWGT + '][' + NEWGT + ']] | %GREEN%' + release + '%ENDCOLOR% | ' + scope + ' | As !' + OLDGT + ' with the following updates:' + changes + '. |\n'
#     docfile.write(docstring)
#     docfile.close()




# RMTAGS = diffconfig.items('RmTags')
# rmtags = dict(RMTAGS)

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

# check if the original conf file exists
if not os.path.isfile(oldfilename):
    # FIXME: shoud create conf file if it doesn't exist
    print error("*** Error" + " original GT conf file: " + oldfilename + " doesn't exist!")
    sys.exit(1)

if os.path.isfile(newconffile) and not options.force:
    print warning("*** Warning, the new GT conf file: " + newconffile + " already exists!")
    confirm = raw_input('Overwrite? (y/N)')
    confirm = confirm.lower() #convert to lowercase
    if confirm != 'y':
        sys.exit(1)



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

failedToDuplicateTag = []
falisedToDuplicateIOV = []

# DUPLICATE
# loop over all entries in the collection
for tagidx in range(0,len(tagstobeduplicated)):
    theTag1 = tagCollection._tagList[tagstobeduplicated[tagidx]]
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
    outputAndStatus = listIov(theTag.getOraclePfn(isOnline), theTag._tag, passwdfile)
    if outputAndStatus[0] != 0:
        print ' -----'
        print error("***Error:") + " list IOV failed for tag: " + str(theTag)
        print outputAndStatus[1]
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



docGenerator.printWikiDoc()

# --------------------------------------------------------------------------
# Write the new conf file
node = tagCollection.nodedata()
root = tagCollection.parent()
globparent = tagCollection.root()

# open output conf file
conf=open(newconffile,'w')
conf.write('[COMMON]\n')
conf.write('connect=sqlite_file:' + NEWGT + '.db\n')
#conf.write('#connect=oracle://cms_orcoff_int2r/'+ACCOUNT+'\n')
conf.write('#connect=oracle://cms_orcon_prod/'+ACCOUNT+'\n')
conf.write('\n')
conf.write('[TAGINVENTORY]\n')
conf.write('tagdata=\n')
for tagidx in range(0,len(tagCollection._tagOrder)):
    outline = tagCollection._tagList[tagCollection._tagOrder[tagidx]].getTagInvetoryLine()
    if tagidx != len(tagCollection._tagOrder) - 1:
        outline=outline+';'
    outline=outline+'\n'
    conf.write(outline)

conf.write("\n")

conf.write('[TAGTREE '+NEWGT+']\n')

conf.write('root='+root+'\n')
conf.write('nodedata='+node+'{parent='+globparent+'}\n')
conf.write('leafdata=\n')
#counter = 0
for tagidx in range(0,len(tagCollection._tagOrder)):
    outline = tagCollection._tagList[tagCollection._tagOrder[tagidx]].getTagTreeLine()
    #counter = counter + 1
    if tagidx != len(tagCollection._tagOrder) - 1:
        outline=outline+';'
    outline=outline+'\n'
    conf.write(outline)

conf.close()


#------------------------------------------------------------------------------

commitcommand = 'cvs commit -m \"' + NEWGT + '\" ' +  CONFIGFILE
#print commitcommand
statusAndOutput = commands.getstatusoutput(commitcommand)
if statusAndOutput[0] != 0:
    print statusAndOutput[1]


print "-----------------------------------------"
print newconffile+' ready. Please have a look:'
print "tkdiff " + oldfilename + " " + newconffile + ' &'

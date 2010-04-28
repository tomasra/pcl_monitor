#!/usr/bin/env python

import os
import sys
from ConfigParser import ConfigParser
from copy import copy
from optparse import OptionParser, Option, OptionValueError
#import coral
from CondCore.TagCollection import Node,tagInventory,CommonUtils,entryComment
from operator import itemgetter

# tools for color printout
from color_tools import *

import commands


def stripws(myinput):
    result=('').join(myinput.split(' '))
    result=('').join(result.split('\n'))
    return result
def converttagdata(value):
    mytagdata={}
    startbrack=value.find('{')
    endbrack=value.find('}')
    metadatastr=value[startbrack+1:endbrack]
    mytagdata['tagname']=value[0:startbrack]
    metadatalist=metadatastr.split(',')
    for pair in metadatalist:
        mydata=pair.split('=',1)
        mytagdata[mydata[0]]=mydata[1]
    return mytagdata
def converttagcollection(value):
    cleanvalue=stripws(value)
    mytagcollection=[]
    taglist=cleanvalue.split(';')
    for tagdata in taglist:
        mytagcollection.append(converttagdata(tagdata))
    return mytagcollection
def check_tagdata(option, opt, value):
    try:
        return converttagcollection(value)
    except ValueError:
        raise OptionValueError(
            "option %s: invalid tagdata: %r" % (opt, value))

def convertnodedata(mynodevalue):
    mynodedata={}
#    datastr=('').join(value.split(' '))
    startbrack=mynodevalue.find('{')
    endbrack=mynodevalue.find('}')
    metagdatastr=mynodevalue[startbrack+1:endbrack]
    mynodedata['nodelabel']=mynodevalue[0:startbrack]
    metadatalist=metagdatastr.split(',')
    for pair in metadatalist:
        mydata=pair.split('=',1)
        mynodedata[mydata[0]]=mydata[1]
    #print 'mynodedata'
    return mynodedata

def convertnodecollection(value):
    cleanvalue=stripws(value)
    mynodecollection=[]
    nodelist=cleanvalue.split(';')
    for nodedata in nodelist:
        mynodecollection.append(convertnodedata(nodedata))
    return mynodecollection



# python wrappers of cmscon commands

def listIov(connect, tag, passwd):
    listiovCommand = '../bin/slc5_ia32_gcc434/cmscond_list_iov -c ' + connect + '  -t ' + tag
    if passwd != 'None':
        listiovCommand = listiovCommand + ' -P ' + passwd
    statusAndOutput = commands.getstatusoutput(listiovCommand)
    if statusAndOutput[0] != 0:
        print warning("Warning") + ": listiov for tag: " + tag + " failed!"
        print statusAndOutput[1]

    return statusAndOutput




def duplicateIovTag(connect, tag, newtag, passwd):
    statusAndOutput = listIov(connect,tag,passwd)

    if statusAndOutput[0] != 0:
        return statusAndOutput
    
    splitOutput = statusAndOutput[1].split("\n")
    #print splitOutput

    iovLoadFileName = '/tmp/'+ newtag + ".txt"
    iovLoadFile = open(iovLoadFileName, 'w')
    index = 0
    for line in splitOutput:
        if index == 0:
            iovLoadFile.write('Tag '+ newtag + '\n')            
        else:
            iovLoadFile.write(line+'\n')
        index = index + 1
    iovLoadFile.close()
    
    loadiovCommand = '../bin/slc5_ia32_gcc434/cmscond_load_iov -c ' + connect + ' ' + iovLoadFileName
    if passwd != 'None':
        loadiovCommand = loadiovCommand + ' -P ' + passwd

    loadiovStatusAndOutput = commands.getstatusoutput(loadiovCommand)
    if loadiovStatusAndOutput[0] != 0:
        print warning("Warning") + "  loadiov for tag: " + newtag + " failed!\n\n"
        print loadiovStatusAndOutput[1]
        return loadiovStatusAndOutput

    return loadiovStatusAndOutput

    
def duplicateIov(connect, tag, run, passwd):
    duplicateiovCommand = "../bin/slc5_ia32_gcc434/cmscond_duplicate_iov -c " + connect + '  -t ' + tag + ' -f ' + run + ' -s ' + run
    if passwd != 'None':
        duplicateiovCommand = duplicateiovCommand + ' -P ' + passwd

    duplicateiovStatusAndOutput =  commands.getstatusoutput(duplicateiovCommand)
    if duplicateiovStatusAndOutput[0] != 0:
          print warning("Warning") + " duplicate iov for tag: " + tag + " and run " + run + " failed!\n\n"
          print duplicateiovStatusAndOutput[1]

    return duplicateiovStatusAndOutput
          


class GTEntry:
    def __init__(self):
        self._leafnode = ''
        self._parent = ''
        self._tag = ''
        self._object = ''
        self._pfn = ''
        self._account = ''
        self._record = ''
        self._connstring = ''
        self._label = ''
        return

    def __eq__(self, other):
        return  self._leafnode == other._leafnode and self._parent == other._parent and self._tag == other._tag and self._object == other._object and self._pfn == other._pfn and self._account == other._account and self._record == other._record and self._connstring == other._connstring and self._label == other._label 


    def __str__(self):
        return 'tag: \'' + self._tag + "\' " + str(self.rcdID())

    def setFromTagInventoryLine(self, line):
        self._tag = line['tagname']
        self._account = 'CMS_COND'+str(line['pfn']).split('/CMS_COND')[1]
        self._object = line['objectname']
        self._pfn = line['pfn']
        self._record = line['recordname']
        self._connstring = (line['pfn']).split('/CMS_COND')[0]
        if line.has_key('labelname'):
            self._label = line['labelname']
        return

    def setFromTagTreeLine(self, line):
        # check this is the right tag
        if line.has_key('tagname') is False:
            raise ValueError, "***Error: \'tagname\' is not specified for leaf node "+line['nodelabel']

        if line['tagname'] != self._tag:
            raise ValueError, "***Error: leaf: " + line['nodelabel'] + " is not for tag "+ self._tag

        self._leafnode = line['nodelabel']
        
        if not line.has_key('parent'):
            raise KeyError,'***Error: no parent parameter for'+line['nodelabel']
        self._parent = line['parent']
        return

    def setFromCfgLine(self, line):
        newrecorddata = stripws(line[1])
        newrecordcollection = convertnodedata(newrecorddata)
        self._tag = line[0]
        self._parent = 'Calibration'
        self._connstring =newrecordcollection['connect']
        self._account = newrecordcollection['account']
        self._object = newrecordcollection['objectname']
        self._record = newrecordcollection['recordname']
        self._leafnode = newrecordcollection['nodelabel']
        if newrecordcollection.has_key('labelname'):
            self._label = newrecordcollection['labelname']
        else :
            self._label = ''
        self._pfn = newrecordcollection['connect']+'/'+newrecordcollection['account']

        return

    
        
    def printTag(self):
        print 'Tag: ' + self._tag
        return

    def getTagInvetoryLine(self):
        outline = str
        if self._label != '':
            outline = ' '+self._tag+'{pfn='+self._connstring+'/'+self._account+',objectname='+self._object+',recordname='+self._record+',labelname='+self._label+'}'
        else:
            outline=' '+self._tag+'{pfn='+self._connstring+'/'+self._account+',objectname='+self._object+',recordname='+self._record+'}'
        return outline

    def getTagTreeLine(self):
        outline=' '+ self._leafnode+'{parent='+ self._parent+',tagname='+ self._tag+',pfn='+ self._connstring+'/'+ self._account+'}'
        return outline

    def rcdID(self):
        return RcdID([self._record,self._label])

    def setConnect(self, newconn):
        self._connstring = newconn
        self._pfn = self._connstring+'/'+ self._account
        return

    def setAccount(self, account):
        self._account = account
        self._pfn = self._connstring+'/'+ self._account
        return

    def getOraclePfn(self, online):
        if online == False:
            if self._connstring == 'frontier://FrontierProd':
                oracleConn =  'oracle://cms_orcoff_prod'
            elif self._connstring == 'frontier://FrontierPrep':
                oracleConn =  'oracle://cms_orcoff_prep'
        elif online == True:
            if self._connstring == 'frontier://FrontierProd':
                oracleConn =  'oracle://cms_orcon_prod'
            elif self._connstring == 'frontier://FrontierPrep':
                oracleConn =  'oracle://cms_orcoff_prep'
        return oracleConn + '/' + self._account

    def isInPrepAccount(self):
        if self._connstring == 'frontier://FrontierPrep':
            return True
        return False





class RcdID(tuple):
    def __new__(cls, *args, **kw):
        return tuple.__new__(cls, *args, **kw)

    def __str__(self):
        return "rcd: \'" + tuple.__getitem__(self,0) + "\' label: \'" + tuple.__getitem__(self,1) + "\'"










class GTEntryCollection:
    def __init__(self):
        # the actual list of entries
        self._tagList = []
        # mapping by tag
        self._tagByTag = dict()
        # mapping by record-label
        self._tagByRcdAndLabelId = dict()
        # keeps track of the order in the conf file
        self._tagOrder = []
        # bookmarks account to create indexes for new insertions
        self._previousaccount = str()
        # maps the last position for each account to be used for new insertions
        self._accountindexes = dict()
        # global subfix for all accounts
        self._glbAccSubfix = ''
        # list of tags in the prep-account
        self._tagsInPrep = []
        # list of new/modified tags
        self._newTags = []
        return

    def addEntry(self, tag):
        # check if this is already in the collection
        if tag._tag in self._tagByTag or tag.rcdID() in self._tagByRcdAndLabelId:
            print error("***Error"),"adding entry:", tag
            othertagid = -1
            if tag._tag in self._tagByTag:
                othertagid = self._tagByTag[tag._tag]
            else:
                othertagid = self._tagByRcdAndLabelId[tag.rcdID()]
                
            print "     same tag or Record for: ",self._tagList[othertagid]
            print ""
            raise ValueError, "***Error: entry has same tag or RcdId than another one in the collection!" 
        # order is kept
        self._tagList.append(tag)
        # add the entry to the maps
        index = len(self._tagList) - 1
        self._tagByTag[tag._tag] = index
        self._tagByRcdAndLabelId[tag.rcdID()] = index
        self._tagOrder.append(index)
        if tag.isInPrepAccount():
            self._tagsInPrep.append(index)
        # self._newTags.append(index)
        # check where to append the new records
        if tag._account != self._previousaccount:
            # print "Prev account: " + self._previousaccount
            if not self._previousaccount in self._accountindexes:
                if index != 1:
                    self._accountindexes[self._previousaccount] = index - 1
                    # print "Account: " + self._previousaccount + " index: " + str(index - 1)
            self._previousaccount = tag._account

        return

    def getByTag(self, tag):
        return self._tagList[self._tagByTag[tag]]

    def getByRcdID(self, id):
        return self._tagList[self._tagByRcdAndLabelId[id]]

    def hasTag(self, tag):
        return tag in self._tagByTag

    def hasRcdID(self, anid):
        return anid in self._tagByRcdAndLabelId

    def modifyEntryTag(self, oldtag, newtag):
        if self.hasTag(oldtag):
            if newtag in  self._tagByTag:
                raise ValueError, "***Error: replacing tag " + oldtag + " with tag: " + newtag + "already in the collection!" 
            index = self._tagByTag[oldtag]
            self.getByTag(oldtag)._tag = newtag
            print "   " + oldtag + ": " + newtag
            self._tagByTag[newtag] = index
            if not index in self._newTags:
                self._newTags.append(index)
        else:
            print error("*** Warning") + " tag: " + oldtag + " not found!"
        return

    def modifyEntryConnection(self, tag, connection):
        if self.hasTag(tag):
            index = self._tagByTag[tag]
            if connection == 'frontier://FrontierPrep' and not self.getByTag(tag).isInPrepAccount():
                self._tagsInPrep.append(index)

            if  connection != 'frontier://FrontierPrep' and self.getByTag(tag).isInPrepAccount():
                self._tagsInPrep.remove(index)

            if not index in self._newTags:
                self._newTags.append(index)
            self.getByTag(tag).setConnect(connect)
            print "   " + tag + ": " + connect
                
        else:
            print error("*** Warning") + " tag: " + tag + " not found!"
        return

    def modifyEntryAccount(self, tag, account):
        if self.hasTag(tag):
            self.getByTag(tag).setAccount(account)
            index = self._tagByTag[tag]

            if not index in self._newTags:
                self._newTags.append(index)
            print "   " + tag + ": " + account
        else:
            print error("*** Warning") + " tag: " + tag + " not found!"

        return

    def replaceEntry(self, entry):
        if self.hasRcdID(entry.rcdID()) == False:
            raise ValueError, "***Error: replaceEntry called for " + str(entry.rcdID()) + " not in the collection"
        # FIXME: check that the tag is not already the same as in the tag collection
        if entry == self.getByRcdID(entry.rcdID()):
            # print "tag: " + entry._tag + " already in!"
            return
        print "  ", self.getByRcdID(entry.rcdID())._tag+ ": ", entry._tag
        index = self._tagByRcdAndLabelId[entry.rcdID()]
        # get the leaf name from the previous one
        entry._leafnode = self._tagList[index]._leafnode
        entry._parent = self._tagList[index]._parent
        self._tagList[index] = entry
        self._tagByTag[entry._tag] = index

        if not index in self._newTags:
            self._newTags.append(index)

        if entry.isInPrepAccount() and not self._tagList[index].isInPrepAccount():
            self._tagsInPrep.append(index)

        if not entry.isInPrepAccount() and self._tagList[index].isInPrepAccount():
            self._tagsInPrep.remove(index)
        
        return

    def insertEntry(self, entry):
        if self.hasRcdID(entry.rcdID()) == True:
            self.replaceEntry(entry)
        else:
            index = len(self._tagList)
            if entry._account in self._accountindexes:
                # append to the other tags of thsi account
                index = self._accountindexes[entry._account]
                #print "Account: "+ entry._account + " Index: " + str(index)
            self._tagList.append(entry)
            listindx = len(self._tagList) - 1
            self._tagByTag[entry._tag] = listindx
            self._tagByRcdAndLabelId[entry.rcdID()] = listindx
            self._tagOrder.insert(index+1, listindx)

            if entry.isInPrepAccount():
                self._tagsInPrep.append(index)
                
            self._newTags.append(index)
            print "   new entry -> " + str(entry)
            # rearrange (=increment) the other account indexes if > index
            for accIndex in sorted(self._accountindexes.items(), key=itemgetter(1)):
                if accIndex[1] >= index:
                    self._accountindexes[accIndex[0]] = accIndex[1]+1
                    #print "           -> account: " + accIndex[0] + " moved to : " + str(self._accountindexes[accIndex[0]])
        return

    def removeEntry(self, rcdId):
        if self.hasRcdID(rcdId) == False:
            print warning("*** Warning:") + " rm entry: " +  str(rcdId) + " not in the collection!"
            return
        print "   " + str(rcdId)
        listindx = self._tagByRcdAndLabelId[rcdId]
        index = self._tagOrder.index(listindx)
        self._tagOrder.remove(listindx)
        # rearrange (=decrement) the other account indexes if > index
        for accIndex in sorted(self._accountindexes.items(), key=itemgetter(1)):
            if accIndex[1] >= index:
                self._accountindexes[accIndex[0]] = accIndex[1]-1
        #remove it from the list of tags in prep account
        if listindx in self._tagsInPrep:
            self._tagsInPrep.remove(listindx)
                
        return

    def addAccountSubfix(self, subfix):
        print "Appending account subfix: " + subfix
        for entry in self._tagList:
            entry.setAccount(entry._account + subfix)

        # FIXME: should fix self._accountindexes
        # for oldtag, newtag in replacetags.iteritems():
        # tagCollection.modifyEntryTag(oldtag, newtag)
        return

    
    def glbConnectReplace(self, newconnect):
        print "Force new connect: " + newconnect
        for entry in self._tagList:
            entry.setConnect(newconnect)
        return

    def printTagsInPrep(self):
        if len(self._tagsInPrep) != 0:
            print "***Warning: the following " + str(len(self._tagsInPrep)) + " tags are read form preparation account:"
        for idx in self._tagsInPrep:
            print "   ",self._tagList[idx] 
    
    def tagsInPrep(self):
        if len(self._tagsInPrep) != 0:
            return True

class GTDocGenerator:
    def __init__(self, gtName, oldGT, scope, release, changelog):
        self._listTagLink = 'http://condb.web.cern.ch/condb/listTags/?GlobalTag=' + gtName
        self._gt = gtName
        self._oldGt = oldGT
        self._scope = scope
        self._release = release
        self._change = changelog

    def isForProd(self, isForProd):
        self._isForProd = isForProd

    def wikiString(self):
        wikiString =  '| [[' + self._listTagLink + '][' + self._gt + ']] | %GREEN%' + self._release + '%ENDCOLOR%'
        if self._isForProd == False:
            wikiString = wikiString + ' %RED%(Not for prod.[[[#NOTENotProd][1]]])%ENDCOLOR%'
        wikiString = wikiString + ' | ' + self._scope  + ' | As !' + self._oldGt + ' with the following updates:' + self._change + '. |\n'
        return wikiString

    def printWikiDoc(self):
        if not os.path.exists('doc/'):
            print " directory \"doc\" doesn't exist: creating it"
            os.mkdir('doc/')
        docfilename = 'doc/' + NEWGT + '.wiki'
        docfile = open(docfilename,'w')
        docstring = self.wikiString()
        docfile.write(docstring)
        docfile.close()


# read the configuration file
CONFIGFILE=sys.argv[1]

if not os.path.isfile(CONFIGFILE):
    print error("*** Error" + " cfg file: " + CONFIGFILE + " doesn't exist!")
    sys.exit(1)

diffconfig = ConfigParser()
diffconfig.optionxform = str

print 'Reading configuration file from ',CONFIGFILE
diffconfig.read(CONFIGFILE)

# this is for [COMMON] part of the myconf.conf


#------------------------------------------------------
# general configuration
ACCOUNT = 'CMS_COND_31X_GLOBALTAG'
if diffconfig.has_option('Common','AccountGT'):
    ACCOUNT =  diffconfig.get('Common','AccountGT')
    
OLDGT = diffconfig.get('Common','OldGT')
NEWGT = diffconfig.get('Common','NewGT')

passwdfile = 'None'
if diffconfig.has_option('Common','Passwd'):
    passwdfile = diffconfig.get('Common','Passwd')

isOnline = False
if diffconfig.has_option('Common','Environment'):
    envir = diffconfig.get('Common','Environment')
    if envir == 'online':
        isOnline = True

if OLDGT == NEWGT:
    print error("*** Error") + " new and old GT names are the same, old: " + OLDGT + " new: " +  NEWGT
    sys.exit(1)

# reads the tags to be substituted and create a dict
replacetags = dict()
if diffconfig.has_section('Tags'):
    REPLACETAGS = diffconfig.items('Tags')
    replacetags = dict(REPLACETAGS)

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
        #print "   " + str(newentry)
        

# read Rcd to be removed
rmentries = []
if diffconfig.has_section("RmRecord"):
    rmrecords = diffconfig.items('RmRecord')
    for record in rmrecords:
        label = record[1]
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

if os.path.isfile(newconffile):
    print warning("*** Warning, the new GT conf file: " + newconffile + " already exists!")
    confirm = raw_input('Overwrite? (y/N)')
    confirm = confirm.lower() #convert to lowercase
    if confirm != 'y':
        sys.exit(1)



# create the collection of tags
tagCollection = GTEntryCollection()


# --------------------------------------------------------------------------

# parse the config file and fill the collection
configparser=ConfigParser()
configparser.read(oldfilename)
data=stripws(configparser.get("TAGINVENTORY",'tagdata'))
tagcollection=converttagcollection(data)

# parse the tag inventory
if len(tagcollection)!=0:
    for item in tagcollection:
        # create the tag object and populate it
        tag = GTEntry()
        tag.setFromTagInventoryLine(item)
        tagCollection.addEntry(tag)

# --------------------------------------------------------------------------
# parse the tag tree
treesection=' '.join(['TAGTREE', OLDGT])

nodecollection = []
if configparser.has_option(treesection, 'nodedata'):
    nodedata=stripws(configparser.get(treesection,'nodedata'))
    nodecollection=convertnodedata(nodedata)
    
# FIXME not dinamically read from 
node = 'Calibration'
globparent = 'All'
root=stripws(configparser.get(treesection,'root'))
if configparser.has_option(treesection, 'leafdata'):
    leafdata=stripws(configparser.get(treesection,'leafdata'))
    leafcollection=convertnodecollection(leafdata)
if len(leafcollection)!=0:
    #inv=tagInventory.tagInventory(session)
    for leafdata in leafcollection:
        # print 'again ',myleaf.nodelabel
        if leafdata.has_key('tagname') is False:
            raise ValueError, "tagname is not specified for the leaf node "+leafdata['nodelabel']
        tag = tagCollection.getByTag(leafdata['tagname'])
        tag.setFromTagTreeLine(leafdata)


# --------------------------------------------------------------------------
# manipulate the tag collection according to cfg file

if(len(replacetags) != 0):
    print "Replace tags:"
    for oldtag, newtag in replacetags.iteritems():
        tagCollection.modifyEntryTag(oldtag, newtag)

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


    # loop over all entries in the collection
    for tagidx in range(0,len(tagstobechecked)):
        theTag = tagCollection._tagList[tagstobechecked[tagidx]]
        outputAndStatus = listIov(theTag.getOraclePfn(isOnline), theTag._tag, passwdfile)
        if outputAndStatus[0] != 0:
            print ' -----'
            print error("***Error:") + " list IOV failed for tag: " + str(theTag)
            print outputAndStatus[1]
            print ''
        # print outputAndStatus[1]



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

docGenerator.printWikiDoc()

# --------------------------------------------------------------------------
# Write the new conf file

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

print "-----------------------------------------"
print newconffile+' ready. Please have a look:'
print "tkdiff " + oldfilename + " " + newconffile + ' &'

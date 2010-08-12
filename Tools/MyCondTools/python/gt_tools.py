import os
import sys
from ConfigParser import ConfigParser
from copy import copy
from optparse import OptionParser, Option, OptionValueError
#import coral
#from CondCore.TagCollection import Node,tagInventory,CommonUtils,entryComment
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
    listiovCommand = 'cmscond_list_iov -c ' + connect + '  -t ' + tag
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
    
    loadiovCommand = 'cmscond_load_iov -c ' + connect + ' ' + iovLoadFileName
    if passwd != 'None':
        loadiovCommand = loadiovCommand + ' -P ' + passwd

    loadiovStatusAndOutput = commands.getstatusoutput(loadiovCommand)
    if loadiovStatusAndOutput[0] != 0:
        print warning("Warning") + "  loadiov for tag: " + newtag + " failed!\n\n"
        print loadiovStatusAndOutput[1]
        return loadiovStatusAndOutput

    return loadiovStatusAndOutput

    
def duplicateIov(connect, tag, run, passwd):
    duplicateiovCommand = "cmscond_duplicate_iov -c " + connect + '  -t ' + tag + ' -f ' + run + ' -s ' + run
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
        # Update type: -1 unknown, 0 manual, 1 O2O
        self._updateType = -1
        return

    def setUpdateType(self, typeCode):
        if typeCode == "o2o":
            self._updateType = 1
        elif typeCode == "manual":
            self._updateType = 0
        else:
            self._updateType = -1

    def updateType(self):
        return self._updateType

    def tagName(self):
        return self._tag

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

    def getCfgFormat(self):
        """ return the string in the same format used in the cfg file to add a new record to the GT """
        cfgstring = self._leafnode + '{recordname=' + self._record + ',connect=' + self._connstring + ',account=' + self._account + ',objectname=' + self._object
        if not self._label == '':
            cfgstring = cfgstring + ',labelname=' + self._label
        cfgstring = cfgstring + '}'
        return cfgstring

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

    def setTagName(self, newtag):
        self._tag = newtag
        return

    def setEntry(self, tagname, parent, connect, account, object, record, leaf, label):
        self._tag = tagname
        self._parent = parent
        self._connstring = connect
        self._account = account
        self._object = object
        self._record = record
        self._leafnode = leaf
        self._label = label
        self._pfn = connect+'/'+record

        return

    
    def getOraclePfn(self, online):
        if online == False:
            if self._connstring == 'frontier://FrontierPrep':
                oracleConn =  'oracle://cms_orcoff_prep'
            elif self._connstring == 'frontier://FrontierArc':
                # no change is needed since it is anyhow frozen
                oracleConn =  'frontier://FrontierArc'
            else:
                oracleConn =  'oracle://cms_orcoff_prod'

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

    def isOnlineConnect(self):
        if self._connstring == 'frontier://(proxyurl=http://localhost:3128)(serverurl=http://localhost:8000/FrontierOnProd)(serverurl=http://localhost:8000/FrontierOnProd)(retrieve-ziplevel=0)(failovertoserver=no)':
            return True
        return False



class RcdID(tuple):
    def __new__(cls, *args, **kw):
        return tuple.__new__(cls, *args, **kw)

    def __str__(self):
        return "rcd: \'" + tuple.__getitem__(self,0) + "\' label: \'" + tuple.__getitem__(self,1) + "\'"




class IOVEntry:
    def __init__(self):
        self._since = -1
        self._till = -1
        self._payloadToken = ""

    def setFromListIOV(self, line):
        listofentries = line.split('\t')
        index = 0
        for entry in listofentries:
            if entry != '':
                if index == 0:
                    self._since = int(entry.rstrip())
                elif index == 1:
                    self._till = int(entry.rstrip())
                elif index == 2:
                    self._payloadToken = entry.rstrip()
            index = index + 1
                
        return

    def __str__(self):
        return str(self._since) + ' ' + str(self._till) + ' ' + self._payloadToken

    def since(self):
        return self._since

    def till(self):
        return self._till

    def token(self):
        return self._payloadToken



class IOVTable:
    def __init__(self):
        self._iovList = []
        self._tagName = ""
        return

    def addIOVEntry(self, entry):
        # print "Add IOV : " + str(entry)
        self._iovList.append(entry)

    def setFromListIOV(self, listiovOutput):
        listiovlines  = listiovOutput.split('\n')
        nLines = len(listiovlines)
        self._tagName = listiovlines[0].split(" ")[1]
        # print self._tagName
        for line in range(4, nLines-1):
            ioventry = IOVEntry()
            ioventry.setFromListIOV(listiovlines[line])
            self.addIOVEntry(ioventry)


    def checkConsitency(self, tagType):
        if tagType == "mc":
            if len(self._iovList) != 1:
                print warning("***Warning") + " MC tag: " + self._tagName + " contains: " + str(len(self._iovList)) + " IOVs"
            else:
                if self._iovList[0].since() != 1 or self._iovList[0].till() != 4294967295:
                    print warning("***Warning") + " MC tag: " + self._tagName + " has IOV: " + str(self._iovList[0])
        elif tagType == "data":
            if self._iovList[0].since() != 1 or self._iovList[len(self._iovList) - 1].till() != 4294967295:
                print warning("***Warning") + " data tag: " + self._tagName + " is not covering the whole range 1 - inf"
                self.printList()
                return
            if len(self._iovList) != 1:
                for index in range(0, len(self._iovList)-1):
                    if (self._iovList[index+1].since() - self._iovList[index].till()) != 1:
                        print warning("***Warning") + " data tag: " + self._tagName + " has an hole in the IOVs:"
                        self.printList()
                        return

    def printList(self):
        for iov in self._iovList:
            print iov
        return
        
    def lastIOV(self):
        return  self._iovList[len(self._iovList)-1]


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
        self._node = ''
        self._root = ''
        self._parent = ''
        return

    def nodedata(self):
        return  self._node

    def root(self):
        return self._root

    def parent(self):
        return self._parent

    def setNodedata(self, node):
        self._node = node

    def setRoot(self, root):
        self._root = root

    def setParent(self, parent):
        self._parent = parent
    
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
            self.getByTag(tag).setConnect(connection)
            print "   " + tag + ": " + connection
                
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

        if entry.isInPrepAccount() and not self._tagList[index].isInPrepAccount():
            self._tagsInPrep.append(index)

        if not entry.isInPrepAccount() and self._tagList[index].isInPrepAccount():
            self._tagsInPrep.remove(index)

        # reassing this entry
        self._tagList[index] = entry
        self._tagByTag[entry._tag] = index

        if not index in self._newTags:
            self._newTags.append(index)

        
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
            tag = self._tagList[idx] 
            print "   tag:", tag.tagName()," obj: ",tag._object," account: ",tag._account
            
    
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
        self._isForProd = True
        
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
        docfilename = 'doc/' + self._gt + '.wiki'
        docfile = open(docfilename,'w')
        docstring = self.wikiString()
        docfile.write(docstring)
        docfile.close()

    def addChange(self, change):
        if not change in self._change:
            self._change = self._change + '<br> - ' + change

    def snapshotValidity(self, date, lastrun = -1):
        self._scope = self._scope + "<br>%RED%(Snapshot not valid for runs > "
        if lastrun != -1:
            self._scope = self._scope + str(lastrun) + " [= " + str(date) + "]"
        else:
            self._scope = self._scope + str(date)
        self._scope = self._scope + ")%ENDCOLOR%[[[#NOTESnapValid][2]]]"



def confFileFromDB(gt, gtConfFileName):
    # check if the original conf file exists
    if not os.path.isfile(gtConfFileName):
        # get the conf file from DB
        print "Getting the conf file for GT: " + gt + " from DB....be patinet!"
        dbtoconf_cfg = ConfigParser()
        dbtoconf_cfg.optionxform = str
        dbtoconf_cfg.add_section("Common")
        dbtoconf_cfg.set("Common","Account","CMS_COND_31X_GLOBALTAG")
        dbtoconf_cfg.set("Common","Conn_string_gtag","frontier://cmsfrontier:8000/FrontierProd/CMS_COND_31X_GLOBALTAG")
        dbtoconf_cfg.set("Common","Globtag",gt)
        dbtoconf_cfg.set("Common","Confoutput",gtConfFileName)
        dbtoconf_file = open("dbtoconf.cfg", 'wb')
        dbtoconf_cfg.write(dbtoconf_file)
        dbtoconf_file.close()

        #dbtoconf_cmd = 'eval `scram runtime -csh`; dbtoconf.py'
        dbtoconf_cmd = 'dbtoconf.py'

        statusAndOutput = commands.getstatusoutput(dbtoconf_cmd)
        if statusAndOutput[0] != 0:
            print statusAndOutput[1]

        # check again
        if not os.path.isfile(gtConfFileName):
            return False

    return True


def fillGTCollection(gtConfFileName, gtName, gtEntryCollection):

    # parse the config file and fill the collection
    configparser=ConfigParser()
    configparser.read(gtConfFileName)
    data=stripws(configparser.get("TAGINVENTORY",'tagdata'))
    tagcollection=converttagcollection(data)

    # parse the tag inventory
    if len(tagcollection)!=0:
        for item in tagcollection:
            # create the tag object and populate it
            tag = GTEntry()
            tag.setFromTagInventoryLine(item)
            # set the update category if present
            if configparser.has_option('UpdateType', tag.tagName()):
                tag.setUpdateType(configparser.get('UpdateType', tag.tagName()))
            gtEntryCollection.addEntry(tag)

    # --------------------------------------------------------------------------
    # parse the tag tree
    treesection=' '.join(['TAGTREE', gtName])

    nodecollection = []
    if configparser.has_option(treesection, 'nodedata'):
        nodedata=stripws(configparser.get(treesection,'nodedata'))
        nodecollection=convertnodedata(nodedata)

    # FIXME not dinamically read from 
    gtEntryCollection.setNodedata('Calibration')
    gtEntryCollection.setParent('All')
    root=stripws(configparser.get(treesection,'root'))
    gtEntryCollection.setRoot(root)
    if configparser.has_option(treesection, 'leafdata'):
        leafdata=stripws(configparser.get(treesection,'leafdata'))
        leafcollection=convertnodecollection(leafdata)
    if len(leafcollection)!=0:
        for leafdata in leafcollection:
            # print 'again ',myleaf.nodelabel
            if leafdata.has_key('tagname') is False:
                raise ValueError, "tagname is not specified for the leaf node "+leafdata['nodelabel']
            tag = gtEntryCollection.getByTag(leafdata['tagname'])
            tag.setFromTagTreeLine(leafdata)


def cvsUpdate(filename):
    #print "cvs update " + filename
    # cvs update 
    outandstat = commands.getstatusoutput("cvs update -A " + filename)
    if outandstat[0] != 0:
        print outandstat[1]

def cvsCommit(filename, comment):
    #print "cvs commit " + filename
    outandstat = commands.getstatusoutput('cvs commit -m "' + comment + '" ' + filename)
    if outandstat[0] != 0:
        print outandstat[1]



#!/usr/bin/env python
import os
import sys
from optparse import OptionParser
import commands
from stat import *
from ConfigParser import ConfigParser

from datetime import datetime
import shutil

#from gt_tools import GTEntryCollection
#from gt_tools import *
from Tools.MyCondTools.color_tools import *
from Tools.MyCondTools.gt_tools import *




if __name__     ==  "__main__":

    parser = OptionParser()
    
    parser.add_option("-c", "--connection", dest="connection",
                      help="connection string",
                      type="str", metavar="<connstring>")
    
    parser.add_option("-t", "--tag", dest="tagname",
                      help="tag name",
                      type="str", metavar="<tag>")
    
    parser.add_option("-p", "--passwdfile", dest="passwdfile",
                      help="password file",
                      type="str", metavar="<passwdfile>",default="/afs/cern.ch/cms/DB/conddb")

    parser.add_option("-b", "--begin", dest="begin",
                      help="since of the first IOV that should",
                      type="int", metavar="<since>")

    parser.add_option("-d", "--duplicated-tag", dest="duplicate",
                      help="name of the tag where the original one will be duplicated",
                      type="str", metavar="<duplicated-tag>")


    (options, args) = parser.parse_args()


    passwdfile= options.passwdfile
    connect = options.connection
    tag = options.tagname
    newtag = options.duplicate

    begin = options.begin


    #1. duplicate the tag 
    duploutandstat = duplicateIovTag(connect, tag, newtag, passwdfile)

    

    
    outputAndStatus = listIov(connect, tag, passwdfile)
    iovtable = IOVTable()
    iovtable.setFromListIOV(outputAndStatus[1])
    #iovtable.printList()

    
    for iov in reversed(iovtable._iovList):
        #print iov.since(), begin
        if iov.since() >= begin:
            print "truncate", iov
            truncateIov(connect, tag, passwdfile)

    outputAndStatus = listIov(connect, tag, passwdfile)
    newiovtable = IOVTable()
    newiovtable.setFromListIOV(outputAndStatus[1])
    newiovtable.printList()

    print "# of IOVs before truncate: " + str(iovtable.size())
    print "# of IOVs after truncate: " + str(newiovtable.size())

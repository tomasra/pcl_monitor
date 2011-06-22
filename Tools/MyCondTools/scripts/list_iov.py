#!/usr/bin/env python

import os
import sys
from ConfigParser import ConfigParser
#from copy import copy
from optparse import OptionParser, Option, OptionValueError
from Tools.MyCondTools.gt_tools import *



def main():
    parser = OptionParser()

    parser.add_option("-c", "--connection", dest="connection",
                      help="connection string",
                      type="str", metavar="<connstring>")

    parser.add_option("-t", "--tag", dest="tagname",
                      help="tag name",
                      type="str", metavar="<tag>")
    
    parser.add_option("-P", "--passwdfile", dest="passwdfile",
                      help="password file",
                      type="str", metavar="<passwdfile>",default="/afs/cern.ch/cms/DB/conddb")

    (options, args) = parser.parse_args()

    outputAndStatus = listIov(options.connection, options.tagname, options.passwdfile)

    iovtable = IOVTable()
    iovtable.setFromListIOV(outputAndStatus[1])
    iovtable.printList()


if __name__     ==  "__main__":
    main()


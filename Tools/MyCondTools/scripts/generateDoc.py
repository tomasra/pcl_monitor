#!/usr/bin/env python
import os
import sys
from ConfigParser import ConfigParser
import commands
from Tools.MyCondTools.gt_tools import *

# --- read the configuration file

wikiFilesDir = "doc/"
wikiWebDir = "/tmp/cerminar/"
wikiWebDirFinal = "GT_branches/GTDoc/"


pwd = os.environ["PWD"]

os.chdir(wikiWebDirFinal)
cvsUpdate('Class.list')
os.chdir(pwd)

config = ConfigParser()
config.optionxform = str
config.read(['GT_branches/Common.cfg','GT_branches/GTDoc/Class.list'])

logFileName = "log/gtCreationLog.txt"
logFile = file(logFileName, 'r')
logList = logFile.read()
logFile.close()

#cvsUpdate(queueCfg)


listOfClasses = config.get("Class","GenerateDocFor").split(",")
webFileList = []

for className in listOfClasses:
    print "Generating doc for class: " + className

    webFileName = wikiWebDir + className + ".wiki.tmp"
    webFile = file(webFileName, 'w')
    if not className + ".wiki" in webFileList:
        webFileList.append(className + ".wiki")
        
    listOfGTs =  config.get(className, "GTList").split(",")
    for gtName in reversed(listOfGTs):
        print "   adding doc for GT: " + gtName
        wikiFileName = wikiFilesDir + gtName + ".wiki"
        wikiFile = file(wikiFileName, 'r')
        tmp = wikiFile.read()
        wikiFile.close()
        webFile.write(tmp)
    webFile.close()

os.chdir(wikiWebDirFinal)
for fileWiki in webFileList:
    mv_cmd = "mv " + wikiWebDir + fileWiki + ".tmp " + fileWiki
    statandout = commands.getstatusoutput(mv_cmd)
    print statandout[1]
    cvsCommit(fileWiki, "update doc")

cvsCommit("Class.list", "update doc")

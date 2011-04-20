#!/usr/bin/env python

import os
import sys
import shutil


if __name__     ==  "__main__":
    
    allwikifiles = os.listdir("doc/")
    count = 0
    for filename in  allwikifiles:
        print filename
        if  'wiki' in filename and not 'wiki~' in filename and not "tar" in filename:
            count += 1
            completeName = 'doc/' + filename
            newFileName  = '/tmp/cerminar/' + filename + ".tmp"
            wikiFile = open(completeName, 'r')
            tmpWikiFile = open(newFileName, 'w')
            wikiFileLines = wikiFile.read()
            if 'listTags' in wikiFileLines:
                newLines = wikiFileLines.replace('http://condb.web.cern.ch/condb/listTags','%LINKTOGTLIST%')
            else:
                newLines = wikiFileLines.replace('http://condb.web.cern.ch/condb/gtlist','%LINKTOGTLIST%')
            print newLines
            tmpWikiFile.write(newLines)
            tmpWikiFile.close()
            wikiFile.close()
            shutil.move(newFileName, completeName)

    print count

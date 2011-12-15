#!/usr/bin/env python
import os
import sys
import datetime
#import date
import shutil

buildArea = "/build/alcaprod/GlobalTag/"

dirsToClean = []

nightlyArea = buildArea + "Nightly/"
validationArea = buildArea + "Validation/"

dirsToClean.append(nightlyArea)

dirsToClean.append(validationArea)


# reference date is today
today = datetime.datetime.today()

for directory in dirsToClean:
    print "Cleaning dir: " + directory
    # list files
    fileList = os.listdir(directory)

    # loop over files
    for filename in fileList:
        completepath = directory + filename
        if os.path.isdir(completepath):
            if filename != "RelIntegration":

                # creation time
                createtime = datetime.datetime.fromtimestamp(os.path.getctime(completepath))

                deltaT = today - datetime.datetime.fromtimestamp(os.path.getctime(completepath))

                print "dir: " + filename + " created on: " + str(createtime) + " (" + str(deltaT.days) + " days ago)"
                if deltaT.days >= 3:
                    print "DELETE: " + filename
                    shutil.rmtree(completepath)


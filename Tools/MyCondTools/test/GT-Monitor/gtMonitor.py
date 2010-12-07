#!/usr/bin/env python
import os
import sys
from optparse import OptionParser
import commands
from stat import *
from ConfigParser import ConfigParser

from datetime import datetime
import shutil

from gt_tools import *
from popcon_monitoring_last_updates import *



def computeModified(GTCREATIONAREA, gtName, nDays, listofchanges, listofchangesO2O):
    # create the collection of tags
    tagCollection = GTEntryCollection()
    gtConf =  GTCREATIONAREA + "/" + gtName + ".conf"    
    gtCategories =  GTCREATIONAREA + "/GT_branches/Categories.cfg"
    # --------------------------------------------------------------------------
    fillGTCollection([gtConf,gtCategories], gtName, tagCollection)

    nSec = nDays*24*60*60
    updateMap = dict()

    popLog = PopCon_Monitoring_last_updates(interval=nSec)

    # loop over all tags in the GT

    for tagidx in range(0,len(tagCollection._tagOrder)):
        gtEntry = tagCollection._tagList[tagCollection._tagOrder[tagidx]]


        data = popLog.PopConRecentActivityRecorded(authfile="./auth.xml",account="",iovtag=gtEntry.tagName())
        if len(data['data']) != 0:
            # print "---------------------------------------------------------"
            #print gtEntry,
            #print "  # of updates:", len(data['data'])
            if gtEntry.updateType() != 1:
                listofchanges.append(str(gtEntry) +  "  # of updates: " + str(len(data['data'])))
            else:
                listofchangesO2O.append(str(gtEntry) +  "  # of updates: " + str(len(data['data'])))
            for entry in data['data']:
                usertext = ''
                if entry[7] != None :
                    usertext = entry[7]
                
                since = 'unknown'
                sincepos = usertext.find('since =')
                #print usertext
                #print sincepos
                if sincepos != -1:
                    since = usertext[sincepos+7:sincepos+7+6]
                else:
                    sincepos = usertext.find('Since')
                    if sincepos != -1:
                        since = usertext[sincepos+6:sincepos+6+6]
                # print '        - ' + entry[1], ' since: ', since#, ' token: ', entry[8]
                # print usertext
    
                updateMap[gtEntry.rcdID()] = len(data['data'])

    #print the results:
    if len(listofchanges) != 0:
        print "manual updates:"
        for item in listofchanges:
            print item
    if len(listofchangesO2O) != 0:
        print "O2O updates:"
        for item in listofchangesO2O:
            print item
        
            
    return updateMap




if __name__     ==  "__main__":

    

    configfile = ConfigParser()
    configfile.optionxform = str


    configfile.read('gtMonitor.cfg')
    GTCREATIONAREA = configfile.get('Common','GTCreationArea')
    gtList = configfile.get('Common','GTToMonitor').split(',')
    mailaddresses = configfile.get('Common','MailAddresses')


    gtListOfResults = []
    
    totalListOfmodifiedRecords =[]

    totalListOfChanges = []
    totalListOfChangesO2O = []

    for gt in gtList:
        print "-------------------------------------------------------------------------------------------"
        print "Updates for GT: " +  gt
        listChange = []
        listChangeO2O = []
        mapUpdates = computeModified(GTCREATIONAREA, gt,1,listChange, listChangeO2O)
        gtListOfResults.append(mapUpdates)
        totalListOfChanges.append(listChange)
        totalListOfChangesO2O.append(listChangeO2O)
        for record in mapUpdates.iteritems():
            if not record[0] in  totalListOfmodifiedRecords:
                totalListOfmodifiedRecords.append(record[0])
        

    listOfWarning = []
    
    print "-------------------------------------------------------------------------------------------"
    print "cross check:"
    for rcd in totalListOfmodifiedRecords:
        prevValue = -1
        warningFlag = False
        for idx in range(0, len(gtList)):
            rcdMap = gtListOfResults[idx]
            if not rcd in rcdMap:
                warningFlag = True
            else:
                if prevValue == -1:
                    prevValue = rcdMap[rcd]
                else:
                    if rcdMap[rcd] != prevValue:
                        warningFlag = True
        if warningFlag :
            warningMsg = '**Warning: ' + str(rcd) + ' updated '
            print warning("**Warning:"), rcd, " updated",
            for idx in range(0, len(gtList)):
                if rcd in gtListOfResults[idx]:
                    nUpd = gtListOfResults[idx][rcd]
                else:
                    nUpd = 0
                print nUpd, "for",  gtList[idx],'|', 
                warningMsg = warningMsg + str(nUpd) + ' for ' + gtList[idx] + ' | '
            print ""
            warningMsg = warningMsg+'\n'
            listOfWarning.append(warningMsg)

    today = datetime.today()

    SENDMAIL = "/usr/sbin/sendmail" # sendmail location
    
    p = os.popen("%s -t" % SENDMAIL, "w")
    p.write("To: " + mailaddresses + "\n")
    p.write("Subject: [GT-MONITOR] "+str(today) +"\n")
    p.write("\n") # blank line separating headers from body
    
    if len(listOfWarning) == 0:
        message = 'SUCCESS: updates to GTs: '
        for gt in gtList:
            message = message + gt + ' '
            message = message + ' are consistent!\n'
            p.write(message)
    
    for lines in listOfWarning:
        p.write(lines)
    

        p.write('\n')
        p.write('\n')
        p.write('\n')
        p.write('\n')
        p.write('\n')
        p.write('------------------------------------------------------------------\n')
        p.write('--- List of updates follow:\n\n\n')
        for idx in range(0, len(gtList)):
            gt = gtList[idx]
            p.write('--------------------------------------------\n')
            p.write('Updates for GT: ' + gt + '\n\n')
            listofchanges = totalListOfChanges[idx]
            for line in listofchanges:
                p.write(line +'\n')
            listofchangesO2O = totalListOfChangesO2O[idx]
            if len(listofchangesO2O):
                p.write('O2O:\n')
            for line in listofchangesO2O:
                p.write(line +'\n')
        
            p.write('\n\n')



        sts = p.close()
        if sts != 0:
            print "Sendmail exit status", sts

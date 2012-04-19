#!/usr/bin/env python
import os
import sys
from optparse import OptionParser
import commands
from stat import *
from ConfigParser import ConfigParser

from ROOT import *

import datetime
import dateutil.parser

import shutil


# Configuration
passwdfile             = "/afs/cern.ch/cms/DB/conddb"
tier0DasSrc            = "https://cmsweb.cern.ch/tier0/"
referenceDataset       = "MinimumBias"
weburl                 = "http://cms-alcadb.web.cern.ch/cms-alcadb/Monitoring/PCLO2O/"
gtconnstring           = 'oracle://cms_orcoff_prod/CMS_COND_31X_GLOBALTAG'
monitoredrecords       = 'EcalLaserAPDPNRatiosRcd,SiStripDetVOffRcd'
# FIXME: move to a better place
cacheFileName          = 'o2oMonitor.cache'
runinfoTag             = 'runinfo_31X_hlt'
webArea                = '/afs/cern.ch/user/a/alcaprod/www/Monitoring/PCLO2O/' 

import Tools.MyCondTools.monitorStatus as monitorStatus
import Tools.MyCondTools.tier0DasInterface as tier0DasInterface
import Tools.MyCondTools.gt_tools as gtTools
import Tools.MyCondTools.o2oMonitoringTools as o2oMonitoringTools
import Tools.MyCondTools.RunRegistryTools as RunRegistryTools
import Tools.MyCondTools.popcon_monitoring_last_updates as popConLog
import Tools.MyCondTools.color_tools as colorPrintTools
import Tools.MyCondTools.RunInfo as RunInfo
import Tools.MyCondTools.tableWriter as tableWriter



def runBackEnd():
    tier0Das = tier0DasInterface.Tier0DasInterface(tier0DasSrc) 
    try:
        nextPromptRecoRun = tier0Das.firstConditionSafeRun()
        print "Tier0 DAS next run for prompt reco:",nextPromptRecoRun
        gtFromPrompt = tier0Das.promptGlobalTag(nextPromptRecoRun, referenceDataset)
        print "      GT for dataset: ", referenceDataset, "run:", str(nextPromptRecoRun), ":", gtFromPrompt
    except Exception as error:
        print '*** Error 2: Tier0-DAS query has failed'
        print error
        return 102, "Error: Tier0-DAS query has failed: " + str(error)
    

    gtName = gtFromPrompt.split('::')[0]
    gtConfFile = gtName + '.conf'

    
    if not gtTools.confFileFromDB(gtName, gtConfFile, gtconnstring, passwdfile):
        # FIXME: which return #?
        return 1000
    

    # create the collection of tags
    tagCollection = gtTools.GTEntryCollection()
    gtTools.fillGTCollection(gtName+'.conf', gtName, tagCollection)
    
    tagsTomonitor = []

    print "Tags to be monitored: "
    for record in monitoredrecords.split(','):
        # FIXME: the label should come from the configuration
        label = ''
        rcdId =  gtTools.RcdID([record, label])
        if not tagCollection.hasRcdID(rcdId):
            print "Error: rcd: " + rcdIdn + " not found in GT: " + gtName
        else:
            print '   ', tagCollection.getByRcdID(rcdId)
            tagsTomonitor.append(tagCollection.getByRcdID(rcdId))


    # --------------------------------------------------------------------------------
    # --- read the cache
    allCachedRuns = o2oMonitoringTools.readCache(cacheFileName)
    cachedRuns = allCachedRuns[0]
    runReports = allCachedRuns[1]

    unknownRun = False # this is set to true only if one run can not be processed
    unknownRunMsg = ''
    # --------------------------------------------------------------------------------
    # --- get the last cached run
    if len(cachedRuns) != 0:
        cachedRuns.sort()
    else:
        cachedRuns.append(1)

    lastCachedRun = cachedRuns[len(cachedRuns)-1]
    #lastCachedRun = 191419
    print "last cached run #: " + str(lastCachedRun)

    # --------------------------------------------------------------------------------
    # --- get the list of collision runs from RR (only for the runs not yet cached)
    runList = []
    try:
        # FIXME: do we need to restrict to Collision12?
        #runList = RunRegistryTools.getRunListRR3(lastCachedRun+1,"Online", "Commissioning12")
        runList = RunRegistryTools.getRunListRR3(lastCachedRun+1,"Online", "Collisions12")

    except Exception as error:
        print '*** Error 1: RR query has failed'
        print error
        return 101, "Error: failed to get collision runs from RunRegistry: " + str(error)

    print runList


    # --------------------------------------------------------------------------------
    # --- check O2O and DB tag status for each record
    threshold = datetime.timedelta(hours=2)
    thresholdSince = datetime.timedelta(hours=48)

    today = datetime.datetime.today()
    fromUTCToLocal = datetime.timedelta(hours=2)
    recordandlastsince = {}

    tableTitle = ["# run", "start-time", "end-time"]

    for entry in tagsTomonitor:
        print "- Tag:", entry
        
        tagName = entry.tagName()
        accountName = entry.account()
        recordName = entry.record()

        tableTitle.append(recordName)

        # create the report for this given record
        rcdRep = o2oMonitoringTools.RecordReport(recordName)
        rcdRep.setTagAndAccount(tagName, accountName)

        # 1. get the last updates from PopConLogger
        nDays = 1
        nSec = nDays*24*60*60
        popLog = popConLog.PopCon_Monitoring_last_updates(interval=nSec)
        # FIXME: the auth.xml can it be read from a central place?
        logData = popLog.PopConRecentActivityRecorded(authfile=passwdfile + "/authentication.xml",
                                                      account=accountName,
                                                      iovtag=tagName)

        

        if len(logData['data']) != 0:
            datestring = logData['data'][0][1]
            status = logData['data'][0][6]
            token =  logData['data'][0][8]
            #datelastupdate = datetime.datetime.strptime(datestring,"%B, %dnd %Y  %H:%M:%S") + fromUTCToLocal
            datelastupdate = dateutil.parser.parse(datestring) + fromUTCToLocal

            updateage = today - datelastupdate
            statusForRpt = "OK"
            print "  - Last O2O run on: " + str(datelastupdate) + " (" +  str(updateage) + " ago)"
            print "    status:",status, "payload token:", token.split("<br>")[4]
            if updateage > threshold:
                print "      " + colorPrintTools.warning("Warning") + ": O2O is not running since a while!"
                statusForRpt = "OLD"
            if status != 'OK':
                print "      Warning: O2O status is: " + status + "!"
                statusForRpt = "ERROR"
            rcdRep.setLastO2OWrite(datelastupdate, updateage, statusForRpt)
        else:
            print "Error: No O2O updates to tag: " + tagName + " in account: " + accountName
            #rcdRep.setLastO2OWrite(datelastupdate, updateage, "ERROR")


            
        # 2. check the status of the tag
        # FIXME: patch to use ADG accounts
        outputAndStatus = gtTools.listIov(entry.getOraclePfn(False), tagName, passwdfile + "/ADG")
        iovtable = gtTools.IOVTable()
        iovtable.setFromListIOV(outputAndStatus[1])
        datesince = iovtable.lastIOV().sinceDate()
        sinceage = today - datesince
        print "  - Last IOV since:", datesince, "(" + str(sinceage),"ago)"
        print "    with token: [" + iovtable.lastIOV().token() +"]"#.split("][")[4]
        recordandlastsince[recordName] = datesince
        #print iovtable.lastIOV()
        stat = "OK"
        if sinceage > thresholdSince:
            stat = "OLD"
        rcdRep.setLastSince(datesince, sinceage, stat)


        
        #pageWriter.addRecordReport(recordName, rcdRep)

    # --------------------------------------------------------------------------------
    # --- Write the Rcd status to cache
    # FIXME
    

    # --------------------------------------------------------------------------------
    # --- check the status for each of the Collision runs
    for run in runList:
        if run == 167551:continue
        print "-- run #: " + colorPrintTools.blue(str(run))            
        #print run
        # get the information from runInfo
        runInfo = None
        try: 
            runInfo = RunInfo.getRunInfoStartAndStopTime(runinfoTag, "", run)
        except Exception as error:
            print '*** Error XXX: RunInfo query failed!'
            print error
            #return 102, "Error: Run-Info query has failed: " + str(error)
            continue
            
        rRep = o2oMonitoringTools.RunReportTagCheck()
        rRep.setRunNumber(runInfo.run())
        #rRep.setStartTime(runInfo.startTime())
        rRep.setRunInfoContent(runInfo)
        deltaTRun = runInfo.stopTime() - runInfo.startTime()
        deltaTRunH = deltaTRun.seconds/(60.*60.)


        print "   start: " + str(runInfo.startTime()) + " stop: " + str(runInfo.stopTime()) + " lenght (h): " + str(deltaTRunH)
        #pageWriter.setNextPromptReco(runInfo.run(), runInfo.startTime(), runInfo.stopTime(), deltaTRunH)
        for entry in tagsTomonitor:
            recordName = entry.record()
            datesince = recordandlastsince[recordName]
            if runInfo.stopTime() <= datesince:
                print "   rcd: ", recordName,":",colorPrintTools.ok("OK")
                rRep.addRecordAndStatus(recordName, 0)
            elif runInfo.startTime()  < datesince and runInfo.stopTime() > datesince:
                print "   rcd: ", recordName,":",colorPrintTools.warning("partially covered!")
                rRep.addRecordAndStatus(recordName, 0.5)
            else:
                print "   rcd: ", recordName,":",colorPrintTools.error("not covered!")
                rRep.addRecordAndStatus(recordName, 1)

        runReports.append(rRep)
        # print "---------------------------------------------------------"
        #print gtEntry,
        #print "  # of updates:", len(logData['data'])
        #if gtEntry.updateType() != 1:
        #    listofchanges.append(str(gtEntry) +  "  # of updates: " + str(len(logData['data'])))
        #else:
        #    listofchangesO2O.append(str(gtEntry) +  "  # of updates: " + str(len(logData['data'])))



    # --------------------------------------------------------------------------------
    # --- write to cache and to log
    runReports.sort(key=lambda rr: rr._runnumber)

    tableForCache =[]
    tableForCache.append(tableTitle)
    tableForLog =[]
    tableForLog.append(tableTitle)

    for rep in runReports:
        if rep.runNumber() < nextPromptRecoRun:
            tableForCache.append(rep.getList())            
        tableForLog.append(rep.getList()) 


    #out = sys.stdout
    print "writing cache file: " + cacheFileName
    cacheFile = file(cacheFileName,"w")
    tableWriter.pprint_table(cacheFile, tableForCache)
    cacheFile.close()

    out = sys.stdout
    logFile = file(webArea + "log.txt","w")
    tableWriter.pprint_table(logFile, tableForLog)
    logFile.close()











if __name__     ==  "__main__":

    # start here
    status = monitorStatus.MonitorStatus("O2OMonitor")
    status.setWebUrl(weburl)
    statAndMsg = None
    #try:
    statAndMsg = runBackEnd()
    
    

    sys.exit(0)

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

#from gt_tools import GTEntryCollection
#from gt_tools import *
from Tools.MyCondTools.color_tools import *
from Tools.MyCondTools.gt_tools import *
from Tools.MyCondTools.RunRegistryTools import *
from Tools.MyCondTools.RunInfo import *
from Tools.MyCondTools.RunValues import *
from Tools.MyCondTools.tableWriter import *


from Tools.MyCondTools.popcon_monitoring_last_updates import *

import os,sys, DLFCN
sys.setdlopenflags(DLFCN.RTLD_GLOBAL+DLFCN.RTLD_LAZY)

from pluginCondDBPyInterface import *

a = FWIncantation()

#os.putenv("CORAL_AUTH_PATH","/afs/cern.ch/cms/DB/conddb")
rdbms                  = RDBMS("/afs/cern.ch/cms/DB/conddb")
dbName                 =  "oracle://cms_orcoff_prod/CMS_COND_31X_RUN_INFO"
logName                = "oracle://cms_orcoff_prod/CMS_COND_31X_POPCONLOG"
runinfoTag             = 'runinfo_31X_hlt'
tier0DasSrc            = "http://gowdy-wttest.cern.ch:8304/tier0/runs"
cacheFile              = ".tagMonitoring.cache"
webArea                = '/afs/cern.ch/user/c/cerminar/www/O2OMonitoring/'

rdbms.setLogger(logName)
from CondCore.Utilities import iovInspector as inspect

db = rdbms.getDB(dbName)
tags = db.allTags()

class RunReportTagCheck:
    def __init__(self):
        self._runnumber = -1
        self._startTime = None
        self._stopTime = None
        self._recordList = []
        self._recordStatus = []
        
        return

    def runNumber(self):
        return self._runnumber


    def startTime(self):
        return self._startTime

    def stopTime(self):
        return self._stopTime

    def setRunNumber(self, number):
        self._runnumber = number

    def setStartTime(self, start):
        self._startTime = start

    def setStopTime(self, stop):
        self._stopTime = stop

    def setRunInfoContent(self, runInfo):
        self._startTime = runInfo.startTime()
        self._stopTime = runInfo.stopTime()
        #self._runInfo = runInfo

    # hours
    def runLenght(self):
        deltaTRun = self.stopTime() - self.startTime()
        return deltaTRun.days*24.0 + deltaTRun.seconds/(60.*60.)

    def __str__(self):
        return "--- run #: " + str(self._runnumber) + " start time: " + str(self.startTime())

    def getList(self):
             theList = [str(self._runnumber), str(self.startTime()), str(self.stopTime())]
             for index in range(0, len(self._recordList)):
                 #theList.append(self._recordList[index])
                 theList.append(self._recordStatus[index])
             return theList

    def addRecordAndStatus(self, record, status):
        if not record in  self._recordList:
            self._recordList.append(record)
            self._recordStatus.append(status)
        else:
            print "Record already registered!"


class RecordReport:
    def __init__(self, recordname):
        self._record = recordname
        self._tagName = None
        self._accountName = None
        self._lastWrite = None
        self._lastWriteAge = None
        self._lastWriteStatus = "OK"
        self._lastSince = None
        self._lastSinceAge = None
        self._lastSinceStatus = "OK"

        
    def setLastO2OWrite(self, dateandtime, age, status):
        self._lastWrite = dateandtime
        self._lastWriteAge = age
        self._lastWriteStatus = status

    def setLastSince(self, dateandtime, age, status):
        self._lastSince = dateandtime
        self._lastSinceAge = age
        self._lastSinceStatus = status

    def setTagAndAccount(self, tag, account):
        self._tagName = tag
        self._accountName = account



class WebPageWriter:
    def __init__(self):
        self._recordReports = dict()
        self._records = []
        self._lastPromptRecoRun = -1
        self._nextPromptRecoRun = -1
        self._nextPromptRecoRunStart = None
        self._nextPromptRecoRunStop = None
        self._nextPromptRecoRunLenght = -1

    def setLastPromptReco(self, run):
        self._lastPromptRecoRun = run

    def setNextPromptReco(self, run, start, stop, lenght):
        self._nextPromptRecoRun = run
        self._nextPromptRecoRunStart = start
        self._nextPromptRecoRunStop = stop
        self._nextPromptRecoRunLenght = lenght
        
    def addRecordReport(self, recordname, report):
        self._records.append(recordname)
        self._recordReports[recordname] = report


    def buildPage(self):
        htmlpage = file('index.html',"w")
        htmlpage.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n')
        htmlpage.write('<html><head>\n')
        htmlpage.write('<link rel="stylesheet" type="text/css" href="./PromptCalibMonitoring.css">\n')
        htmlpage.write('<META HTTP-EQUIV="REFRESH" CONTENT="1800">\n')
        htmlpage.write('<title>Monitoring of Tags in the Prompt-calibration Loop</title>\n')
        htmlpage.write('</head>\n')
        htmlpage.write('<body>\n')
        htmlpage.write('<center><h1>Monitoring of Tags in the Prompt-calibration Loop</h1></center>\n<hr>\n')
        htmlpage.write('<center>')
        for rcd in self._records:
            htmlpage.write('[<a href=#' + rcd + '>' + rcd + '</a>]')
        htmlpage.write('</center><br>\n')
        htmlpage.write('<p>Last update: ' + str(datetime.datetime.today()) + '</p>\n')
        htmlpage.write('<p>Last run released for Prompt-Reco: ' + str(self._lastPromptRecoRun) + '</p>\n')
        htmlpage.write('<p>Next <b>Collision</b> run to be released for Prompt-Reco: ' + str(self._nextPromptRecoRun) + ' start time: ' + str(self._nextPromptRecoRunStart) + ' stop time: ' + str(self._nextPromptRecoRunStop) + ' length (h): ' + str(self._nextPromptRecoRunLenght) + '</p>\n')
        htmlpage.write('<p><b>Next</b> the O2O processes run every 2 hours. It might happen that no new payload are written in that case the "date" might be old. Unless there are runs not covered by the last IOV that are about to be released for prompt-reco this is usually not a problem. Anyhow keep an eye on it...</p>\n')


        for rcd in self._records:
            rpt = self._recordReports[rcd]
            htmlpage.write('<h3>' + rcd + '</h3><a name=' + rcd + '></a>\n')
            htmlpage.write('<table width="100%">\n')
            htmlpage.write('<tr><td><b>Tag:</b> ' + rpt._tagName + ', <b>account:</b> ' + rpt._accountName + '</td><td><b>status</b>:</td></tr>\n')

            img = "warning.png"
            if rpt._lastWriteStatus == "ERROR":
                img = "error.png"
            elif rpt._lastWriteStatus == "OK":
                img = "ok.png"
            htmlpage.write('<tr><td><b>Last O2O wrote @:</b> ' + str(rpt._lastWrite) + ', (' + str(rpt._lastWriteAge) + ' hours ago)</td><td>' + rpt._lastWriteStatus + ' <img src="./' + img + '" width="20"></td></tr>\n')
            imgSince = "ok.png"
            if rpt._lastSinceStatus != "OK":
                imgSince = "error.png"
            htmlpage.write('<tr><td><b>Last Since in the DB:</b> ' + str(rpt._lastSince) + ', (' + str(rpt._lastSinceAge) + ' hours old)</td><td>' + rpt._lastSinceStatus + ' <img src="./' + imgSince + '" width="20"></td></tr>\n')
            htmlpage.write('<tr><td><img src="./c' + rcd + '.png" width="1200"></td><td></td></tr>\n')
            htmlpage.write('</table>\n')
            htmlpage.write('<hr>\n')



        htmlpage.write('<p>Full logs can be accessed here: <a href=log.txt>log.txt</a></p>\n')
        
        htmlpage.write('<h3>Useful Links for debugging</h3><br>\n')
        htmlpage.write('<ul>\n')
        htmlpage.write('<li><a href=http://cms-conddb.cern.ch/popcon/PopConRecentActivityRecorded.html>Pop-Con Logger</a></li>\n')
        htmlpage.write('<li><a href=http://cms-conddb.cern.ch/popcon/PopConCronjobTailFetcher.html>Pop-Con Tail Fetcher</a></li>\n')
        htmlpage.write('<li><a href=http://cms-conddb.cern.ch/gtlist/>GT list </a></li>\n')
        htmlpage.write('</ul>\n')

        htmlpage.write('<p>\n')
        htmlpage.write('<hr>\n')
        htmlpage.write('<address>Gianluca Cerminara</address>\n')
        htmlpage.write('</body>\n')
        htmlpage.write('</html>\n')
        htmlpage.close()

if __name__     ==  "__main__":
    passwdfile="/afs/cern.ch/cms/DB/conddb"


    tagsTomonitor = []
    
    laserTag = GTEntry()
    laserTag.setEntry('EcalLaserAPDPNRatios_v6_noVPT_online',
                      "Calibration",
                      "oracle://cms_orcoff_prod/",
                      "CMS_COND_311X_ECAL_LAS",
                      "EcalLaserAPDPNRatios",
                      "EcalLaserAPDPNRatiosRcd",
                      "EcalLaserAPDPNRatios", "")

    sistripdcsTag =  GTEntry()
    sistripdcsTag.setEntry('SiStripDetVOff_v2_prompt',
                           "Calibration",
                           "oracle://cms_orcoff_prod/",
                           'CMS_COND_31X_STRIP',
                           'SiStripDetVOff',
                           'SiStripDetVOffRcd',
                           'SiStripDetVOff',"")

    tagsTomonitor.append(laserTag)
    tagsTomonitor.append(sistripdcsTag)

    threshold = datetime.timedelta(hours=2)
    thresholdSince = datetime.timedelta(hours=48)

    today = datetime.datetime.today()
    fromUTCToLocal = datetime.timedelta(hours=2)

    pageWriter = WebPageWriter()


    # get the last run released for prompt
    rv = RunValues()
    lastPromptRecoRun = rv.getLargestReleasedForPrompt(tier0DasSrc)
    print "Last run released for prompt:", lastPromptRecoRun
    #print runList
    pageWriter.setLastPromptReco(int(lastPromptRecoRun))
    
    runReports = []
    cachedRuns = []
    cachedRuns.append(1)
    
    # FIXME: read cache
    if os.path.exists(cacheFile):
        cache = file(cacheFile,"r")
        data = cache.readlines()
        for line in data:
            if line[0] != '#' and line != "":
                items = line.split()
                runCached = int(items[0])
                cachedRuns.append(runCached)
                startCached = getDate(items[1] + " " + items[2])
                stopCached = getDate(items[3] + " " + items[4])

                rRep = RunReportTagCheck()
                rRep.setRunNumber(runCached)
                rRep.setStartTime(startCached)
                rRep.setStopTime(stopCached)
                remaining = len(items) - 5
                last = 4
                #print runCached
                while remaining >= 1:
                    record = data[0].split()[last]
                    status = items[last+1]
                    rRep.addRecordAndStatus(record,status)
                    #print data[0].split()
                    #print record, status
                    last += 1
                    remaining -= 1
                runReports.append(rRep)
    cachedRuns.sort()
    lastCachedRun = cachedRuns[len(cachedRuns)-1]
    # 0. get the list of runs from run info
    runList = getRunList(lastCachedRun+1)    

    recordandlastsince = dict()

    
    tableTitle = ["# run", "start-time", "end-time"]
    for entry in tagsTomonitor:
        print "- Tag:", entry
        
        tagName = entry.tagName()
        accountName = entry.account()
        recordName = entry.record()
        tableTitle.append(recordName)
        #        tableTitle.append("covered")
        rcdRep = RecordReport(recordName)
        rcdRep.setTagAndAccount(tagName, accountName)

        # 1. get the last updates from PopConLogger
        nDays = 1
        nSec = nDays*24*60*60
        popLog = PopCon_Monitoring_last_updates(interval=nSec)
        data = popLog.PopConRecentActivityRecorded(authfile="./Tools/MyCondTools/test/GT-Monitor/auth.xml",
                                                   account=accountName,
                                                   iovtag=tagName)
        if len(data['data']) != 0:
            datestring = data['data'][0][1]
            status = data['data'][0][6]
            token =  data['data'][0][8]
            #datelastupdate = datetime.datetime.strptime(datestring,"%B, %dnd %Y  %H:%M:%S") + fromUTCToLocal
            datelastupdate = dateutil.parser.parse(datestring) + fromUTCToLocal

            updateage = today - datelastupdate
            statusForRpt = "OK"
            print "  - Last O2O run on: " + str(datelastupdate) + " (" +  str(updateage) + " ago)"
            print "    status:",status, "payload token:", token.split("<br>")[4]
            if updateage > threshold:
                print "      " + warning("Warning") + ": O2O is not running since a while!"
                statusForRpt = "OLD"
            if status != 'OK':
                print "      Warning: O2O status is: " + status + "!"
                statusForRpt = "ERROR"
            rcdRep.setLastO2OWrite(datelastupdate, updateage, statusForRpt)
        else:
            print "Error: No O2O updates to tag: " + tagName + " in account: " + accountName

            
            
        # 2. check the status of the tag
        outputAndStatus = listIov(entry.getOraclePfn(False), tagName, passwdfile)
        iovtable = IOVTable()
        iovtable.setFromListIOV(outputAndStatus[1])
        datesince = iovtable.lastIOV().sinceDate()
        sinceage = today - datesince
        print "  - Last IOV since:", datesince, "(" + str(sinceage),"ago)"
        print "    with token: [" + iovtable.lastIOV().token().split("][")[4]
        recordandlastsince[recordName] = datesince
        #print iovtable.lastIOV()
        stat = "OK"
        if sinceage > thresholdSince:
            stat = "OLD"
        rcdRep.setLastSince(datesince, sinceage, stat)
        
        pageWriter.addRecordReport(recordName, rcdRep)

    for run in runList:
        #print run
        # get the information from runInfo
        try :
            log = db.lastLogEntry(runinfoTag)
            # for printing all log info present into log db 
            #print log.getState()

            # for inspecting all payloads/runs
            iov = inspect.Iov(db,runinfoTag, run,run)
        except RuntimeError :
            print error("*** Error:") + " no iov? in", runinfoTag


        # --- read the information for the run from runinfo
        for x in  iov.summaries():
            #print x
            runInfo = RunInfoContent(x[3])
            #print x[3]
            # run lenght
            deltaTRun = runInfo.stopTime() - runInfo.startTime()
            deltaTRunH = deltaTRun.seconds/(60.*60.)

            #print runInfo.run()
            #print runInfo.startTime()
            #print runInfo.stopTime()
            #print deltaTRun
            #print deltaTRun.seconds

        rRep = RunReportTagCheck()
        rRep.setRunNumber(runInfo.run())
        #rRep.setStartTime(runInfo.startTime())
        rRep.setRunInfoContent(runInfo)

        print "-- run #: " + blue(runInfo.run())            
        print "   start: " + str(runInfo.startTime()) + " stop: " + str(runInfo.stopTime()) + " lenght (h): " + str(deltaTRunH)
        pageWriter.setNextPromptReco(runInfo.run(), runInfo.startTime(), runInfo.stopTime(), deltaTRunH)
        for entry in tagsTomonitor:
            recordName = entry.record()
            datesince = recordandlastsince[recordName]
            if runInfo.stopTime() <= datesince:
                print "   rcd: ", recordName,":",ok("OK")
                rRep.addRecordAndStatus(recordName, 0)
            elif runInfo.startTime()  < datesince and runInfo.stopTime() > datesince:
                print "   rcd: ", recordName,":",warning("partially covered!")
                rRep.addRecordAndStatus(recordName, 0.5)
            else:
                print "   rcd: ", recordName,":",error("not covered!")
                rRep.addRecordAndStatus(recordName, 1)

        runReports.append(rRep)
        # print "---------------------------------------------------------"
        #print gtEntry,
        #print "  # of updates:", len(data['data'])
        #if gtEntry.updateType() != 1:
        #    listofchanges.append(str(gtEntry) +  "  # of updates: " + str(len(data['data'])))
        #else:
        #    listofchangesO2O.append(str(gtEntry) +  "  # of updates: " + str(len(data['data'])))


    # ================================================================================
    # write to cache and to log
    runReports.sort(key=lambda rr: rr._runnumber)
    
    tableForCache =[]
    tableForCache.append(tableTitle)
    tableForLog =[]
    tableForLog.append(tableTitle)

    for rep in runReports:
        if rep.runNumber() < lastPromptRecoRun:
            tableForCache.append(rep.getList())            
        tableForLog.append(rep.getList()) 

        
    #out = sys.stdout
    cacheFile = file(cacheFile,"w")
    pprint_table(cacheFile, tableForCache)
    cacheFile.close()

    #out = sys.stdout
    logFile = file(webArea + "log.txt","w")
    pprint_table(logFile, tableForLog)
    logFile.close()



    # ================================================================================
    # draw a plot for each record
    # --- set the style 
    # draw the plots
    gStyle.SetOptStat(0) 
    gStyle.SetPadBorderMode(0) 
    gStyle.SetCanvasBorderMode(0) 
    gStyle.SetPadColor(0);
    gStyle.SetCanvasColor(0);
    gStyle.SetOptTitle(0)
    gStyle.SetPadBottomMargin(0.13)
    gStyle.SetTitleXOffset(1.6)
    gStyle.SetTitleOffset(1.6,"X")


    from array import array
    colorError = array('i')
    colorError.append(408)
    colorError.append(791)
    colorError.append(611)
    gStyle.SetPalette(3,colorError)

    # --- book the histos
    newlegend = TLegend(0.8,0.8,1,1)
#     ok = TH1F("ok","ok",1,0,1)
#     ok.SetFillColor(408)
#     newlegend.AddEntry(ok,"ok","F")
#     notFully = TH1F("notFully","notFully",1,0,1)
#     notFully.SetFillColor(791)
#     newlegend.AddEntry(notFully,"not fully covered","F")
#     notCovered = TH1F("notCovered","notCovered",1,0,1)
#     notCovered.SetFillColor(611)
#     newlegend.AddEntry(notCovered,"not covered","F")
#    newlegend.Draw()

    nRunsToPlot = 100
    if nRunsToPlot != -1:
        nToFill = nRunsToPlot



    histoPerRecord = dict()
    for entry in tagsTomonitor:
        recordName = entry.record()
        hStatus = TH2F('h'+recordName, "Status for record: " + recordName, nToFill,0,nToFill, 1, 0, 1)
        histoPerRecord[recordName] = hStatus
        hStatus.SetBinContent(-1,1,1)
        
    minId = 0
    if nRunsToPlot != -1 and nRunsToPlot < len(runReports):
        minId = len(runReports) - nRunsToPlot

    binIdx = 1
    indexLastT0Run = 1
    for id in range(minId, len(runReports)):
        report = runReports[id]
        run = report.runNumber()
        if int(run) < int(lastPromptRecoRun):
            indexLastT0Run = binIdx
        for rcdidx in range(0, len(tagsTomonitor)):
            rcd = report._recordList[rcdidx]
            status = report._recordStatus[rcdidx]
            histoPerRecord[rcd].GetXaxis().SetBinLabel(binIdx, str(run))
            histoPerRecord[rcd].SetBinContent(binIdx, 1, float(status)+0.01)
            
        binIdx += 1

    lineLastPromptRecoEnd = TLine(indexLastT0Run, 0, indexLastT0Run, 1)
    lineLastPromptRecoEnd.SetLineColor(2)
    lineLastPromptRecoEnd.SetLineWidth(3)
    lineLastPromptRecoEnd.SetLineStyle(2)
    newlegend.AddEntry(lineLastPromptRecoEnd, "Prompt-reco status", "L")


    for rcdidx in range(0, len(tagsTomonitor)):
        record = tagsTomonitor[rcdidx].record()
        c4 = TCanvas("c" + record,"c" + record,1200,200)
        c4.GetPad(0).SetBottomMargin(0.5)
        c4.GetPad(0).SetLeftMargin(0.01)
        c4.GetPad(0).SetRightMargin(0.02)

        rcd = report._recordList[rcdidx]
        hist = histoPerRecord[rcd]
        hist.SetMaximum(1)
        hist.SetMinimum(0)
        hist.GetXaxis().SetLabelSize(0.12)
        hist.GetYaxis().SetNdivisions(1)
        hist.Draw("COL")
        lineLastPromptRecoEnd.Draw("same")
        newlegend.Draw("same")
        c4.Print(webArea + 'c' + record + '.png')
        #raw_input ("Enter to quit")

    os.chdir(webArea)
    pageWriter.buildPage()

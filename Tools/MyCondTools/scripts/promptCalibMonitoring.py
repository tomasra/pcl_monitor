#!/usr/bin/env python

import os,sys, DLFCN
sys.setdlopenflags(DLFCN.RTLD_GLOBAL+DLFCN.RTLD_LAZY)

from Tools.MyCondTools.gt_tools import *
from Tools.MyCondTools.color_tools import *
#from Tools.MyCondTools.Tier0LastRun import *
from Tools.MyCondTools.RunValues import *

import shutil

from pluginCondDBPyInterface import *

a = FWIncantation()

# --------------------------------------------------------------------------------
# configuratio
runinfoTag             = 'runinfo_31X_hlt'
promptCalibDir         = '/afs/cern.ch/cms/CAF/CMSALCA/ALCA_PROMPT/'
webArea                = '/afs/cern.ch/user/c/cerminar/www/PromptCalibMonitoring/'
tagLumi                = "BeamSpotObject_ByLumi"
tagRun                 = "BeamSpotObject_ByRun"
tier0DasSrc            = "https://cmsweb.cern.ch/tier0/runs"
passwd                 = "/afs/cern.ch/cms/DB/conddb"
connectOracle          =  "oracle://cms_orcoff_prod/CMS_COND_31X_BEAMSPOT"
tagRunOracle           = "BeamSpotObjects_PCL_byRun_v0_offline"
tagLumiOracle          = "BeamSpotObjects_PCL_byLumi_v0_prompt"

writeToWeb             = True
nRunsToPlot            = 100

#os.putenv("CORAL_AUTH_PATH","/afs/cern.ch/cms/DB/conddb")
rdbms = RDBMS("/afs/cern.ch/cms/DB/conddb")
dbName =  "oracle://cms_orcoff_prod/CMS_COND_31X_RUN_INFO"
logName = "oracle://cms_orcoff_prod/CMS_COND_31X_POPCONLOG"

rdbms.setLogger(logName)
from CondCore.Utilities import iovInspector as inspect

db = rdbms.getDB(dbName)
tags = db.allTags()



#webArea = './'
# for inspecting last run after run has stopped  
#tag = 'runsummary_test'


from ROOT import *
from array import array

import datetime

def getDate(string):
    date = string.split()[0].split('-')
    time = string.split()[1].split(':')
    datet = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]),int(float(time[2])))
    return datet

class RunInfoContent:
    def __init__(self, summary):
        listofEntries = summary.split(',')
        self._run = listofEntries[0].lstrip('RUN:').lstrip()
        self._startTime = listofEntries[1].lstrip('START TIME:').lstrip()
        self._stopTime = listofEntries[2].lstrip('STOP TIME:').lstrip()
        self._fromUTCToLocal = datetime.timedelta(hours=2)
        return

    def startTime(self):
        return self.getDate(self._startTime)+self._fromUTCToLocal

    def stopTime(self):
        return self.getDate(self._stopTime)+self._fromUTCToLocal

    def run(self):
        return self._run

    def getDate(self, string):
        date = string.split('T')[0].split('-')
        time = string.split('T')[1].split(':')
        datet = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]),int(float(time[2])))
        return datet


import os,string,sys,commands,time
import xmlrpclib


def getRunList(minRun):
    runlist = []
    
    FULLADDRESS="http://pccmsdqm04.cern.ch/runregistry/xmlrpc"
    #FULLADDRESS="http://pccmsdqm04.cern.ch/runregistry_api/"
    print "RunRegistry from: ",FULLADDRESS
    server = xmlrpclib.ServerProxy(FULLADDRESS)
    # you can use this for single run query
#    sel_runtable="{runNumber} = "+run+" and {datasetName} LIKE '%Express%'"
    sel_runtable="{groupName} ='Collisions11' and {runNumber} >= " + str(minRun) + " and {datasetName} LIKE '%Express%'"
    #sel_runtable="{groupName} ='Commissioning11' and {runNumber} >= " + str(minRun)# + " and {datasetName} LIKE '%Express%'"

    run_data = server.DataExporter.export('RUN', 'GLOBAL', 'csv_runs', sel_runtable)
    for line in run_data.split("\n"):
        #print line
        run=line.split(',')[0]
        if "RUN_NUMBER" in run or run == "":
            continue
        #print "RUN: " + run
        runlist.append(int(run))
    return runlist

def fill1DHisto(histo, xarray, yarray, labels = False):
    lastBin= int(len(xarray))
    counter = 0
    for runnumber in xarray:
#        print "run: " + str(runnumber)
#        print "bin: " + str(lastBin)
        histo.SetBinContent(lastBin, yarray[counter])
        if labels:
            histo.GetXaxis().SetBinLabel(lastBin, str(int(runnumber)))
        lastBin-=1
        counter+=1


class RunReport:
    def __init__(self):
        self._runnumber = -1
        self._pclRun = True
        self._hasPayload = True
        self._hasUpload = True
        self._isOutOfOrder = False
        self._startTime = None
        self._stopTime = None
        #self._runInfo = None
        self._latencyFromEnd = -1.
        self._latencyFromBeginning = -1.
        return

    def startTime(self):
        return self._startTime

    def stopTime(self):
        return self._stopTime

    def setRunNumber(self, number):
        self._runnumber = number

    def sqliteFound(self, isFound):
        self._pclRun = isFound

    def payloadFound(self, isFound):
        self._hasPayload = isFound

    def isUploaded(self, isUploaded):
        self._hasUpload = isUploaded

    def isOutoforder(self, isOutofOrder):
        self._isOutOfOrder = isOutofOrder

    def setRunInfoContent(self, runInfo):
        self._startTime = runInfo.startTime()
        self._stopTime = runInfo.stopTime()
        #self._runInfo = runInfo

    def setStartTime(self, start):
        self._startTime = start

    def setStopTime(self, stop):
        self._stopTime = stop

    # hours
    def runLenght(self):
        deltaTRun = self.stopTime() - self.startTime()
        return deltaTRun.seconds/(60.*60.)

    def setLatencyFromEnd(self, timeFromEnd):
        self._latencyFromEnd = timeFromEnd

    def setLatencyFromBeginning(self, timeFromBeginning):
        self._latencyFromBeginning = timeFromBeginning
        

    def __str__(self):
        return "--- run #: " + str(self._runnumber) + " start time: " + str(self.startTime())

    def getList(self):
        theList = [str(self._runnumber), str(self.startTime()), str(self.stopTime()), self._pclRun,  self._hasPayload, self._hasUpload, self._isOutOfOrder, float(self._latencyFromBeginning), float(self._latencyFromEnd)]
        return theList
    

import locale
locale.setlocale(locale.LC_NUMERIC, "")

def format_num(num):
    """Format a number according to given places.
    Adds commas, etc. Will truncate floats into ints!"""

    return str(num)
    try:
        inum = float(num)
        return locale.format("%.*f", (0, inum), True)

    except (ValueError, TypeError):
        return str(num)


def get_max_width(table, index):
    """Get the maximum width of the given column index"""

    return max([len(format_num(row[index])) for row in table])


def pprint_table(out, table):
    """Prints out a table of data, padded for alignment
    @param out: Output stream (file-like object)
    @param table: The table to print. A list of lists.
    Each row must have the same number of columns. """

    col_paddings = []

    for i in range(len(table[0])):
        col_paddings.append(get_max_width(table, i))

    for row in table:
        # left col
        print >> out, row[0].ljust(col_paddings[0] + 1),
        # rest of the cols
        for i in range(1, len(row)):
            col = format_num(row[i]).rjust(col_paddings[i] + 2)
            print >> out, col,
        print >> out
    
if __name__ == "__main__":


    # get the list of interesting runs from RR
    runList = []

    #print getRunList(144114)
    #runList = getRunList(144115)
#    runList = getRunList(147116)
    # 2011 data taking
    #runList = getRunList(159159)

#    runList = getRunList(1)
#     runList.append(160898)
#    runList.append(160907)

    # store the report for all collision runs
    runReports = []

    
    sumTimeFromEnd = 0.
    sumTimeFromBegin = 0.

    nSqliteFiles = 0


    # counters
    countTot = 0
    countPCLNoRun = 0
    countNoPayload = 0
    countInvertedOrder = 0
    countUploadFail = 0
    myCounter = 0

    maxtimeEnd = 0
    maxtimeBegin = 0


    cachedRuns = []
    cachedRuns.append(1)
    #cachedRuns.append(161396) #FIXME


    if os.path.exists("cache.txt"):
        cache = file("cache.txt","r")
        data = cache.readlines()
        for line in data:
            if line[0] != '#' and line != "":
                items = line.split()
                runCached = int(items[0])
                cachedRuns.append(runCached)
                startCached = getDate(items[1] + " " + items[2])
                stopCached = getDate(items[3] + " " + items[4])
                pclRunCached = False
                if items[5] == "True":
                    pclRunCached = True
                payloadFoundCached = False
                if items[6] == "True":
                    payloadFoundCached = True
                uploadCached = False
                if items[7] == "True":
                    uploadCached = True
                oooCached = False
                if items[8] == "True":
                    oooCached = True
                latencyStartCached = float(items[9])
                latencyEndCached = float(items[10])
                runReport = RunReport()
                runReport.setRunNumber(runCached)
                runReport.sqliteFound(pclRunCached)
                if not pclRunCached:
                    countPCLNoRun += 1
                runReport.setStartTime(startCached)
                runReport.setStopTime(stopCached)
                runReport.payloadFound(payloadFoundCached)
                if not payloadFoundCached:
                    countNoPayload += 1
                runReport.isUploaded(uploadCached)
                if not uploadCached:
                    countUploadFail += 1
                runReport.isOutoforder(oooCached)
                if oooCached:
                    countInvertedOrder += 1
                runReport.setLatencyFromEnd(latencyEndCached)
                if latencyEndCached > maxtimeEnd:
                    maxtimeEnd = latencyEndCached
                runReport.setLatencyFromBeginning(latencyStartCached)
                if latencyEndCached != -1:
                    sumTimeFromEnd += latencyEndCached
                if latencyStartCached > maxtimeBegin:
                    maxtimeBegin = latencyStartCached
                if latencyStartCached != -1:
                    sumTimeFromBegin += latencyStartCached
                runReports.append(runReport)
                countTot += 1
        cache.close()                
    #print runReports


    cachedRuns.sort()
    lastCachedRun = cachedRuns[len(cachedRuns)-1]
    print "last cached run #: " + str(lastCachedRun)




    # get the run list from RR for the runs not already cached
    runList = getRunList(lastCachedRun+1)    
    #if(len(runList) != 0):
    #    runList.sort()
    
    # --------------------------------------------------------------------------------
    # last run for which prompt reco was released
    #jsonData = urllib.urlopen(tier0DasSrc).read().replace("'", "\"")
    #src = "tier0.js"
    #jsonData = open(src, 'r').read().replace("'", "\"")
    #data = json.loads(jsonData)
    #wrapper = Tier0LastRun(data)

    #lastPromptRecoRun = wrapper.performTest(wrapper) - 1
    rv = RunValues()
    lastPromptRecoRun = rv.getLargestReleasedForPrompt("https://cmsweb.cern.ch/tier0/runs")
    

    # --------------------------------------------------------------------------------
    # list the IOVs in oracle
    
    # runbased tag
    listiov_run_oracle = listIov(connectOracle, tagRunOracle, passwd)
    if listiov_run_oracle[0] == 0:
        iovtableByRun_oracle = IOVTable()
        iovtableByRun_oracle.setFromListIOV(listiov_run_oracle[1])
        #iovtableByRun_oracle.printList()

    # iovbased tag
    listiov_lumi_oracle = listIov(connectOracle, tagLumiOracle, passwd)
    if listiov_lumi_oracle[0] == 0:
        iovtableByLumi_oracle = IOVTable()
        iovtableByLumi_oracle.setFromListIOV(listiov_lumi_oracle[1])

    # --------------------------------------------------------------------------------


    # --------------------------------------------------------------------------------
    # run on runs not yet cached
    isFirst = True
    lastDate = datetime.datetime
    for run in runList:

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

            # run lenght
            deltaTRun = runInfo.stopTime() - runInfo.startTime()
            deltaTRunH = deltaTRun.seconds/(60.*60.)
            
            #print runInfo.run()
            #print runInfo.startTime()
            #print runInfo.stopTime()
            #print deltaTRun
            #print deltaTRun.seconds
            

            
        rRep = RunReport()
        rRep.setRunNumber(runInfo.run())
        #rRep.setStartTime(runInfo.startTime())
        rRep.setRunInfoContent(runInfo)
        
        print "-- run #: " + blue(runInfo.run())            
        print "   start: " + str(runInfo.startTime()) + " stop: " + str(runInfo.stopTime()) + " lenght (h): " + str(deltaTRunH)
        countTot += 1

        # --- look for the file on AFS
        isFileFound = False
        emptyPayload = False
        # find the file in the afs area
        fileList = os.listdir(promptCalibDir)

        fileName = ""

        for dbFile in fileList:
            if str(run) in dbFile:
                print "   file: " + dbFile
                if isFileFound:
                    # more than one file for this run
                    print "   " + warning("***Warning") + ": more than one file for this run!"
                isFileFound = True
                modifDate = datetime.datetime.fromtimestamp(os.path.getmtime(promptCalibDir + dbFile))
                if isFirst:
                    lastDate = modifDate
                    isFirst = False
                else:
                    if modifDate < lastDate:
                        #print "last date: " + str(lastDate)
                        lastDate = modifDate
                    else:
                        print "   " + warning("Warning: ") + " this comes after the following run!!!"
                        countInvertedOrder += 1
                        rRep.isOutoforder(True)
                #                 print modifDate
                #                 print datetime.datetime.fromtimestamp(os.path.getmtime(promptCalibDir + dbFile))
                #                 # last access time
                #                 print  datetime.datetime.fromtimestamp(os.path.getatime(promptCalibDir + dbFile))
                #                 # creation time
                #                 print  datetime.datetime.fromtimestamp(os.path.getctime(promptCalibDir + dbFile))

                # delta-time from begin of run
                deltaTFromBegin = modifDate - runInfo.startTime()
                deltaTFromBeginH = deltaTFromBegin.seconds/(60.*60.)

                # delta-time from end of run
                deltaTFromEndH = 0.01
                if(modifDate > runInfo.stopTime()): 
                    deltaTFromEnd = modifDate - runInfo.stopTime()
                    deltaTFromEndH = deltaTFromEnd.seconds/(60.*60.)
                    
                # check the file size
                fileSize = os.path.getsize(promptCalibDir + dbFile)
                if fileSize == 1:
                    emptyPayload = True
                else:
                    fileName = dbFile

        rRep.sqliteFound(isFileFound)
        rRep.payloadFound(not emptyPayload)
        



        if isFileFound:
            print "   file time: " + str(modifDate) + " Delta_T begin (h): " + str(deltaTFromBeginH) + " Delta_T end (h): " + str(deltaTFromEndH)
            if(deltaTFromBeginH > maxtimeBegin):
                maxtimeBegin = deltaTFromBeginH
            if(deltaTFromEndH > maxtimeEnd):
                maxtimeEnd = deltaTFromEndH

            if not emptyPayload:
                rRep.setLatencyFromBeginning(deltaTFromBeginH)
                rRep.setLatencyFromEnd(deltaTFromEndH)

                # list the iov in the tag
                connect    = "sqlite_file:" + promptCalibDir + fileName
                listiov_run_sqlite = listIov(connect, tagRun, passwd)
                if listiov_run_sqlite[0] == 0:
                    iovtableByRun_sqlite = IOVTable()
                    iovtableByRun_sqlite.setFromListIOV(listiov_run_sqlite[1])
                    #iovtableByRun_sqlite.printList()
                    for iov in iovtableByRun_sqlite._iovList:
                        iovOracle = IOVEntry()
                        if iovtableByRun_oracle.search(iov.since(), iovOracle):
                            print "    runbased IOV found in Oracle!"
                            #print iovOracle
                        else:
                            print "    " + warning("Warning:") + " runbased IOV not found in Oracle"

                allLumiIOVFound = True
                listiov_lumi_sqlite = listIov(connect, tagLumi, passwd)
                if listiov_lumi_sqlite[0] == 0:
                    iovtableByLumi_sqlite = IOVTable()
                    iovtableByLumi_sqlite.setFromListIOV(listiov_lumi_sqlite[1])
                    #iovtableByLumi_sqlite.printList()
                    counterbla = 0
                    for iov in iovtableByLumi_sqlite._iovList:
                        iovOracle = IOVEntry()
                        if not iovtableByLumi_oracle.search(iov.since(), iovOracle):
                            #print "    Lumi based IOV found in Oracle:"
                            #print iovOracle
                            counterbla += 1
                            print "    " + warning("Warning:") + " lumibased IOV not found in Oracle for since: " + str(iov.since())
                            allLumiIOVFound = False
                if allLumiIOVFound:
                    print "    All lumibased IOVs found in oracle!"
                else:
                    print "    " + warning("Warning:") + " not all lumibased IOVs found in Oracle!!!"
                    rRep.isUploaded(False)
                    if counterbla != len(iovtableByLumi_sqlite._iovList):
                        myCounter += 1
                    
                    countUploadFail += 1

            else:
                print "   " + warning("***Warning") + ": no payload in sqlite file!"
                rRep.payloadFound(False)
                countNoPayload += 1
                rRep.setLatencyFromBeginning(deltaTFromBeginH)
                rRep.setLatencyFromEnd(deltaTFromEndH)

            sumTimeFromEnd += deltaTFromEndH
            sumTimeFromBegin += deltaTFromBeginH
            nSqliteFiles += 1
        else:
            countPCLNoRun += 1
            print "   " + warning("***Warning") + ": no sqlite file found!"



        runReports.append(rRep)



    runReports.sort(key=lambda rr: rr._runnumber)


    # -----------------------------------------------------------------
    # ---- cache the results for runs older than 48h
    last2days = datetime.timedelta(days=2)
    tableForCache =[]
    tableForCache.append(["# run", "start-time", "end-time", "PCL Run", "payload","upload","Tier0 OOO", "latency from start", "latency from end"])

    tableForLog =[]
    tableForLog.append(["# run", "start-time", "end-time", "PCL Run", "payload","upload","Tier0 OOO", "latency from start", "latency from end"])

    print str(len(runReports))
    for rep in runReports:

        twdaysago = datetime.datetime.today() - last2days
        if rep.startTime() < twdaysago:
            #print "start: " + str(rep.startTime()) + " older than " + str(twdaysago)
            tableForCache.append(rep.getList())            
        tableForLog.append(rep.getList()) 

        
    #out = sys.stdout
    cacheFile = file("cache.txt","w")
    pprint_table(cacheFile, tableForCache)
    cacheFile.close()

    #out = sys.stdout
    logFile = file(webArea + "log.txt","w")
    pprint_table(logFile, tableForLog)
    logFile.close()



    # --- printout
    print "--------------------------------------------------"

    nToFill = int(len(runReports))
    print "# of runs: " + str(nToFill)

    # --- compute average values
    averageTimeFromEnd = sumTimeFromEnd/nToFill
    averageTimeFromBegin = sumTimeFromBegin/nToFill
    print "Average time from the end-of-run: " + str(averageTimeFromEnd)
    print "Average time from the begining of run: " + str(averageTimeFromBegin)

    # --- further printout
    print "--------------------------------------------------------------"
    print "Tot. # of runs: " + str(countTot)
    print "# runs for which PCL was not run: " + str(countPCLNoRun) + " = " + str(countPCLNoRun*100./countTot) + "%"
    print "# runs for which no payload was produced: " + str(countNoPayload) + " = " + str(countNoPayload*100./countTot) + "%"
    print "# runs for which upload was out-of-order: " + str(countInvertedOrder) + " = " + str(countInvertedOrder*100./countTot) + "%"
    print "# runs for which drop box had problems: " + str(countUploadFail-countInvertedOrder) + " = " + str((countUploadFail-countInvertedOrder)*100./countTot) + "%"
    print 'last run # in prompt reco: ' + str(lastPromptRecoRun)



    if nRunsToPlot != -1:
        nToFill = nRunsToPlot

    
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


    # --- book the histos
    newlegend = TLegend(0.8,0.8,1,1)

    hTimeFromEndNew = TH1F("hTimeFromEndNew","time (h) from the end of the run",nToFill,0,nToFill)
    hTimeFromEndNew.SetMarkerStyle(20)

    hTimeFromBeginningNew = TH1F("hTimeFromBeginningNew","time (h) from the beginning of the run",nToFill,0,nToFill)
    hTimeFromBeginningNew.SetMarkerStyle(20)


    hSuccessEnd = TH1F("hSuccessEnd","success",nToFill,0,nToFill)
    hSuccessEnd.SetFillColor(408)
    hSuccessEnd.SetLineColor(408)
    newlegend.AddEntry(hSuccessEnd, "Ok","F")

    hSuccessBegin = TH1F("hSuccessBegin","success",nToFill,0,nToFill)
    hSuccessBegin.SetFillColor(408)
    hSuccessBegin.SetLineColor(408)


    hOutofOrdersEnd = TH1F("hOutofOrdersEnd","Out of order",nToFill,0,nToFill)
    hOutofOrdersEnd.SetFillColor(791)
    hOutofOrdersEnd.SetLineColor(791)
    newlegend.AddEntry(hOutofOrdersEnd, "Out of order","F")

    
    hOutofOrdersBegin = TH1F("hOutofOrdersBegin","Out of order",nToFill,0,nToFill)
    hOutofOrdersBegin.SetFillColor(791)
    hOutofOrdersBegin.SetLineColor(791)


    hNoPayloadEnd = TH1F("hNoPayloadEnd","success",nToFill,0,nToFill)
    hNoPayloadEnd.SetFillColor(611)
    hNoPayloadEnd.SetLineColor(611)
    newlegend.AddEntry(hNoPayloadEnd, "No payload","F")

    hNoPayloadBegin = TH1F("hNoPayloadBegin","success",nToFill,0,nToFill)
    hNoPayloadBegin.SetFillColor(611)
    hNoPayloadBegin.SetLineColor(611)


    hNoUploadEnd = TH1F("hNoUploadEnd","success",nToFill,0,nToFill)
    hNoUploadEnd.SetFillColor(871)
    hNoUploadEnd.SetLineColor(871)
    newlegend.AddEntry(hNoUploadEnd, "No upload","F")

    hNoUploadBegin = TH1F("hNoUploadBegin","success",nToFill,0,nToFill)
    hNoUploadBegin.SetFillColor(871)
    hNoUploadBegin.SetLineColor(871)



    hNoPCLEnd = TH1F("hNoPCLEnd","success",nToFill,0,nToFill)
    hNoPCLEnd.SetFillColor(422)
    hNoPCLEnd.SetLineColor(422)
    newlegend.AddEntry(hNoPCLEnd, "No sqlite","F")


    hNoPCLBegin = TH1F("hNoPCLBegin","success",nToFill,0,nToFill)
    hNoPCLBegin.SetFillColor(422)
    hNoPCLBegin.SetLineColor(422)

    # superimpose the average
    lineAverageFromEnd = TLine(0, averageTimeFromEnd, nToFill, averageTimeFromEnd)
    lineAverageFromEnd.SetLineColor(1)
    lineAverageFromEnd.SetLineWidth(2)
    lineAverageFromEnd.SetLineStyle(2)
    newlegend.AddEntry(lineAverageFromEnd,"average", "L")
        
    lineAverageFromBegin = TLine(0, averageTimeFromBegin, nToFill, averageTimeFromBegin)
    lineAverageFromBegin.SetLineColor(1)
    lineAverageFromBegin.SetLineWidth(2)
    lineAverageFromBegin.SetLineStyle(2)

    # --- fill the histos
    index = 1
    indexLastT0Run = 1
    maxtimeEnd = maxtimeEnd * 1.05
    maxtimeBegin = maxtimeBegin * 1.05


    minId = 0
    if nRunsToPlot != -1 and nRunsToPlot < len(runReports):
        minId = len(runReports) - nRunsToPlot


    for id in range(minId, len(runReports)):
        report = runReports[id]
        if int(report._runnumber) < int(lastPromptRecoRun):
            indexLastT0Run = index
        hTimeFromEndNew.SetBinContent(index, report._latencyFromEnd)
        hTimeFromBeginningNew.SetBinContent(index, report._latencyFromBeginning)

        hSuccessEnd.GetXaxis().SetBinLabel(index, str(report._runnumber))
        hSuccessBegin.GetXaxis().SetBinLabel(index, str(report._runnumber))

        if(report._pclRun and report._hasPayload and  report._hasUpload):
            hSuccessEnd.SetBinContent(index, maxtimeEnd)
            hSuccessBegin.SetBinContent(index, maxtimeBegin)
        elif(report._isOutOfOrder):
            hOutofOrdersEnd.SetBinContent(index, maxtimeEnd)
            hOutofOrdersBegin.SetBinContent(index, maxtimeBegin)
        elif(not report._hasPayload):
            hNoPayloadEnd.SetBinContent(index, maxtimeEnd)
            hNoPayloadBegin.SetBinContent(index, maxtimeBegin)
        elif(not report._isOutOfOrder and not report._hasUpload):
            hNoUploadEnd.SetBinContent(index, maxtimeEnd)
            hNoUploadBegin.SetBinContent(index, maxtimeBegin)
        elif(not report._pclRun):
            hNoPCLEnd.SetBinContent(index, maxtimeEnd)
            hNoPCLBegin.SetBinContent(index, maxtimeBegin)
        index += 1
        


    lineLastPromptRecoEnd = TLine(indexLastT0Run, 0, indexLastT0Run, maxtimeEnd)
    lineLastPromptRecoEnd.SetLineColor(2)
    lineLastPromptRecoEnd.SetLineWidth(3)
    lineLastPromptRecoEnd.SetLineStyle(2)
    newlegend.AddEntry(lineLastPromptRecoEnd, "Prompt-reco status", "L")


    lineLastPromptRecoBegin = TLine(indexLastT0Run, 0, indexLastT0Run, maxtimeBegin)
    lineLastPromptRecoBegin.SetLineColor(2)
    lineLastPromptRecoBegin.SetLineWidth(3)
    lineLastPromptRecoBegin.SetLineStyle(2)


    # --- draw the histos
    c4 = TCanvas("cTimeFromEndN1","cTimeFromEndN1",1200,600)
    hSuccessEnd.GetYaxis().SetRangeUser(0,maxtimeEnd)
    hSuccessEnd.Draw("")
    hSuccessEnd.GetXaxis().SetTitle("run #")
    hSuccessEnd.GetXaxis().SetTitleOffset(1.6)
    hSuccessEnd.GetYaxis().SetTitle("delay (hours)")
    hSuccessEnd.LabelsOption("v","X")

    hOutofOrdersEnd.Draw("same")
    hNoUploadEnd.Draw("same")
    hNoPayloadEnd.Draw("same")
    hNoPCLEnd.Draw("same")
    #hTimeFromEndNew.Draw("P")
    #hSuccessEnd.Draw("same")
    lineAverageFromEnd.Draw("same")
    lineLastPromptRecoEnd.Draw("same")
    hTimeFromEndNew.Draw("P,SAME")
    newlegend.Draw("same")
    if writeToWeb:
        c4.Print(webArea + 'cTimeFromEnd.png')


    c5 = TCanvas("cTimeFromBeginN","cTimeFromBeginN",1200,600)
    hSuccessBegin.GetYaxis().SetRangeUser(0,maxtimeBegin)
    hSuccessBegin.Draw("")
    hSuccessBegin.GetXaxis().SetTitle("run #")
    hSuccessBegin.GetXaxis().SetTitleOffset(1.6)
    hSuccessBegin.GetYaxis().SetTitle("delay (hours)")
    hSuccessBegin.LabelsOption("v","X")

    hOutofOrdersBegin.Draw("same")
    hNoUploadBegin.Draw("same")
    hNoPayloadBegin.Draw("same")
    hNoPCLBegin.Draw("same")
    #hTimeFromBeginNew.Draw("P")
    #hSuccessBegin.Draw("same")
    lineAverageFromBegin.Draw("same")
    lineLastPromptRecoBegin.Draw("same")
    hTimeFromBeginningNew.Draw("P,SAME")
    newlegend.Draw("same")
    hSuccessBegin.GetYaxis().Draw("same")
    if writeToWeb:
        c5.Print(webArea + 'cTimeFromBegin.png')

    


    if not writeToWeb:
        raw_input ("Enter to quit")
    else:
        #shutil.copy("log.txt", webArea + "log.txt")
        updateFile = file(webArea + "lastupdate.txt","w")
        updateFile.write(str(datetime.datetime.today()))
        updateFile.close()

#    raw_input ("Enter to quit")

#print sqFile
# modified time
#print datetime.datetime.fromtimestamp(os.path.getmtime(promptCalibDir + sqFile))
# last access time
#print  datetime.datetime.fromtimestamp(os.path.getatime(promptCalibDir + sqFile))
# creation time
#print  datetime.datetime.fromtimestamp(os.path.getctime(promptCalibDir + sqFile))

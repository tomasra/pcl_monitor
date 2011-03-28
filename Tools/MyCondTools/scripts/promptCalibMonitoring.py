#!/usr/bin/env python

import os,sys, DLFCN
sys.setdlopenflags(DLFCN.RTLD_GLOBAL+DLFCN.RTLD_LAZY)

from Tools.MyCondTools.gt_tools import *

from Tools.MyCondTools.color_tools import *
from pluginCondDBPyInterface import *
a = FWIncantation()
#os.putenv("CORAL_AUTH_PATH","/afs/cern.ch/cms/DB/conddb")
rdbms = RDBMS("/afs/cern.ch/cms/DB/conddb")

dbName =  "oracle://cms_orcoff_prod/CMS_COND_31X_RUN_INFO"
logName = "oracle://cms_orcoff_prod/CMS_COND_31X_POPCONLOG"

rdbms.setLogger(logName)
from CondCore.Utilities import iovInspector as inspect

db = rdbms.getDB(dbName)
tags = db.allTags()

# for inspecting last run after run has started  
#tag = 'runinfo_start_31X_hlt'
tag = 'runinfo_31X_hlt'
promptCalibDir = '/afs/cern.ch/cms/CAF/CMSALCA/ALCA_PROMPT/'
webArea = '/afs/cern.ch/user/c/cerminar/www/PromptCalibMonitoring/'
#webArea = './'
# for inspecting last run after run has stopped  
#tag = 'runsummary_test'


from ROOT import *
from array import array

import datetime


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
        self._runInfo = None
        self._latencyFromEnd = -1.
        self._latencyFromBeginning = -1.
        return

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
        self._runInfo = runInfo

    # hours
    def runLenght(self):
        deltaTRun = self._runInfo.stopTime() - self._runInfo.startTime()
        return deltaTRun.seconds/(60.*60.)

    def setLatencyFromEnd(self, timeFromEnd):
        self._latencyFromEnd = timeFromEnd

    def setLatencyFromBeginning(self, timeFromBeginning):
        self._latencyFromBeginning = timeFromBeginning
        

    def __str__(self):
        return "--- run #: " + str(self._runnumber) + " start time: " + str(self._runInfo.startTime())


if __name__ == "__main__":


    # get the list of interesting runs from RR
    runList = []

    #print getRunList(144114)
    #runList = getRunList(144115)
#    runList = getRunList(147116)
    # 2011 data taking
    #runList = getRunList(159159)
    #runList = getRunList(161224)
    runList = getRunList(1)
#     runList.append(160898)
#     runList.append(160907)

    # store the report for all collision runs
    runReports = []

    

    runForHisto    = array('d')
    timeFromEnd    = array('d')
    noFile         = array('d')
    noPayload      = array('d')
    timeFromBegin  = array('d')
#    timeFromBeginNoFile = array('d')

    
    sumTimeFromEnd = 0.
    sumTimeFromBegin = 0.

    nSqliteFiles = 0

    # --------------------------------------------------------------------------------
    # list the IOVs in oracle
    passwd     = "/afs/cern.ch/cms/DB/conddb"
    connectOracle =  "oracle://cms_orcoff_prod/CMS_COND_31X_BEAMSPOT"

    # runbased tag
    tagRunOracle = "BeamSpotObjects_PCL_byRun_v0_offline"
    listiov_run_oracle = listIov(connectOracle, tagRunOracle, passwd)
    if listiov_run_oracle[0] == 0:
        iovtableByRun_oracle = IOVTable()
        iovtableByRun_oracle.setFromListIOV(listiov_run_oracle[1])
        #iovtableByRun_oracle.printList()

    # iovbased tag
    tagLumiOracle = "BeamSpotObjects_PCL_byLumi_v0_prompt"
    listiov_lumi_oracle = listIov(connectOracle, tagLumiOracle, passwd)
    if listiov_lumi_oracle[0] == 0:
        iovtableByLumi_oracle = IOVTable()
        iovtableByLumi_oracle.setFromListIOV(listiov_lumi_oracle[1])

    # --------------------------------------------------------------------------------

    # counters
    countTot = 0
    countPCLNoRun = 0
    countNoPayload = 0
    countInvertedOrder = 0
    countUploadFail = 0
    myCounter = 0

    maxtimeEnd = 0
    maxtimeBegin = 0


    isFirst = True
    lastDate = datetime.datetime
    for run in runList:

        # get the information from runInfo
        try :
            log = db.lastLogEntry(tag)
            # for printing all log info present into log db 
            #print log.getState()

            # for inspecting all payloads/runs
            iov = inspect.Iov(db,tag, run,run)
        except RuntimeError :
            print error("*** Error:") + " no iov? in", tag


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
        
        # fill the arrays used for histogramming
        runForHisto.append(float(runInfo.run()))



        if isFileFound:
            print "   file time: " + str(modifDate) + " Delta_T begin (h): " + str(deltaTFromBeginH) + " Delta_T end (h): " + str(deltaTFromEndH)
            if(deltaTFromBeginH > maxtimeBegin):
                maxtimeBegin = deltaTFromBeginH
            if(deltaTFromEndH > maxtimeEnd):
                maxtimeEnd = deltaTFromEndH

            if not emptyPayload:
                timeFromEnd.append(deltaTFromEndH)
                timeFromBegin.append(deltaTFromBeginH)
                rRep.setLatencyFromBeginning(deltaTFromBeginH)
                rRep.setLatencyFromEnd(deltaTFromEndH)
                noFile.append(0.)
                noPayload.append(0.)

                # list the iov in the tag
                connect    = "sqlite_file:" + promptCalibDir + fileName
                tagLumi    = "BeamSpotObject_ByLumi"
                tagRun     = "BeamSpotObject_ByRun"
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
                timeFromEnd.append(0.)
                timeFromBegin.append(deltaTFromBeginH)
                noFile.append(0.)
                noPayload.append(deltaTFromEndH)
                rRep.setLatencyFromBeginning(deltaTFromBeginH)
                rRep.setLatencyFromEnd(deltaTFromEndH)

            sumTimeFromEnd += deltaTFromEndH
            sumTimeFromBegin += deltaTFromBeginH
            nSqliteFiles += 1
        else:
            countPCLNoRun += 1
            print "   " + warning("***Warning") + ": no sqlite file found!"

            timeFromEnd.append(0.)
            timeFromBegin.append(0.)
            noFile.append(1000.)
            noPayload.append(0.)


        runReports.append(rRep)

    # --- printout
    print "--------------------------------------------------"

    print "# of runs: " + str(len(runReports))

    averageTimeFromEnd = sumTimeFromEnd/nSqliteFiles
    averageTimeFromBegin = sumTimeFromBegin/nSqliteFiles
    print "Average time from the end-of-run: " + str(averageTimeFromEnd)
    print "Average time from the begining of run: " + str(averageTimeFromBegin)
    
    # build the plots:
    print "Filling the histo:"
    hTimeFromEnd = TH1F("hTimeFromEnd","time (h) from the end of the run",int(len(runForHisto)),0,int(len(runForHisto)))
    hTimeFromEnd.SetFillColor(40)
    fill1DHisto(hTimeFromEnd, runForHisto, timeFromEnd)

    hTimeFromBegin = TH1F("hTimeFromBegin","time (h) from the beginning of the run",int(len(runForHisto)),0,int(len(runForHisto)))
    hTimeFromBegin.SetFillColor(40)
    fill1DHisto(hTimeFromBegin, runForHisto, timeFromBegin)
    
    hNoFile = TH1F("hNoFile","time (h) from the end of the run",int(len(runForHisto)),0,int(len(runForHisto)))
    hNoFile.SetFillColor(45)
    fill1DHisto(hNoFile, runForHisto, noFile, True)

    hNoPayload = TH1F("hNoPayload","time (h) from the end of the run",int(len(runForHisto)),0,int(len(runForHisto)))
    hNoPayload.SetFillColor(49)
    fill1DHisto(hNoPayload, runForHisto, noPayload, True)



    # superimpose the average
    lineAverageFromEnd = TLine(0, averageTimeFromEnd, int(len(runForHisto)), averageTimeFromEnd)
    lineAverageFromEnd.SetLineColor(1)
    lineAverageFromEnd.SetLineWidth(2)
    lineAverageFromEnd.SetLineStyle(2)
    
    lineAverageFromBegin = TLine(0, averageTimeFromBegin, int(len(runForHisto)), averageTimeFromBegin)
    lineAverageFromBegin.SetLineColor(1)
    lineAverageFromBegin.SetLineWidth(2)
    lineAverageFromBegin.SetLineStyle(2)

    

    legend = TLegend(0.8,0.8,1,1)
#    legend.AddEntry(hTimeFromEnd,"payload","F")
    legend.AddEntry(hNoFile,"No file","F")
    legend.AddEntry(hNoPayload,"No payload","F")
    

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

    
    c2 = TCanvas("cTimeFromEnd","cTimeFromEnd",1200,600)
    hNoFile.Draw("")
    hNoFile.GetXaxis().SetTitle("run #")
    hNoFile.GetXaxis().SetTitleOffset(1.6)
    hNoFile.GetYaxis().SetTitle("delay (hours)")
    hNoFile.LabelsOption("v","X")
    hTimeFromEnd.Draw("same")
    hNoPayload.Draw("same")
    hNoFile.GetYaxis().SetRangeUser(0,hTimeFromEnd.GetMaximum()*1.05)
    lineAverageFromEnd.Draw("same")
    legend.Draw("same")
    c2.Print(webArea + 'cTimeFromEndOld.png')#FIXME
#    c2.Print(webArea + 'cTimeFromEnd.root')

    c3 = TCanvas("cTimeFromBegin","cTimeFromBegin",1200,600)
    hNoFile.Draw("")
    hNoFile.GetXaxis().SetTitle("run #")
    hNoFile.GetXaxis().SetTitleOffset(1.6)
    hNoFile.GetYaxis().SetTitle("delay (hours)")
    hNoFile.LabelsOption("v","X")
    hTimeFromBegin.Draw("same")
    hNoFile.GetYaxis().SetRangeUser(0,hTimeFromBegin.GetMaximum()*1.05)
    lineAverageFromBegin.Draw("same")
    legend.Draw("same")
    c3.Print(webArea + 'cTimeFromBeginOld.png')#FIXME



    nToFill = int(len(runReports))
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


    index = 1

    maxtimeEnd = maxtimeEnd * 1.05
    maxtimeBegin = maxtimeBegin * 1.05




    
    for report in reversed(runReports):
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
    hTimeFromEndNew.Draw("P,SAME")
    newlegend.Draw("same")
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
    hTimeFromBeginningNew.Draw("P,SAME")
    newlegend.Draw("same")
    c5.Print(webArea + 'cTimeFromBegin.png')

    


    print "--------------------------------------------------------------"
    print "Tot. # of runs: " + str(countTot)
    print "# runs for which PCL was not run: " + str(countPCLNoRun) + " = " + str(countPCLNoRun*100./countTot) + "%"
    print "# runs for which no payload was produced: " + str(countNoPayload) + " = " + str(countNoPayload*100./countTot) + "%"
    print "# runs for which upload was out-of-order: " + str(countInvertedOrder) + " = " + str(countInvertedOrder*100./countTot) + "%"
    print "# runs for whcih drop box had problems: " + str(countUploadFail-countInvertedOrder) + " = " + str((countUploadFail-countInvertedOrder)*100./countTot) + "%"

#    raw_input ("Enter to quit")


#    raw_input ("Enter to quit")

#print sqFile
# modified time
#print datetime.datetime.fromtimestamp(os.path.getmtime(promptCalibDir + sqFile))
# last access time
#print  datetime.datetime.fromtimestamp(os.path.getatime(promptCalibDir + sqFile))
# creation time
#print  datetime.datetime.fromtimestamp(os.path.getctime(promptCalibDir + sqFile))

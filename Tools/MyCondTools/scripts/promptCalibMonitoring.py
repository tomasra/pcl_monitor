#!/usr/bin/env python

import os,sys, DLFCN
sys.setdlopenflags(DLFCN.RTLD_GLOBAL+DLFCN.RTLD_LAZY)

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
    sel_runtable="{groupName} ='Collisions10' and {runNumber} >= " + str(minRun) + " and {datasetName} LIKE '%Express%'"

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


if __name__ == "__main__":


    # get the list of interesting runs from RR
    runList = []

    #print getRunList(144114)
    runList = getRunList(144115)

    runForHisto    = array('d')
    timeFromEnd    = array('d')
    failed         = array('d')

    timeFromBegin  = array('d')
#    timeFromBeginFailed = array('d')

    
    sumTimeFromEnd = 0.
    sumTimeFromBegin = 0.

    nSqliteFiles = 0
    
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
            

            


        print "-- run #: " + blue(runInfo.run())            
        print "   start: " + str(runInfo.startTime()) + " stop: " + str(runInfo.stopTime()) + " lenght (h): " + str(deltaTRunH)

        # --- look for the file on AFS
        isFileFound = False
        # find the file in the afs area
        fileList = os.listdir(promptCalibDir)

        for dbFile in fileList:
            if str(run) in dbFile:
                print "   file: " + dbFile
                if isFileFound:
                    # more than one file for this run
                    print "   " + warning("***Warning") + ": more than one file for this run!"
                isFileFound = True
                modifDate = datetime.datetime.fromtimestamp(os.path.getmtime(promptCalibDir + dbFile))
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
                deltaTFromEnd = modifDate - runInfo.stopTime()
                deltaTFromEndH = deltaTFromEnd.seconds/(60.*60.)

        # fill the arrays used for histogramming
        runForHisto.append(float(runInfo.run()))



        if isFileFound:
            print "   file time: " + str(modifDate) + " Delta_T begin (h): " + str(deltaTFromBeginH) + " Delta_T end (h): " + str(deltaTFromEndH)
            timeFromEnd.append(deltaTFromEndH)
            timeFromBegin.append(deltaTFromBeginH)
            failed.append(0.)
            sumTimeFromEnd += deltaTFromEndH
            sumTimeFromBegin += deltaTFromBeginH
            nSqliteFiles += 1
        else:

            print "   " + warning("***Warning") + ": no sqlite file found!"

            timeFromEnd.append(0.)
            timeFromBegin.append(0.)
            failed.append(1000.)

    # --- printout
    print "--------------------------------------------------"
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
    
    hNoPayload = TH1F("hNoPayload","time (h) from the end of the run",int(len(runForHisto)),0,int(len(runForHisto)))
    hNoPayload.SetFillColor(45)
    fill1DHisto(hNoPayload, runForHisto, failed, True)

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

    
    c2 = TCanvas("cTimeFromEnd","cTimeFromEnd",800,600)
    hNoPayload.Draw("")
    hNoPayload.GetXaxis().SetTitle("run #")
    hNoPayload.GetXaxis().SetTitleOffset(1.6)
    hNoPayload.GetYaxis().SetTitle("delay (hours)")
    hNoPayload.LabelsOption("v","X")
    hTimeFromEnd.Draw("same")
    hNoPayload.GetYaxis().SetRangeUser(0,hTimeFromEnd.GetMaximum()*1.05)
    lineAverageFromEnd.Draw("same")
    legend.Draw("same")
    c2.Print(webArea + 'cTimeFromEnd.png')

    c3 = TCanvas("cTimeFromBegin","cTimeFromBegin",800,600)
    hNoPayload.Draw("")
    hNoPayload.GetXaxis().SetTitle("run #")
    hNoPayload.GetXaxis().SetTitleOffset(1.6)
    hNoPayload.GetYaxis().SetTitle("delay (hours)")
    hNoPayload.LabelsOption("v","X")
    hTimeFromBegin.Draw("same")
    hNoPayload.GetYaxis().SetRangeUser(0,hTimeFromBegin.GetMaximum()*1.05)
    lineAverageFromBegin.Draw("same")
    legend.Draw("same")
    c3.Print(webArea + 'cTimeFromBegin.png')





#    raw_input ("Enter to quit")

#print sqFile
# modified time
#print datetime.datetime.fromtimestamp(os.path.getmtime(promptCalibDir + sqFile))
# last access time
#print  datetime.datetime.fromtimestamp(os.path.getatime(promptCalibDir + sqFile))
# creation time
#print  datetime.datetime.fromtimestamp(os.path.getctime(promptCalibDir + sqFile))

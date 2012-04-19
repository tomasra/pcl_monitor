#!/usr/bin/env python

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

        htmlpage.write('<li><a href=' + tier0DasSrc + '>DAS Run List </a></li>\n')
        htmlpage.write('<li><a href=' + tier0SafeCond + '>First run safe for condition update </a></li>\n')
        htmlpage.write('<li><a href=' + tier0Mon + '>Tier0Mon </a></li>\n')

        htmlpage.write('</ul>\n')

        htmlpage.write('<p>\n')
        htmlpage.write('<hr>\n')
        htmlpage.write('<address>Gianluca Cerminara</address>\n')
        htmlpage.write('</body>\n')
        htmlpage.write('</html>\n')
        htmlpage.close()




tier0DasSrc            = "https://cmsweb.cern.ch/tier0/"
webArea                = '/afs/cern.ch/user/a/alcaprod/www/Monitoring/PCLO2O/'
writeToWeb             = True

import Tools.MyCondTools.o2oMonitoringTools as o2oMonitoringTools
import Tools.MyCondTools.tier0DasInterface as tier0DasInterface
import Tools.MyCondTools.monitorStatus as monitorStatus
import Tools.MyCondTools.RunInfo as RunInfo

import ROOT
import array
import os
import datetime
import sys

#from ROOT import *
def producePlots(runReports, nRunsToPlot, maxtimeEnd, maxtimeBegin, averageTimeFromEnd, averageTimeFromBegin, lastPromptRecoRun):

    # --- set how many runs should be plotter
    nToFill = int(len(runReports))
    if nRunsToPlot != -1:
        nToFill = nRunsToPlot
    
    # --- set the style 
    # draw the plots
    ROOT.gStyle.SetOptStat(0) 
    ROOT.gStyle.SetPadBorderMode(0) 
    ROOT.gStyle.SetCanvasBorderMode(0) 
    ROOT.gStyle.SetPadColor(0);
    ROOT.gStyle.SetCanvasColor(0);
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetPadBottomMargin(0.13)
    ROOT.gStyle.SetTitleXOffset(1.6)
    ROOT.gStyle.SetTitleOffset(1.6,"X")


    # --- book the histos
    newlegend = ROOT.TLegend(0.8,0.8,1,1)

    hTimeFromEndNew = ROOT.TH1F("hTimeFromEndNew","time (h) from the end of the run",nToFill,0,nToFill)
    hTimeFromEndNew.SetMarkerStyle(20)

    hTimeFromBeginningNew = ROOT.TH1F("hTimeFromBeginningNew","time (h) from the beginning of the run",nToFill,0,nToFill)
    hTimeFromBeginningNew.SetMarkerStyle(20)


    hSuccessEnd = ROOT.TH1F("hSuccessEnd","success",nToFill,0,nToFill)
    hSuccessEnd.SetFillColor(408)
    hSuccessEnd.SetLineColor(408)
    newlegend.AddEntry(hSuccessEnd, "Ok","F")

    hSuccessBegin = ROOT.TH1F("hSuccessBegin","success",nToFill,0,nToFill)
    hSuccessBegin.SetFillColor(408)
    hSuccessBegin.SetLineColor(408)


    hOutofOrdersEnd = ROOT.TH1F("hOutofOrdersEnd","Out of order",nToFill,0,nToFill)
    hOutofOrdersEnd.SetFillColor(791)
    hOutofOrdersEnd.SetLineColor(791)
    newlegend.AddEntry(hOutofOrdersEnd, "Out of order","F")

    
    hOutofOrdersBegin = ROOT.TH1F("hOutofOrdersBegin","Out of order",nToFill,0,nToFill)
    hOutofOrdersBegin.SetFillColor(791)
    hOutofOrdersBegin.SetLineColor(791)


    hNoPayloadEnd = ROOT.TH1F("hNoPayloadEnd","success",nToFill,0,nToFill)
    hNoPayloadEnd.SetFillColor(611)
    hNoPayloadEnd.SetLineColor(611)
    newlegend.AddEntry(hNoPayloadEnd, "No payload","F")

    hNoPayloadBegin = ROOT.TH1F("hNoPayloadBegin","success",nToFill,0,nToFill)
    hNoPayloadBegin.SetFillColor(611)
    hNoPayloadBegin.SetLineColor(611)


    hNoUploadEnd = ROOT.TH1F("hNoUploadEnd","success",nToFill,0,nToFill)
    hNoUploadEnd.SetFillColor(871)
    hNoUploadEnd.SetLineColor(871)
    newlegend.AddEntry(hNoUploadEnd, "No upload","F")

    hNoUploadBegin = ROOT.TH1F("hNoUploadBegin","success",nToFill,0,nToFill)
    hNoUploadBegin.SetFillColor(871)
    hNoUploadBegin.SetLineColor(871)



    hNoPCLEnd = ROOT.TH1F("hNoPCLEnd","success",nToFill,0,nToFill)
    hNoPCLEnd.SetFillColor(422)
    hNoPCLEnd.SetLineColor(422)
    newlegend.AddEntry(hNoPCLEnd, "PCL not run","F")


    hNoPCLBegin = ROOT.TH1F("hNoPCLBegin","success",nToFill,0,nToFill)
    hNoPCLBegin.SetFillColor(422)
    hNoPCLBegin.SetLineColor(422)

    # superimpose the average
    lineAverageFromEnd = ROOT.TLine(0, averageTimeFromEnd, nToFill, averageTimeFromEnd)
    lineAverageFromEnd.SetLineColor(1)
    lineAverageFromEnd.SetLineWidth(2)
    lineAverageFromEnd.SetLineStyle(2)
    newlegend.AddEntry(lineAverageFromEnd,"average", "L")
        
    lineAverageFromBegin = ROOT.TLine(0, averageTimeFromBegin, nToFill, averageTimeFromBegin)
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
        


    lineLastPromptRecoEnd = ROOT.TLine(indexLastT0Run, 0, indexLastT0Run, maxtimeEnd)
    lineLastPromptRecoEnd.SetLineColor(2)
    lineLastPromptRecoEnd.SetLineWidth(3)
    lineLastPromptRecoEnd.SetLineStyle(2)
    newlegend.AddEntry(lineLastPromptRecoEnd, "Prompt-reco status", "L")


    lineLastPromptRecoBegin = ROOT.TLine(indexLastT0Run, 0, indexLastT0Run, maxtimeBegin)
    lineLastPromptRecoBegin.SetLineColor(2)
    lineLastPromptRecoBegin.SetLineWidth(3)
    lineLastPromptRecoBegin.SetLineStyle(2)


    # --- draw the histos
    c4 = ROOT.TCanvas("cTimeFromEndN1","cTimeFromEndN1",1200,600)
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


    c5 = ROOT.TCanvas("cTimeFromBeginN","cTimeFromBeginN",1200,600)
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

    

if __name__ == "__main__":

    # get the run reports from the file
    allCachedRuns = o2oMonitoringTools.readCache(webArea + "log.txt")
    cachedRuns = allCachedRuns[0]
    runReports = allCachedRuns[1]



    tier0Das = tier0DasInterface.Tier0DasInterface(tier0DasSrc) 
    try:
        nextPromptRecoRun = tier0Das.firstConditionSafeRun()
        print "Tier0 DAS next run for prompt reco:",nextPromptRecoRun
        #gtFromPrompt = tier0Das.promptGlobalTag(nextPromptRecoRun, referenceDataset)
        #print "      GT for dataset: ", referenceDataset, "run:", str(nextPromptRecoRun), ":", gtFromPrompt
    except Exception as error:
        print '*** Error 2: Tier0-DAS query has failed'
        print error
        sys.exit(102)

    pageWriter = WebPageWriter()
    pageWriter.setLastPromptReco(int(nextPromptRecoRun))

    # FIXME: this needs to come from the cache
    #pageWriter.addRecordReport(recordName, rcdRep)

    runReports.sort(key=lambda rr: rr._runnumber)

    for rRep in runReports:
        print rRep
        deltaTRun = rRep.stopTime() - rRep.startTime()
        deltaTRunH = deltaTRun.seconds/(60.*60.)
        pageWriter.setNextPromptReco(rRep.runNumber(), rRep.startTime(), rRep.stopTime(), deltaTRunH)

    sys.exit(0)

    nToFill = 100
    nRuns = int(len(runReports))

    minId = 0
    if nToFill != -1 and nToFill < nRuns:
        minId = nRuns - nToFill
    else:
        nToFill = nRuns

    # global counters
    avgDelayFromRunEnd = 0
    avgDelayFromRunBegin = 0
    nPCLNotRun = 0
    nNoPayload = 0
    nOutOfOrder = 0
    nUploadproblems = 0

    # counters for last n runs (where n = nToFill)
    avgDelayFromRunEnd_lastN = 0
    avgDelayFromRunBegin_lastN = 0
    nPCLNotRun_lastN = 0
    nNoPayload_lastN = 0
    nOutOfOrder_lastN = 0
    nUploadproblems_lastN = 0

    index = 1

    maxTimeFromEnd = 0
    maxTimeFromBegin = 0

    for rRep in runReports:
        #print rRep
        if not rRep._pclRun:
            nPCLNotRun += 1
            if index > minId:
                nPCLNotRun_lastN += 1
        if not rRep._hasPayload:
            nNoPayload += 1
            if index > minId:
                nNoPayload_lastN += 1
        if rRep._isOutOfOrder:
            nOutOfOrder += 1
            if index > minId:
                nOutOfOrder_lastN += 1      
        if not rRep._hasUpload:
            nUploadproblems += 1
            if index > minId:
                nUploadproblems_lastN += 1
        avgDelayFromRunEnd += rRep._latencyFromEnd
        avgDelayFromRunBegin += rRep._latencyFromBeginning
        if index > minId:
            avgDelayFromRunEnd_lastN += rRep._latencyFromEnd
            avgDelayFromRunBegin_lastN += rRep._latencyFromBeginning
            if rRep._pclRun:
                if rRep._latencyFromEnd > maxTimeFromEnd:
                    maxTimeFromEnd = rRep._latencyFromEnd
                if rRep._latencyFromBeginning > maxTimeFromBegin:
                    maxTimeFromBegin = rRep._latencyFromBeginning
        index += 1
    
    avgDelayFromRunEnd = avgDelayFromRunEnd/nRuns
    avgDelayFromRunBegin = avgDelayFromRunBegin/nRuns

    avgDelayFromRunEnd_lastN = avgDelayFromRunEnd_lastN/nToFill
    avgDelayFromRunBegin_lastN = avgDelayFromRunBegin_lastN/nToFill

    tier0Das = tier0DasInterface.Tier0DasInterface(tier0DasSrc) 
    lastPromptRecoRun = 1
    try:
        lastPromptRecoRun = tier0Das.lastPromptRun()
        print "Tier0 DAS last run released for PROMPT:       ", lastPromptRecoRun
        #print "Tier0 DAS first run safe for condition update:", tier0Das.firstConditionSafeRun()
    except Exception as error:
        print '*** Error: Tier0-DAS query has failed'
        print error



    

    producePlots(runReports, nToFill, maxTimeFromEnd, maxTimeFromBegin, avgDelayFromRunEnd_lastN, avgDelayFromRunBegin_lastN, lastPromptRecoRun)

    # --- printout
    print "--------------------------------------------------"

    print "Total # of runs:", nRuns
    # --- compute average values
    print "Average time from the end-of-run: " + str(avgDelayFromRunEnd)
    print "Average time from the begining of run: " + str(avgDelayFromRunBegin)
    print "# runs for which PCL was not run: " + str(nPCLNotRun) + " = " + str(nPCLNotRun*100./nRuns) + "%"
    print "# runs for which no payload was produced: " + str(nNoPayload) + " = " + str(nNoPayload*100./nRuns) + "%"
    print "# runs for which upload was out-of-order: " + str(nOutOfOrder) + " = " + str(nOutOfOrder*100./nRuns) + "%"
    print "# runs for which had upload problems: " + str(nUploadproblems) + " = " + str(nUploadproblems*100./nRuns) + "%"
    
    print "--------------------------------------------------"
    print "Last ", nToFill, " runs"
    print "Average time from the end-of-run: " + str(avgDelayFromRunEnd_lastN)
    print "Average time from the begining of run: " + str(avgDelayFromRunBegin_lastN)
    print "# runs for which PCL was not run: " + str(nPCLNotRun_lastN) + " = " + str(nPCLNotRun_lastN*100./nToFill) + "%"
    print "# runs for which no payload was produced: " + str(nNoPayload_lastN) + " = " + str(nNoPayload_lastN*100./nToFill) + "%"
    print "# runs for which upload was out-of-order: " + str(nOutOfOrder_lastN) + " = " + str(nOutOfOrder_lastN*100./nToFill) + "%"
    print "# runs for which had upload problems: " + str(nUploadproblems_lastN) + " = " + str(nUploadproblems_lastN*100./nToFill) + "%"
    
    print '--- last run # in prompt reco: ' + str(lastPromptRecoRun)    

    status = monitorStatus.MonitorStatus('read')
    status.readJsonFile(webArea + "status.json")
    
    os.chdir(webArea)
    htmlwriter = WebPageWriter()
    htmlwriter.setNRunsShown(nToFill)
    htmlwriter.setBackendUpdateDate(status.getField('update'))
    htmlwriter.statusSummary(status.getField('status'),status.getField('msg'))
    #update = datetime.datetime
    update = RunInfo.getDate(status.getField('update'))
    deltatfromend = datetime.datetime.today() - update
#    deltatfromendH = deltatfromend.days*24. + deltatfromend.seconds/(60.*60.)
    #print deltatfromendH
    htmlwriter.setOldUpdateWarning(deltatfromend)



    htmlwriter.buildPage()

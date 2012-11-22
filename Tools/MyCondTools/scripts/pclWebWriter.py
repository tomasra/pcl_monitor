#!/usr/bin/env python


import ConfigParser as ConfigParser
#from ConfigParser import ConfigParser


# --------------------------------------------------------------------------------
# configuration

# read a global configuration file
cfgfile = ConfigParser.ConfigParser()
cfgfile.optionxform = str

CONFIGFILE = "GT_branches/pclMonitoring.cfg"
print 'Reading configuration file from ',CONFIGFILE
cfgfile.read([ CONFIGFILE ])

tier0DasSrc                 = cfgfile.get('Common','tier0DasSrc')
webArea                     = cfgfile.get('PCLMonitor','webArea')


writeToWeb             = True


class WebPageWriter:
    def __init__(self):
        self._fineName ="./index.html"
        self._title = "Monitoring of Prompt Calibration Loop"
        self._version = "2.0"
        self._nRunsInPlot = 100
        self._statusCode = -1
        self._statusMsg = ""
        self._statusImg = "../common/img/warning.png"
        self._backEndUpdate = datetime.datetime
        self._udateAge = datetime.timedelta

    def setBackendUpdateDate(self, date):
        self._backEndUpdate = date
        
    def setNRunsShown(self, nRuns):
        self._nRunsInPlot = nRuns


    def setOldUpdateWarning(self, age):
        self._udateAge = age
        
        
    def statusSummary(self, code, message):
        self._statusCode = code
        self._statusMsg = message
        if self._statusCode == 0:
            self._statusImg = "../common/imgs/ok.png"
            self._statusMsg = '<b>OK: </b> ' + self._statusMsg
        elif self._statusCode <= 10:
            self._statusImg = "../common/imgs/warning.png"
            self._statusMsg = '<b>WARNING: </b> ' + self._statusMsg
        else:
            self._statusImg = "../common/imgs/error.png"
            self._statusMsg = '<b>ERROR: </b> ' + self._statusMsg
            

    def buildPage(self):
        htmlpage = file(self._fineName,"w")
        htmlpage.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n')
        htmlpage.write('<html><head>\n')
        htmlpage.write('<link rel="stylesheet" type="text/css" href="../common/PromptCalibMonitoring.css">\n')
        htmlpage.write('<META HTTP-EQUIV="REFRESH" CONTENT="3600">\n')
        htmlpage.write('<title>' + self._title + '</title>\n')
        htmlpage.write('</head>\n')
        htmlpage.write('<body>\n')
        htmlpage.write('<center><h1>' + self._title + '</h1></center>\n<hr>\n')
        #htmlpage.write('<center>[<a href=./index.html>index</a>]</center><br>\n')
        htmlpage.write('<p>\n')


        htmlpage.write('<p>This page shows <b>monitoring</b> and <b>statistics</b> about the prompt-calibration loop running @ Tier0.</p>\n')
        htmlpage.write('<p>The following plots show the latency of the production step in hours. The dashed black line is the current average value. The monitoring is limited to the last ' + str(self._nRunsInPlot) + ' <i>collision</i> runs (based on Run-Registry).</p>\n')        
        
        htmlpage.write('<table width="100%">\n')
        if self._statusCode != -1 :
            htmlpage.write('<tr><td><h4>Status summary of last 48h</h4></td></tr>\n')
            htmlpage.write('<tr><td><table><tr><td><img src="' + self._statusImg + '" width="20"></td><td>' + self._statusMsg + '</td><td>(Last update on: ' + str(self._backEndUpdate) + ')</td></tr></table></td></tr>\n')

        if self._udateAge >  datetime.timedelta(hours=2,minutes=0):
            htmlpage.write('<tr><td><img src="../common/imgs/warning.png" width="20"><b>WARNING:</b> last update is more than ' + str(self._udateAge) + ' hours old</td></tr>\n')
            
        htmlpage.write('<tr><td><h4>Latency since the beginning of the run (h)</h4></td></tr>\n')
        htmlpage.write('<tr><td><img src="./cTimeFromBegin.png" width="1200"></td></tr>\n')
        htmlpage.write('<tr><td><h4>Latency since the end of the run (h)</h4></td></tr>\n')
        htmlpage.write('<tr><td><img src="./cTimeFromEnd.png" width="1200"></td></tr>\n')
        htmlpage.write('</table>\n')

        htmlpage.write('<p>Full logs can be accessed here: <a href=log.txt>log.txt</a></p>\n')

        htmlpage.write('<hr>\n')
        htmlpage.write('<center>[<a href=./' + self._fineName + '>back to the top</a>]</center>\n')

        htmlpage.write('<address>Gianluca Cerminara</address>\n')
        htmlpage.write('<p>Page generated on: ' + str(datetime.datetime.today()) + '</p>\n')
        htmlpage.write('</body>\n')
        htmlpage.write('</html>\n')
        htmlpage.close()










import Tools.MyCondTools.pclMonitoringTools as pclMonitoringTools
import Tools.MyCondTools.tier0DasInterface as tier0DasInterface
import Tools.MyCondTools.monitorStatus as monitorStatus
import Tools.MyCondTools.RunInfo as RunInfo

import ROOT
import array
import os
import datetime

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
    allCachedRuns = pclMonitoringTools.readCache(webArea + "log.txt")
    cachedRuns = allCachedRuns[0]
    runReports = allCachedRuns[1]
    runReports.sort(key=lambda rr: rr._runnumber)


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

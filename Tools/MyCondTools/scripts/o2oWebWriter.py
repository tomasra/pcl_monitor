#!/usr/bin/env python



############################################################################################
#
# Description:
# This script creates the web-pages for the monitoring of the O2O Jobs for PCL.
# The configuration is handled via the INI file:  GT_branches/pclMonitoring.cfg
# which is common to the "back-end" part and all other PCL monitoring tools.
# The web page is created relying on the data created by the script "o2oMonitor.py"
# which implements the real montoring. The output of this script are static html pages
# and a "status" JSON file used by the mail notification and eventually by the NAGIOS plugin.
#
# $Date: 2012/05/31 10:43:32 $
# $Revision: 1.3 $
# Author: G.Cerminara
#
############################################################################################


import Tools.MyCondTools.o2oMonitoringTools as o2oMonitoringTools
import Tools.MyCondTools.tier0WMADasInterface as tier0DasInterface
import Tools.MyCondTools.monitorStatus as monitorStatus
import Tools.MyCondTools.RunInfo as RunInfo

import ROOT
import array
import os
import datetime
import sys




import ConfigParser as ConfigParser
#from ConfigParser import ConfigParser



# read a global configuration file
cfgfile = ConfigParser.ConfigParser()
cfgfile.optionxform = str

CONFIGFILE = "GT_branches/pclMonitoring.cfg"
print 'Reading configuration file from ',CONFIGFILE
cfgfile.read([ CONFIGFILE ])


tier0DasSrc                 = cfgfile.get('Common','tier0DasSrc')
webArea                     = cfgfile.get('O2OMonitor','webArea')

tier0SafeCond          = tier0DasSrc + "firstconditionsaferun"
tier0Mon               = tier0DasSrc.split('tier0')[0] + "T0Mon/static/pages/index.html"








class WebPageWriter:
    """
    This class generates the static html page showing the results of the monitoring.
    """
    def __init__(self):
        self._recordReports = dict()
        self._records = []
        self._lastPromptRecoRun = -1
        self._nextPromptRecoRun = -1
        self._nextPromptRecoRunStart = None
        self._nextPromptRecoRunStop = None
        self._nextPromptRecoRunLenght = -1
        self._backEndUpdate = datetime.datetime
        self._statusMsg = ""
        self._statusImg = "../common/img/warning.png"
        self._udateAge = datetime.timedelta

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

    def setBackendUpdateDate(self, date):
        self._backEndUpdate = date

    def statusSummary(self, code, message):
        self._statusCode = code
        self._statusMsg = message
        if self._statusCode == 0:
            self._statusImg = "../common/imgs/ok.png"
            self._statusMsg = '<b>OK: </b> ' + self._statusMsg
        else:
            self._statusImg = "../common/imgs/error.png"
            self._statusMsg = '<b>ERROR: </b> ' + self._statusMsg


    def setOldUpdateWarning(self, age):
        self._udateAge = age


    def buildPage(self, dirName):
        htmlpage = file(dirName + '/' + 'index.html',"w")
        htmlpage.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n')
        htmlpage.write('<html><head>\n')
        htmlpage.write('<link rel="stylesheet" type="text/css" href="../common/PromptCalibMonitoring.css">\n')
        htmlpage.write('<META HTTP-EQUIV="REFRESH" CONTENT="1800">\n')
        htmlpage.write('<title>Monitoring of Tags in the Prompt-calibration Loop</title>\n')
        htmlpage.write('</head>\n')
        htmlpage.write('<body>\n')
        htmlpage.write('<center><h1>Monitoring of Tags in the Prompt-calibration Loop</h1></center>\n<hr>\n')
        htmlpage.write('<center>')
        for rcd in self._records:
            htmlpage.write('[<a href=#' + rcd + '>' + rcd + '</a>]')
        htmlpage.write('</center><br>\n')
        #htmlpage.write('<p>Last update: ' + str(datetime.datetime.today()) + '</p>\n')
        htmlpage.write('<p>Last run released for Prompt-Reco: ' + str(self._lastPromptRecoRun) + '</p>\n')
        htmlpage.write('<p>Next <b>Collision</b> run to be released for Prompt-Reco: ' + str(self._nextPromptRecoRun) + ' start time: ' + str(self._nextPromptRecoRunStart) + ' stop time: ' + str(self._nextPromptRecoRunStop) + ' length (h): ' + str(self._nextPromptRecoRunLenght) + '</p>\n')
        htmlpage.write('<p><b>Next</b> the O2O processes run every 2 hours. It might happen that no new payload are written in that case the "date" might be old. Unless there are runs not covered by the last IOV that are about to be released for prompt-reco this is usually not a problem. Anyhow keep an eye on it...</p>\n')


        htmlpage.write('<table width="100%">\n')
        htmlpage.write('<tr><td><h3>Status summary of last 48h</h3></td></tr>\n')
        htmlpage.write('<tr><td><table><tr><td><img src="' + self._statusImg + '" width="20"></td><td>' + self._statusMsg + '</td><td>(Last update on: ' + str(self._backEndUpdate) + ')</td></tr></table></td></tr>\n')

        if self._udateAge >  datetime.timedelta(hours=2,minutes=0):
            htmlpage.write('<tr><td><img src="../common/imgs/warning.png" width="20"><b>WARNING:</b> last update is more than ' + str(self._udateAge) + ' hours old</td></tr>\n')
        htmlpage.write('</table>\n')


        for rcd in self._records:
            rpt = self._recordReports[rcd]
            htmlpage.write('<h3>' + rcd + '</h3><a name=' + rcd + '></a>\n')
            htmlpage.write('<table width="100%">\n')
            htmlpage.write('<tr><td><b>Tag:</b> ' + rpt.getProperty('tagName') + ', <b>account:</b> ' + rpt.getProperty('accountName') + '</td><td><b>status</b>:</td></tr>\n')

            img = "warning.png"
            if rpt.getProperty('lastRunStatus') == "ERROR":
                img = "error.png"
            elif rpt.getProperty('lastRunStatus') == "OK":
                img = "ok.png"

            htmlpage.write('<tr><td><b>Last O2O run @:</b> ' + str(rpt.getProperty('lastRun')) + ', (' + str(rpt.getProperty('lastRunAge')) + ' hours ago)</td><td>' + str(rpt.getProperty('lastRunStatus')) + ' <img src="../common/imgs/' + img + '" width="20"></td></tr>\n')


            img = "warning.png"
            if rpt.getProperty('lastWriteStatus') == "ERROR":
                img = "error.png"
            elif rpt.getProperty('lastWriteStatus') == "OK":
                img = "ok.png"

            htmlpage.write('<tr><td><b>Last O2O wrote @:</b> ' + str(rpt.getProperty('lastWrite')) + ', (' + str(rpt.getProperty('lastWriteAge')) + ' hours ago)</td><td>' + str(rpt.getProperty('lastWriteStatus')) + ' <img src="../common/imgs/' + img + '" width="20"></td></tr>\n')
            imgSince = "ok.png"
            if rpt.getProperty('lastSinceStatus') != "OK":
                imgSince = "error.png"
            htmlpage.write('<tr><td><b>Last Since in the DB:</b> ' + str(rpt.getProperty('lastSince')) + ', (' + str(rpt.getProperty('lastSinceAge')) + ' hours old)</td><td>' + rpt.getProperty('lastSinceStatus') + ' <img src="../common/imgs/' + imgSince + '" width="20"></td></tr>\n')
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
        htmlpage.write('<p>Page generated on: ' + str(datetime.datetime.today()) + '</p>\n')
        htmlpage.write('</body>\n')
        htmlpage.write('</html>\n')
        htmlpage.close()





#from ROOT import *
def producePlots(tagsTomonitor, runReports, lastPromptRecoRun):
    """
    Draw a plot (using PyROOT) for each record to be montiored showing graphically the
    content of the runReports. The plots are saved in png format to the webArea.
    """
    # ================================================================================
    # draw a plot for each record
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


    from array import array
    colorError = array('i')
    colorError.append(408)
    colorError.append(791)
    colorError.append(611)
    ROOT.gStyle.SetPalette(3,colorError)

    # --- book the histos
    newlegend = ROOT.TLegend(0.8,0.8,1,1)
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
        recordName = entry.getProperty('recordName')
        hStatus = ROOT.TH2F('h'+recordName, "Status for record: " + recordName, nToFill,0,nToFill, 1, 0, 1)
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

    lineLastPromptRecoEnd = ROOT.TLine(indexLastT0Run, 0, indexLastT0Run, 1)
    lineLastPromptRecoEnd.SetLineColor(2)
    lineLastPromptRecoEnd.SetLineWidth(3)
    lineLastPromptRecoEnd.SetLineStyle(2)
    newlegend.AddEntry(lineLastPromptRecoEnd, "Prompt-reco status", "L")

    for rcdidx in range(0, len(tagsTomonitor)):
        record = tagsTomonitor[rcdidx].getProperty('recordName')
        c4 = ROOT.TCanvas("c" + record,"c" + record,1200,200)
        c4.GetPad(0).SetBottomMargin(0.5)
        c4.GetPad(0).SetLeftMargin(0.01)
        c4.GetPad(0).SetRightMargin(0.02)

        hist = histoPerRecord[record]
        hist.SetMaximum(1)
        hist.SetMinimum(0)
        hist.GetXaxis().SetLabelSize(0.12)
        hist.GetYaxis().SetNdivisions(1)
        hist.Draw("COL")
        lineLastPromptRecoEnd.Draw("same")
        newlegend.Draw("same")
        c4.Print(webArea + 'c' + record + '.png')
        #raw_input ("Enter to quit")




    

if __name__ == "__main__":

    # get the run reports from the file
    allCachedRuns = o2oMonitoringTools.readCache(webArea + "log.txt")
    cachedRuns = allCachedRuns[0]
    runReports = allCachedRuns[1]



    tier0Das = tier0DasInterface.Tier0DasInterface(tier0DasSrc) 
    try:
        nextPromptRecoRun = tier0Das.firstConditionSafeRun()
        lastPromptRecoRun = tier0Das.lastPromptRun()

        print "Tier0 DAS next run for prompt reco:",nextPromptRecoRun
        #gtFromPrompt = tier0Das.promptGlobalTag(nextPromptRecoRun, referenceDataset)
        #print "      GT for dataset: ", referenceDataset, "run:", str(nextPromptRecoRun), ":", gtFromPrompt
    except Exception as error:
        print '*** Error 2: Tier0-DAS query has failed'
        print error
        #FIXME
        sys.exit(102)
    
    pageWriter = WebPageWriter()
    pageWriter.setLastPromptReco(int(lastPromptRecoRun))

    rcdReports = []
    
    # read the record reports from the json file
    rcdJson = o2oMonitoringTools.O2ORecordJson("o2oMonitor")
    rcdJson.readJsonFile(webArea)
    for rcd in rcdJson.getRecordIds():
        pageWriter.addRecordReport(rcd, rcdJson.getRecordReport(rcd))
        rcdReports.append(rcdJson.getRecordReport(rcd))

    runReports.sort(key=lambda rr: rr._runnumber)

    nextFound = False
    for rRep in runReports:
        print rRep
        deltaTRun = rRep.stopTime() - rRep.startTime()
        deltaTRunH = deltaTRun.seconds/(60.*60.)
        # FIXME
        if rRep.runNumber() > lastPromptRecoRun and not nextFound:
            pageWriter.setNextPromptReco(rRep.runNumber(), rRep.startTime(), rRep.stopTime(), deltaTRunH)
            nextFound = True
            
    producePlots(rcdReports, runReports, nextPromptRecoRun)

    status = monitorStatus.MonitorStatus('read')
    status.readJsonFile(webArea + "status.json")



    pageWriter.setBackendUpdateDate(status.getField('update'))
    pageWriter.statusSummary(status.getField('status'),status.getField('msg'))

    #update = datetime.datetime
    update = RunInfo.getDate(status.getField('update'))
    deltatfromend = datetime.datetime.today() - update
#    deltatfromendH = deltatfromend.days*24. + deltatfromend.seconds/(60.*60.)
    #print deltatfromendH
    pageWriter.setOldUpdateWarning(deltatfromend)




    pageWriter.buildPage(webArea)

    sys.exit(0)


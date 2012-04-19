#!/usr/bin/env python

import os
import sys

from ConfigParser import ConfigParser

import Tools.MyCondTools.RunRegistryTools as RunRegistryTools
import Tools.MyCondTools.alcaRecoMonitoringTools as alcaRecoMonitoringTools

#from Tools.MyCondTools.RunValues import *



import shutil



from ROOT import *
from array import array

import datetime

import os,string,sys,commands,time
#import xmlrpclib


    
if __name__ == "__main__":

    # --------------------------------------------------------
    # --- Get the configuration from file
    
    configfile = ConfigParser()
    configfile.optionxform = str

    configfile.read('GT_branches/AlCaRecoMonitoring.cfg')
    webArea = configfile.get('Common','webArea')
    groups = configfile.get('Common','groups').split(",")
    refreshCache = bool(configfile.get('Common','refreshCache'))

    # list of datasets to be monitored
    alcarecoDatasets = []

    os.chdir(webArea)



    # 1 find all the alcarecos and theyr parets for each "group"
    for group in groups:
        if group == "":
            continue
        print "--------------------------------------------"
        print "--------------------------------------------"
        print "==== Group: " + group
        epoch = configfile.get(group, 'epoch')
        version = configfile.get(group, 'version')
        rawversion = configfile.get(group, 'rawversion')
        htmlwriter = alcaRecoMonitoringTools.WebPageWriter(group, epoch, version)
        jsonDatasetList = alcaRecoMonitoringTools.AlcaRecoDatasetJson(group)
        jsonDatasetList.readJsonFile()

        for dataset in jsonDatasetList.getDatasets():
            details = jsonDatasetList.getDatasetDetails(dataset)
            htmlwriter.addDataset(details.pd(), details)
            alcarecoDatasets.append(alcaRecoMonitoringTools.DBSAlCaRecoResults(dataset, ""))

        htmlwriter.buildPage()

    indexBuilder = alcaRecoMonitoringTools.WebPageIndex()
    indexBuilder.scan(webArea)
    indexBuilder.buildPage()
    
    # --- set the style 
    gStyle.SetOptStat(0) 
    gStyle.SetPadBorderMode(0) 
    gStyle.SetCanvasBorderMode(0) 
    gStyle.SetPadColor(0);
    gStyle.SetCanvasColor(0);
    gStyle.SetOptTitle(0)
    gStyle.SetPadBottomMargin(0.13)
    gStyle.SetTitleXOffset(1.6)
    gStyle.SetTitleOffset(1.6,"X")
    gStyle.SetPadGridY(True)

    for dataset in alcarecoDatasets:
        print dataset.name()
        dataset.readCache()
        
        label1 = TLatex(0.012, 0.94007, dataset.name())
        label1.SetNDC(True)
        hNEvents = dataset.buildHistoNEvents()
        c1 = TCanvas(hNEvents.GetName(),"hNEvents",1200,600)
        hNEvents.Draw("")
        label1.Draw("same")
        c1.Print(".png")
        hEff = dataset.buildHistoEff()
        c2 = TCanvas(hEff.GetName(),"hEff",1200,600)
        c2.cd()
        hEff.Draw("")
        label1.Draw("same")
        c2.Print(".png")

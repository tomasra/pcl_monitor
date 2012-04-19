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
        jsonDatasetList = alcaRecoMonitoringTools.AlcaRecoDatasetJson(group)
        datasets = alcaRecoMonitoringTools.getDatasets("*",epoch, version, "ALCARECO")
        for dataset in datasets:
            pd = dataset.split("/")[1]
            parenttier = "RECO"
            # exception
            if group == "Run2011A-v4":
                parenttier = "RAW"
            pdforhtml = pd
            details = alcaRecoMonitoringTools.AlcaRecoDetails(dataset, pdforhtml, epoch, version)
            if pd == 'StreamExpressCosmics':
                continue
            jsonDatasetList.addDataset(dataset, details)
            if pd == 'StreamExpress':
                pd = 'ExpressPhysics'
                parenttier = "FEVT"
            if pd == 'StreamHIExpress':
                pd = 'HIExpressPhysics'
                parenttier = "FEVT"
            parent = alcaRecoMonitoringTools.getDatasets(pd,epoch, version, parenttier)
            if len(parent) == 0 or parent[0] == '':
                parent = alcaRecoMonitoringTools.getDatasets(pd,epoch, rawversion,"RAW")
            print "--------------------------------------------"
            print "dataset: " + dataset
            print "parent: " + parent[0]
            alcarecoDatasets.append(alcaRecoMonitoringTools.DBSAlCaRecoResults(dataset, parent[0]))
        jsonDatasetList.writeJsonFile()


    #2 get the statistics and draw the results
    cachedlisttype = "DUMMY"
    cachedlist = []
    


    
    for dataset in alcarecoDatasets:
        print dataset.name()
        lastCached = dataset.readCache() #FIXME
        #lastCached = 160404
        if refreshCache:
            # FIXME: max run (used to limit the size of the query)
            maxRun = -1
            #maxRun = lastCached + 500
            query = alcaRecoMonitoringTools.dbsQuery(dataset.name(), lastCached, maxRun)
            dataset.appendQuery(query[1])
            queryParent = alcaRecoMonitoringTools.dbsQuery(dataset.parent(), lastCached, maxRun)
            dataset.addParentQuery(queryParent[1])

            rrSet = ""
            if "2010" in  dataset.name():
                rrSet = "Collisions10"
            elif "2011" in dataset.name():
                rrSet = "Collisions11"
            elif "2012" in dataset.name():
                rrSet = "Collisions12"


            # cache the list from RR
            if rrSet != cachedlisttype:
                cachedlisttype = rrSet
                #cachedlist = getRunList(1, rrSet)
                cachedlist = RunRegistryTools.getRunListRR3(1, "Online", "Collisions12")

                
            runList = cachedlist            
            print "RR: " + rrSet + " # runs: " + str(len(runList))
            #print runList

            dataset.purgeList(runList)
            dataset.printAll()
            dataset.writeCache()

    #raw_input ("Enter to quit")
    sys.exit(0)
    
    

    

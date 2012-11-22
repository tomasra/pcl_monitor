#!/usr/bin/env python

from Tools.MyCondTools.gt_tools import *
from Tools.MyCondTools.color_tools import *
#from Tools.MyCondTools.Tier0LastRun import *
#from Tools.MyCondTools.RunValues import *

from Tools.MyCondTools.RunInfo import *


import Tools.MyCondTools.RunRegistryTools as RunRegistryTools
import Tools.MyCondTools.tier0DasInterface as tier0DasInterface
import Tools.MyCondTools.pclMonitoringTools as pclMonitoringTools



import shutil



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


runinfoTag                  = cfgfile.get('Common','runinfoTag')
tier0DasSrc                 = cfgfile.get('Common','tier0DasSrc')
passwdfile                  = cfgfile.get('Common','passwdfile')



taskName                    = cfgfile.get('PCLMonitor','taskName')
promptCalibDir              = cfgfile.get('PCLMonitor','promptCalibDir')
weburl                      = cfgfile.get('PCLMonitor','weburl')
webArea                     = cfgfile.get('PCLMonitor','webArea')
tagLumi                     = cfgfile.get('PCLMonitor','tagBSLumi')
tagRun                      = cfgfile.get('PCLMonitor','tagBSRun')
connectOracle               = cfgfile.get('PCLMonitor','connectBSOracle')
tagRunOracle                = cfgfile.get('PCLMonitor','tagBSRunOracle')
tagLumiOracle               = cfgfile.get('PCLMonitor','tagBSLumiOracle')
cacheFileName               = cfgfile.get('PCLMonitor','cacheFileName')
rrDatasetName               = cfgfile.get('PCLMonitor','rrDatasetName')
rrRunClassName              = cfgfile.get('PCLMonitor','rrRunClassName')
firstRunToMonitor           = int(cfgfile.get('PCLMonitor','firstRunToMonitor'))








#os.putenv("CORAL_AUTH_PATH","/afs/cern.ch/cms/DB/conddb")






import datetime

# -- status must include:
# 1. errori nell'esecuzione -> exit code !=0 + messaggio di descrizione
# 2. problema PCL -> exit code !=0 + messaggio di descrizione
# 3. data update (controllata dal plugin di nagios)
# NOTE: il plugin di nagios deve anche controllare che l'url sia raggiungibile


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

    

def runBackEnd():
    # --------------------------------------------------------------------------------
    # --- read the cache
    allCachedRuns = pclMonitoringTools.readCache(cacheFileName)
    cachedRuns = allCachedRuns[0]
    runReports = allCachedRuns[1]

    unknownRun = False # this is set to true only if one run can not be processed
    unknownRunMsg = ''
    # --------------------------------------------------------------------------------
    # --- get the last cached run
    if len(cachedRuns) != 0:
        cachedRuns.sort()
    else:
        cachedRuns.append(firstRunToMonitor)

    retValues = 0, 'OK'

    # get the list of runs to be refreshed (< 24h old)
    runsToBeRefreshed = []
    reportsToBeRefreshed = []
    last2days = datetime.timedelta(days=2)
    twdaysago = datetime.datetime.today() - last2days
    for rep in runReports:

        if rep.startTime() >= twdaysago:
            runsToBeRefreshed.append(rep.runNumber())
            reportsToBeRefreshed.append(rep)
            #print rep.runNumber()
            #print "start: " + str(rep.startTime()) + " less than " + str(twdaysago)

    #remove the list of reports and runs to be refreshed from the cahced ones
    for rep in reportsToBeRefreshed:
        cachedRuns.remove(rep.runNumber())
        runReports.remove(rep)

        
    lastCachedRun = firstRunToMonitor
    if(len(cachedRuns) != 0):
        lastCachedRun = cachedRuns[len(cachedRuns)-1]
    runsToBeRefreshed.sort(reverse=True)
    print "last cached run #: " + str(lastCachedRun)
    print "runs to be refreshed: " + str(runsToBeRefreshed)


    
    # --------------------------------------------------------------------------------
    # --- get the list of collision runs from RR (only for the runs not yet cached)
    runList = []
    try:
        #runList = RunRegistryTools.getRunList(lastCachedRun+1)
        #runList2 = RunRegistryTools.getRunListRR3(lastCachedRun+1, "Express", "Collisions12")
        runList = RunRegistryTools.getRunListRR3(lastCachedRun+1, rrDatasetName, rrRunClassName)
        #print runList
        #print runList2
        runList.sort(reverse=True)
    except Exception as error:
        print '*** Error 1: RR query has failed'
        print error
        return 101, "Error: failed to get collision runs from RunRegistry: " + str(error)

    print "run list from RR: " + str(runList)
    if len(runList) < len(runsToBeRefreshed):
        print "Warning: list from RR is fishy...using the previous one!"
        retValues = 1, 'Warning: list from RR is fishy...using the previous one!'
        runList = runsToBeRefreshed

    # --- get the prompt reco status from Tier0-DAS
    tier0Das = tier0DasInterface.Tier0DasInterface(tier0DasSrc) 
    lastPromptRecoRun = lastCachedRun
    try:
        lastPromptRecoRun = tier0Das.lastPromptRun()
        print "Tier0 DAS last run released for PROMPT:       ", lastPromptRecoRun
        #print "Tier0 DAS first run safe for condition update:", tier0Das.firstConditionSafeRun()
    except Exception as error:
        print '*** Error 2: Tier0-DAS query has failed'
        print error
        return 102, "Error: Tier0-DAS query has failed: " + str(error)

    # --------------------------------------------------------------------------------
    # list the IOVs in oracle
    # FIXME: get the tag name directly from the GT through the Tier0-DAS interface for the prompt_cfg
    # runbased tag
    listiov_run_oracle = listIov(connectOracle, tagRunOracle, passwdfile)
    if listiov_run_oracle[0] == 0:
        iovtableByRun_oracle = IOVTable()
        iovtableByRun_oracle.setFromListIOV(listiov_run_oracle[1])
        #iovtableByRun_oracle.printList()

    # iovbased tag
    listiov_lumi_oracle = listIov(connectOracle, tagLumiOracle, passwdfile)
    if listiov_lumi_oracle[0] == 0:
        iovtableByLumi_oracle = IOVTable()
        iovtableByLumi_oracle.setFromListIOV(listiov_lumi_oracle[1])

    # --------------------------------------------------------------------------------
    # find the file produced by PCL in the afs area
    fileList = os.listdir(promptCalibDir)
    

    # --------------------------------------------------------------------------------
    # run on runs not yet cached
    isFirst = True
    lastDate = datetime.datetime
    isLastProcessed = True
    for run in runList:
        #print run
        if run == 167551:
            continue #FIXME: implement a workaround to the fact that the run-info payload is not there
        # get the run report
        rRep = None
        try:
            rRep = pclMonitoringTools.getRunReport(runinfoTag, run, promptCalibDir, fileList,
                                                   iovtableByRun_oracle, iovtableByLumi_oracle)
        except pclMonitoringTools.OngoingRunExcept as error:
            print error
        except Exception as error:
            unknownRun = True
            unknownRunMsg = "Error: can not get report for run: " + str(run) + ", reason: " + str(error)
            print unknownRunMsg
        else:

            if rRep._pclRun:
                # check this is not older than the one for the following run
                if isFirst or rRep.jobTime() < lastDate:
                    rRep.isOutoforder(False)
                    if rRep._pclRun:
                        isFirst = False
                        lastDate = rRep.jobTime()
                else:
                    print "   " + warning("Warning: ") + " this comes after the following run!!!"
                    rRep.isOutoforder(True)

            runReports.append(rRep)

            if not isLastProcessed:
                if not rRep._pclRun:
                    retValues =  1001, "PCL not run for run: " + str(rRep._runnumber)
                elif not rRep._hasPayload:
                    retValues =  1002, "PCL produced no paylaod for run: " + str(rRep._runnumber)
                elif rRep._isOutOfOrder and not rRep._hasUpload:
                    retValues =  1003, "PCL run out of order for run: " + str(rRep._runnumber)
                elif not rRep._hasUpload:
                    retValues = 1004, "Upload to DB failed for run: " + str(rRep._runnumber)
            if rRep._pclRun:
                isLastProcessed = False
                
    runReports.sort(key=lambda rr: rr._runnumber)


    # -----------------------------------------------------------------
    # ---- cache the results for runs older than 48h and write the log for the web
    pclMonitoringTools.writeCacheAndLog(cacheFileName, webArea + "log.txt", runReports)
    status = retValues[0]
    message = retValues[1]
    if status == 0 and unknownRun:
        status = 10
        message = unknownRunMsg
    return status, message

import Tools.MyCondTools.monitorStatus as monitorStatus


if __name__ == "__main__":

    # TODO:
    # 5. aggiuni check sulla latency
    # 6. come fai a catchare problemi nel frontend?

    # start here
    status = monitorStatus.MonitorStatus(taskName)
    status.setWebUrl(weburl)
    statAndMsg = None
    #try:
    statAndMsg = runBackEnd()
    #except:
    #    print "*** Error running back-end call"
    #    statAndMsg = 1000, "unknown error"
    
    status.setStatus(statAndMsg[0],statAndMsg[1])
    #print datetime.datetime.today()
    status.setUpdateTime(datetime.datetime.today())
    status.writeJsonFile(webArea + "status.json")

    sys.exit(0)

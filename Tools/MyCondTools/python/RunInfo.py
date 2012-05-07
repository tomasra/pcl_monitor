import datetime

import os,sys, DLFCN
sys.setdlopenflags(DLFCN.RTLD_GLOBAL+DLFCN.RTLD_LAZY)

#from pluginCondDBPyInterface import *
import pluginCondDBPyInterface as condDB

# FIXME: this should go to cfg
dbName =  "oracle://cms_orcon_adg/CMS_COND_31X_RUN_INFO"
logName = "oracle://cms_orcon_adg/CMS_COND_31X_POPCONLOG"

fwkInc = condDB.FWIncantation()
rdbms = condDB.RDBMS("/afs/cern.ch/cms/DB/conddb/ADG")
rdbms.setLogger(logName)

from CondCore.Utilities import iovInspector as inspect

db = rdbms.getDB(dbName)

#tags = db.allTags()


def getDate(string):
    date = string.split()[0].split('-')
    time = string.split()[1].split(':')
    datet = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]),int(float(time[2])))
    return datet

class RunInfoContent:
    def __init__(self, summary):
        listofEntries = summary.split(',')
        #print listofEntries
        self._run = listofEntries[0].lstrip('RUN:').lstrip()
        #print self._run
        if int(self._run) == -1:
            raise ValueError("[RunInfoContent::Init] Error: run number in RunInfo is: " + str(self._run))
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
        #print string
        if string != 'null':
            date = string.split('T')[0].split('-')
            time = string.split('T')[1].split(':')
            datet = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]),int(float(time[2])))
            return datet
        else :
            print "string for date is:",string
            return None 


def getRunInfoStartAndStopTime(runinfoTag, runinfoaccount, run):
    try :
        db.startTransaction()
        log = db.lastLogEntry(runinfoTag)
        # for printing all log info present into log db 
        #print log.getState()

        # for inspecting all payloads/runs
        iov = inspect.Iov(db,runinfoTag, run,run)
        db.commitTransaction()
    except RuntimeError as error :
        print error("*** Error") + " no iov? in RunInfo tag ", runinfoTag
        raise RuntimeError('No IOV for run: ' + str(run) + ' in RunInfo tag: ' + runinfoTag)
    except Exception:
        raise 
    else:
        # --- read the information for the run from runinfo
        for x in  iov.summaries():
            #print x
            runInfo = RunInfoContent(x[3])
            #print x[3]
            # run lenght
            return runInfo

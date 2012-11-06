import datetime

import os,sys, DLFCN
sys.setdlopenflags(DLFCN.RTLD_GLOBAL+DLFCN.RTLD_LAZY)

#from pluginCondDBPyInterface import *
import pluginCondDBPyInterface as condDB

# FIXME: this should go to cfg
dbName =  "oracle://cms_orcon_adg/CMS_COND_31X_RUN_INFO"
#dbName =  "frontier://PromptProd/CMS_COND_31X_RUN_INFO"
logName = "oracle://cms_orcon_adg/CMS_COND_31X_POPCONLOG"

fwkInc = condDB.FWIncantation()
rdbms = condDB.RDBMS("/afs/cern.ch/cms/DB/conddb/ADG")
rdbms.setLogger(logName)

from CondCore.Utilities import iovInspector as inspect

db = rdbms.getDB(dbName)

#tags = db.allTags()



"""
Module providing tools to query the RunInfo tags in the condition DB

$Date: 2012/09/20 14:33:33 $
$Revision: 1.7 $

"""






def getDate(string):
    """
    Convert a string into a datetime object
    """
    if not 'null' in string:
        date = string.split()[0].split('-')
        time = string.split()[1].split(':')
        datet = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]),int(float(time[2])))
        return datet
    else:
        return None

class RunInfoContent:
    """
    This object stores the result of a query to RunInfo for a given run.
    """
    
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
        """
        Returns a datetime object for the start time of the run
        """
        return self.getDate(self._startTime)+self._fromUTCToLocal

    def stopTime(self):
        """
        Returns a datetime object for the stop time of the run
        """
        if self._stopTime != 'null':
            return self.getDate(self._stopTime)+self._fromUTCToLocal
        else:
            return 'null null'

            
    def run(self):
        """
        Run number
        """
        return self._run

    def getDate(self, string):
        """
        String to datetime conversion
        """
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
    """
    Builds a RunInfoContent for a given run. Input parameters are the RunInfo tag name, connection string and run #
    """


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


if __name__ == "__main__":
    print getRunInfoStartAndStopTime("runinfo_31X_hlt", '', 206448)





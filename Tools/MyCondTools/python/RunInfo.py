import datetime

import InspectTag



"""
Module providing tools to query the RunInfo tags in the condition DB

$Date: 2012/11/06 09:51:29 $
$Revision: 1.8 $

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
        Returns a datetime object for the stop time of the run. In case of runs still ongoing it returns 'null null'
        """
        if self._stopTime != 'null':
            return self.getDate(self._stopTime)+self._fromUTCToLocal
        else:
            # FIXME: should handle with exception...
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
            return datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%S.%f")
        else :
            print "string for date is:",string
            return None 


def getRunInfoStartAndStopTime(runInfoTag, runinfoaccount, run, logName = 'oracle://cms_orcon_adg/CMS_COND_31X_POPCONLOG', passwdFile = '/afs/cern.ch/cms/DB/conddb/ADG'):
    """
    Builds a RunInfoContent for a given run. Input parameters are the RunInfo tag name, connection string and run #
    """
    
    try:
        summaries = InspectTag.getSummaries(runInfoTag, runinfoaccount, run, run, logName, passwdFile)
        for x in  summaries:
            #print x
            runInfo = RunInfoContent(x[3])
            #print x[3]
            # run lenght
            return runInfo

    except Exception:
        raise 


if __name__ == "__main__":
    print getRunInfoStartAndStopTime("runinfo_31X_hlt", "oracle://cms_orcon_adg/CMS_COND_31X_RUN_INFO", 206448)





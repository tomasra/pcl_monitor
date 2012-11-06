import datetime
import os
import Tools.MyCondTools.RunInfo as RunInfo
import Tools.MyCondTools.tableWriter as tableWriter
import Tools.MyCondTools.color_tools as colorTools
import Tools.MyCondTools.gt_tools as gtTools


# fixme find a method to configure which records/tafs need to be monitored
tagLumi                = "BeamSpotObject_ByLumi"
tagRun                 = "BeamSpotObject_ByRun"


class RunReport:
    def __init__(self):
        self._runnumber = -1
        self._pclRun = True
        self._hasPayload = True
        self._hasUpload = True
        self._isOutOfOrder = False
        self._startTime = None
        self._stopTime = None
        #self._runInfo = None
        self._latencyFromEnd = -1.
        self._latencyFromBeginning = -1.
        self._jobTime = datetime.datetime
        return

    def runNumber(self):
        return self._runnumber

    def startTime(self):
        return self._startTime

    def stopTime(self):
        return self._stopTime

    def setRunNumber(self, number):
        self._runnumber = number

    def sqliteFound(self, isFound):
        self._pclRun = isFound

    def payloadFound(self, isFound):
        self._hasPayload = isFound

    def isUploaded(self, isUploaded):
        self._hasUpload = isUploaded

    def isOutoforder(self, isOutofOrder):
        self._isOutOfOrder = isOutofOrder

    def setRunInfoContent(self, runInfo):
        self._startTime = runInfo.startTime()
        self._stopTime = runInfo.stopTime()
        #self._runInfo = runInfo

    def setStartTime(self, start):
        self._startTime = start

    def setStopTime(self, stop):
        self._stopTime = stop

    # hours
    def runLenght(self):
        deltaTRun = self.stopTime() - self.startTime()
        return deltaTRun.days*24. + deltaTRun.seconds/(60.*60.)

    def setLatencyFromEnd(self, timeFromEnd):
        self._latencyFromEnd = timeFromEnd

    def setLatencyFromBeginning(self, timeFromBeginning):
        self._latencyFromBeginning = timeFromBeginning
        

    def __str__(self):
        return "--- run #: " + str(self._runnumber) + " start time: " + str(self.startTime())

    def getList(self):
        theList = [str(self._runnumber), str(self.startTime()), str(self.stopTime()), self._pclRun,  self._hasPayload, self._hasUpload, self._isOutOfOrder, float(self._latencyFromBeginning), float(self._latencyFromEnd)]
        return theList

    def setJobTime(self, time):
        self._jobTime = time

    def jobTime(self):
        return self._jobTime





def readCache(filename):
    # read the cache file and returns the list of the RunReports for all the cached files
    runReports = []
    runNumbers = []
    if os.path.exists(filename):
        print "reading cache file: " + filename
        cache = file(filename,"r")
        data = cache.readlines()
        for line in data:
            if line[0] != '#' and line != "":
                # read the relevant lines
                items = line.split()
                # get the  run #
                runCached = int(items[0])
                runNumbers.append(runCached)
                # create the report
                runReport = RunReport()
                runReport.setRunNumber(runCached)

                if items[5] == "True":
                    runReport.sqliteFound(True)
                else:
                    runReport.sqliteFound(False)

                if items[6] == "True":
                    runReport.payloadFound(True)
                else:
                    runReport.payloadFound(False)

                if items[7] == "True":
                    runReport.isUploaded(True)
                else:
                    runReport.isUploaded(False)

                if items[8] == "True":
                    runReport.isOutoforder(True)
                else:
                    runReport.isOutoforder(False)
                    oooCached = True


                startCached = RunInfo.getDate(items[1] + " " + items[2])
                runReport.setStartTime(startCached)
                
                stopCached = RunInfo.getDate(items[3] + " " + items[4])
                runReport.setStopTime(stopCached)
                
                latencyStartCached = float(items[9])
                latencyEndCached = float(items[10])

                runReport.setLatencyFromBeginning(latencyStartCached)
                runReport.setLatencyFromEnd(latencyEndCached)

                runReports.append(runReport)
        cache.close()                

    return runNumbers, runReports

def writeCacheAndLog(cachefilename, logfilename, runReports):
    last2days = datetime.timedelta(days=2)
    tableForCache =[]
    tableForCache.append(["# run", "start-time", "end-time", "PCL Run", "payload","upload","Tier0 OOO", "latency from start", "latency from end"])

    tableForLog =[]
    tableForLog.append(["# run", "start-time", "end-time", "PCL Run", "payload","upload","Tier0 OOO", "latency from start", "latency from end"])

    #print str(len(runReports))
    for rep in runReports:

        # cache only runs older than 48h
        #twdaysago = datetime.datetime.today() - last2days
        #if rep.startTime() < twdaysago:
        #    #print "start: " + str(rep.startTime()) + " older than " + str(twdaysago)
        #    tableForCache.append(rep.getList())            
        # FIXME: cache everything and refresh only runs younger than 48h
        tableForCache.append(rep.getList())
        tableForLog.append(rep.getList()) 

        
    #out = sys.stdout
    cacheFile = file(cachefilename,"w")
    tableWriter.pprint_table(cacheFile, tableForCache)
    cacheFile.close()

    #out = sys.stdout
    logFile = file(logfilename,"w")
    tableWriter.pprint_table(logFile, tableForLog)
    logFile.close()


def getFileTimeHash(filename):
    hashTime = ''
    if 'ALCAPROMPTHarvest' in filename:
        # this is the ProdA file-name
        hashTime = filename.split('-')[4]
    else:
        # this is the WMA file-name
        hashTime = filename.split('@')[2]
    return hashTime


class OngoingRunExcept(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def getRunReport(runinfoTag, run, promptCalibDir, fileList, iovtableByRun_oracle, iovtableByLumi_oracle):

    #print run
    # input: runInfoTag, run, fileList, iovlist
    runInfo = None
    try:
        runInfo = RunInfo.getRunInfoStartAndStopTime(runinfoTag, '', run)
    except Exception as error:
        print "*** Error can not find run: " + str(run) + " in RunInfo: " + str(error)
        raise Exception("Error can not find run: " + str(run) + " in RunInfo: " + str(error))

    if int(run) != int(runInfo.run()):
        # try to get the payload from runinfo_start: this run might still be ongoing
        # FIXME: need to get this from cfg
        runinfoStartTag = "runinfo_start_31X_hlt"
        try:
            runInfo = RunInfo.getRunInfoStartAndStopTime(runinfoStartTag, '', run)
            if int(run) != int(runInfo.run()):
                raise Exception("Error mismatch with the runInfo payload for run: " + str(run) + " in RunInfo: " + str(runInfo.run()))
        except Exception as error:
            print "*** Error can not find run: " + str(run) + " in RunInfo (start): " + str(error)
            raise Exception("Error can not find run: " + str(run) + " in RunInfo (start): " + str(error))
        
        

    #print run
    #print runInfo.run()
    rRep = RunReport()
    rRep.setRunNumber(runInfo.run())
    rRep.setRunInfoContent(runInfo)

    if(type(runInfo.stopTime()) == datetime.datetime):
        print runInfo.stopTime()
        #raise OngoingRunExcept('Run ' + str(runInfo.run()) + " is still onging!")
        deltaTRun = runInfo.stopTime() - runInfo.startTime()
        deltaTRunH = deltaTRun.days*24. + deltaTRun.seconds/(60.*60.)

        print "-- run #: " + colorTools.blue(runInfo.run())            
        print "   start: " + str(runInfo.startTime()) + " stop: " + str(runInfo.stopTime()) + " lenght (h): " + str(deltaTRunH)
    else:
        print "-- run #: " + colorTools.blue(runInfo.run())            
        print "   start: " + str(runInfo.startTime()) + " is ongoing according to RunInfo" 


    # --- status flags for this run
    isFileFound = False
    emptyPayload = True
    isOutOfOrder = False
    allLumiIOVFound = False


    # --- look for the file on AFS
    fileName = ""
    fileForRun = []
    hashTimes = []
    # find the files associated to this run:
    for dbFile in fileList:
        if '.db' in dbFile:
            if str(run) in dbFile:
                hashTime = getFileTimeHash(dbFile)
                if not hashTime in hashTimes:
                    hashTimes.append(hashTime)
                    fileForRun.append(dbFile)

    if len(fileForRun) == 0:
        print "   " + colorTools.warning("***Warning") + ": no sqlite file found!"
        isFileFound = False

    elif len(fileForRun) > 1:
        print "   " + colorTools.warning("***Warning") + ": more than one file for this run!"
        for dbFile in fileForRun:
            modifDate = datetime.datetime.fromtimestamp(os.path.getmtime(promptCalibDir + dbFile))
            accessDate = datetime.datetime.fromtimestamp(os.path.getatime(promptCalibDir + dbFile))
            changeDate = datetime.datetime.fromtimestamp(os.path.getctime(promptCalibDir + dbFile))
            print '       ',dbFile,'time-stamp (modification):',modifDate
            print '       ',dbFile,'time-stamp (access):',accessDate
            print '       ',dbFile,'time-stamp (change):',changeDate

    for dbFile in fileForRun:
        isFileFound = True
        if isFileFound and not emptyPayload and isFileFound:
            # in this case the file was already identified
            continue
        print "   file: " + dbFile
        modifDate = datetime.datetime.fromtimestamp(os.path.getmtime(promptCalibDir + dbFile))
        rRep.setJobTime(modifDate)

        #         # check this is not older than the one for the following run
        #         if isFirst or modifDate < lastDate:
        #             lastDate = modifDate
        #             isFirst = False
        #             isOutOfOrder = False

        #         else:
        #             print "   " + warning("Warning: ") + " this comes after the following run!!!"
        #             isOutOfOrder = True


        # delta-time from begin of run
        deltaTFromBegin = modifDate - runInfo.startTime()
        deltaTFromBeginH = deltaTFromBegin.days*24. + deltaTFromBegin.seconds/(60.*60.)

        # delta-time from end of run
        deltaTFromEndH = 0.01
        if(modifDate > runInfo.stopTime()): 
            deltaTFromEnd = modifDate - runInfo.stopTime()
            deltaTFromEndH = deltaTFromEnd.days*24. + deltaTFromEnd.seconds/(60.*60.)

        print "   file time: " + str(modifDate) + " Delta_T begin (h): " + str(deltaTFromBeginH) + " Delta_T end (h): " + str(deltaTFromEndH)

        rRep.setLatencyFromBeginning(deltaTFromBeginH)
        rRep.setLatencyFromEnd(deltaTFromEndH)

        # check the file size
        fileSize = os.path.getsize(promptCalibDir + dbFile)
        if fileSize == 1 or fileSize == 32768:
            emptyPayload = True
            print "   " + colorTools.warning("***Warning") + ": no payload in sqlite file!"
        else:
            
            emptyPayload = False

            
            # list the iov in the tag
            connect    = "sqlite_file:" + promptCalibDir + dbFile
            listiov_run_sqlite = gtTools.listIov(connect, tagRun, '')
            if listiov_run_sqlite[0] == 0:
                iovtableByRun_sqlite = gtTools.IOVTable()
                iovtableByRun_sqlite.setFromListIOV(listiov_run_sqlite[1])
                #iovtableByRun_sqlite.printList()
                for iov in iovtableByRun_sqlite._iovList:
                    iovOracle = gtTools.IOVEntry()
                    if iovtableByRun_oracle.search(iov.since(), iovOracle):
                        print "    runbased IOV found in Oracle!"
                        #print iovOracle
                    else:
                        print "    " + colorTools.warning("Warning:") + " runbased IOV not found in Oracle"
            else:
                print colorTools.warning("Warning") +  " can not list IOV for file",connect
                #raise Exception("Error can not list IOV for file",connect)
              

            missingIOV = False
            listiov_lumi_sqlite = gtTools.listIov(connect, tagLumi, '')
            if listiov_lumi_sqlite[0] == 0:
                iovtableByLumi_sqlite = gtTools.IOVTable()
                iovtableByLumi_sqlite.setFromListIOV(listiov_lumi_sqlite[1])
                #iovtableByLumi_sqlite.printList()
                counterbla = 0
                for iov in iovtableByLumi_sqlite._iovList:
                    iovOracle = gtTools.IOVEntry()
                    if not iovtableByLumi_oracle.search(iov.since(), iovOracle):
                        #print "    Lumi based IOV found in Oracle:"
                        #print iovOracle
                        counterbla += 1
                        print "    " + colorTools.warning("Warning:") + " lumibased IOV not found in Oracle for since: " + str(iov.since())
                        missingIOV = True
            else:
                emptyPayload = True
                print "   " + colorTools.warning("***Warning") + ": no payload in sqlite file!"
                print colorTools.warning("Warning") +  " can not list IOV for file",connect
                #raise Exception("Error can not list IOV for file",connect)
                

        if not emptyPayload:
            if not missingIOV:
                allLumiIOVFound = True
                print "    All lumibased IOVs found in oracle!"
            else:
                allLumiIOVFound = False
                print "    " + colorTools.warning("Warning:") + " not all lumibased IOVs found in Oracle!!!"




    # fill the run-report for this run
    if not isFileFound:
        rRep.sqliteFound(False)
    else:
        rRep.sqliteFound(True)
        if isOutOfOrder:
            rRep.isOutoforder(True)
        else:
            rRep.isOutoforder(False)

        if emptyPayload:
            rRep.payloadFound(False)
        else:
            rRep.payloadFound(True)

        if not allLumiIOVFound:
            rRep.isUploaded(False)
        else:
            rRep.isUploaded(True)

    return rRep


import datetime
import os
import json
import ast
import Tools.MyCondTools.RunInfo as RunInfo
import Tools.MyCondTools.tableWriter as tableWriter
import Tools.MyCondTools.color_tools as colorTools
import Tools.MyCondTools.gt_tools as gtTools
import Tools.MyCondTools.monitoring_config as config




class PCLDBFile:
    """
    Class representing an sqlite file created by Tier0 PCL machinery.
    """
    def __init__ (self, filename, isPA = False):
        self.fileName = filename
        # creation time = modification = access = change time on AFS
        self.creationTime = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        # time of upload in the DropBox
        self.uploadTime = None
        self.uploadFileName = None
        self.metaDataFileName = None
        # for ProdAgent the creation and the uplaod are simulteneous
        # while for WMA a .txt.uploaded file is created at upload time
        # by the upload deamon
        if isPA:
            self.uploadTime = self.creationTime
        else:
            self.uploadFileName = filename.split('.db')[0] + ".txt.uploaded"
            self.metaDataFileName = filename.split('.db')[0] + ".txt"
            if os.path.exists(self.uploadFileName):
                self.uploadTime = datetime.datetime.fromtimestamp(os.path.getmtime(self.uploadFileName))
        return

    def isUploaded(self):
        """ Returns True if the file has been sent (or tried to send) to the DB Drop-Box """
        # file is uploaded only if the upload time was set
        if self.uploadTime != None:
            return True
        return False



class RunReport:
    """ This class represents the statemachine of the PCL for each run """
    def __init__(self, runNumber):
        self.runNumber = runNumber

        # run start and stop time (from run-info)
        self.startTime = None
        self.stopTime = None

        # ---- list of states for each run
        # - this is set to true if at least 1 sqlite is found
        self.pclRun = False
        # - this is set if there is more than 1 db file for this run
        self.multipleFiles = False
        # - this is set to true if the file actually contains a payload
        self.hasPayload = False
        # - this is set to true if the .txt.upload file is found in AFS
        # note that the upload might have failed but at least it was attempted
        self.hasUpload = False
        # - this is set to true if the payloads are found in the target tag in ORACLE
        self.uploadSucceeded = False
        # - this is set to true if the UPLOAD of different runs happened OutOf ORder
        self.isOutOfOrder = False

        #self._runInfo = None

        # latencies in hours
        self.latencyUploadFromEnd = -1.
        self.latencyUploadFromStart = -1.
        self.latencyJobFromEnd = -1
        self.jobTime = datetime.datetime

        self.fileList = []

        return


    def addFile(self, file):
        """
        Add a file for this run. while adding check also some of the possible states
        """
        # append the file
        self.fileList.append(file)

        if len(self.fileList) > 1:
            self.multipleFiles = True

        # swtich the PCLRun flag on
        self.pclRun = True

        if file.uploadTime != None:
            self.hasUpload = True

        self.fileList.sort(key = lambda ff: ff.creationTime)
        
    def stopTimeAge(self):
        """ time passed from the stop of the run until NOW (in hours) """
        ageStop = datetime.datetime.today() - self.stopTime
        return ageStop.days*24. + ageStop.seconds/(60.*60.)


    def setRunInfoContent(self, runInfo):
        self.startTime = runInfo.startTime()
        self.stopTime = runInfo.stopTime()
        #self._runInfo = runInfo

    # hours
    def runLenght(self):
        """ Run lenght in hours """
        deltaTRun = self.stopTime - self.startTime
        return deltaTRun.days*24. + deltaTRun.seconds/(60.*60.)
        

    def __str__(self):
        return "--- run #: " + str(self.runNumber) + " start time: " + str(self.startTime)

    def getList(self):
        theList = [str(self.runNumber),\
                   str(self.startTime),\
                   str(self.stopTime),\
                   self.pclRun,\
                   self.multipleFiles,\
                   self.hasPayload,\
                   self.hasUpload,\
                   self.uploadSucceeded,\
                   self.isOutOfOrder,\
                   float(self.latencyJobFromEnd),\
                   float(self.latencyUploadFromStart),\
                   float(self.latencyUploadFromEnd)]
        return theList

    def setJobTime(self, time):
        self.jobTime = time
        deltaTfromEnd = time - self.stopTime
        self.latencyJobFromEnd = deltaTfromEnd.days*24. + deltaTfromEnd.seconds/(60.*60.)
    
    def setUploadTime(self, time):
        self.uploadTime = time
        # compute latency from end of run
        deltaTfromEnd = time - self.stopTime
        self.latencyUploadFromEnd = deltaTfromEnd.days*24. + deltaTfromEnd.seconds/(60.*60.)
        # compute latency from start of run
        deltaTfromStart = time - self.startTime
        self.latencyUploadFromStart = deltaTfromStart.days*24. + deltaTfromStart.seconds/(60.*60.)
        





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
                # print line
                items = line.split()
                # get the  run #
                runCached = int(items[0])
                runNumbers.append(runCached)
                # create the report
                runReport = RunReport(runCached)
                #runReport.setRunNumber(runCached)

                runReport.startTime = RunInfo.getDate(items[1] + " " + items[2])
                runReport.stopTime  = RunInfo.getDate(items[3] + " " + items[4])


                runReport.pclRun        = ast.literal_eval(items[5])
                runReport.multipleFiles = ast.literal_eval(items[6])
                
                runReport.hasPayload      = ast.literal_eval(items[7])
                runReport.hasUpload       = ast.literal_eval(items[8])
                runReport.uploadSucceeded = ast.literal_eval(items[9])
                runReport.isOutofOrder    = ast.literal_eval(items[10])

                    
                latencyJobFromEnd = float(items[11])
                latencyStartCached = float(items[12])
                latencyEndCached = float(items[13])

                runReport.latencyJobFromEnd      = latencyJobFromEnd
                runReport.latencyUploadFromStart = latencyStartCached
                runReport.latencyUploadFromEnd   = latencyEndCached

                runReports.append(runReport)
        cache.close()                

    return runNumbers, runReports

def writeCacheAndLog(cachefilename, logfilename, runReports):
    tableHeaders = ["# run", "start-time", "end-time", "PCL Run", "mult. files", "payload","upload","upload OK", "Tier0 OOO", "latency job", "lat. upload (f start)", "lat. upload (f end)"]
    

    last2days = datetime.timedelta(days=2)
    tableForCache =[]
    tableForCache.append(tableHeaders)

    tableForLog =[]
    tableForLog.append(tableHeaders)

    #print str(len(runReports))
    for rep in runReports:
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


def getDropBoxMetadata(dbFile):
    jsonData = open(dbFile.uploadFileName)
    metadataMap = json.load(jsonData)
    jsonData.close()
    return metadataMap

    
    


def getRunReport(pclTag, run, fileList, oracleTables, lastUploadDate):



    #print run
    # input: runInfoTag, run, fileList, iovlist
    runInfo = None
    try:
        runInfo = RunInfo.getRunInfoStartAndStopTime(config.runInfoTag_stop, config.runInfoConnect, run)
    except Exception as error:
        print "*** Error can not find run: " + str(run) + " in RunInfo: " + str(error)
        raise Exception("Error can not find run: " + str(run) + " in RunInfo: " + str(error))

    if int(run) != int(runInfo.run()):
        # try to get the payload from runinfo_start: this run might still be ongoing
        try:
            runInfo = RunInfo.getRunInfoStartAndStopTime(config.runInfoTag_start, config.runInfoConnect, run)
            if int(run) != int(runInfo.run()):
                raise Exception("Error mismatch with the runInfo payload for run: " + str(run) + " in RunInfo: " + str(runInfo.run()))
        except Exception as error:
            print "*** Error can not find run: " + str(run) + " in RunInfo (start): " + str(error)
            raise Exception("Error can not find run: " + str(run) + " in RunInfo (start): " + str(error))
        

    # -------------------------------------------------------------------
    # 0 --- print the timing information about this run
    if(type(runInfo.stopTime()) == datetime.datetime):
        deltaTRun = runInfo.stopTime() - runInfo.startTime()
        deltaTRunH = deltaTRun.days*24. + deltaTRun.seconds/(60.*60.)

        print "-- run #: " + colorTools.blue(runInfo.run())            
        print "   start: " + str(runInfo.startTime()) + " stop: " + str(runInfo.stopTime()) + " lenght (h): " + str(deltaTRunH)
    else:
        print "-- run #: " + colorTools.blue(runInfo.run())            
        print "   start: " + str(runInfo.startTime()) + " is ongoing according to RunInfo" 
    
        


        
    # print '   -- Creating runReport for tag: ' + colorTools.blue(pclTag)
    rRep = RunReport(runInfo.run())

    # set the info about the run from RunInfo
    rRep.setRunInfoContent(runInfo)

    # -------------------------------------------------------------------
    # 1 --- look for the file on AFS
    for dbFile in fileList:
        if '.db' in dbFile:
            if str(run) in dbFile:
                if pclTag in dbFile:
                    rRep.addFile(PCLDBFile(config.promptCalibDir + dbFile, False))


    if not rRep.pclRun:
        print "   " + colorTools.warning("***Warning") + ": no sqlite file found!"

    elif rRep.multipleFiles:
        print "   " + colorTools.warning("***Warning") + ": more than one file for this run!"
        # print timestamps of all files
        for dbFile in rRep.fileList:
            print '       ',dbFile.fileName ,'time-stamp (creation):',dbFile.creationTime,' (upload)',dbFile.uploadTime

    # pick the most meaningful file (the first one? and run checks
    for dbFile in rRep.fileList:
        print "     file: " + dbFile.fileName



        # -------------------------------------------------------------------
        # 2 --- Check for empty payloads (if the case exit)
        # list IOV
        # - if empty -> setEmpty Payload and continue
        # - if full quit check for uplaod in oracle and quit the loop
        connect    = "sqlite_file:" + dbFile.fileName
        listiov_sqlite = gtTools.listIov(connect, pclTag, '')

        rRep.setJobTime(dbFile.creationTime)
        

        if listiov_sqlite[0] != 0:
            # the payload was not found in the sqlite -> look for the next file
            print colorTools.warning("Warning") +  " can not list IOV for this file -> no payload"
            continue

        # FIXME: use pywrappers
        iovtable_sqlite = gtTools.IOVTable()
        iovtable_sqlite.setFromListIOV(listiov_sqlite[1])
        rRep.hasPayload = True
        print "     sqlite contains a payload!"


        # -------------------------------------------------------------------
        # 3 --- check if upload was tried (if not exit)
        if not dbFile.isUploaded():
            print colorTools.warning("      Warning") +  " upload not yet tried!",connect
            continue
        rRep.hasUpload = True
        rRep.setUploadTime(dbFile.uploadTime)

        # -------------------------------------------------------------------
        # 4 --- check for out-of-order upload
        if not lastUploadDate == None:
            # make sure this is not the first run to be checked...
            # FIXME: check
            if lastUploadDate <  dbFile.uploadTime:
                print "     " + warning("Warning: ") + " this comes after the following run!!!"
                rRep.isOutofOrder = True
        
        lastUploadDate = dbFile.uploadTime

        # -------------------------------------------------------------------
        # 5 --- check for the IOVs in ORACLE
        # get the target tag in oracle from the Drop-Box metadata
        metadatamap = getDropBoxMetadata(dbFile)
        #print metadatamap
        targetOracleTag = metadatamap['destinationTags'].keys()[0]
        targetOracleConnect = metadatamap['destinationDatabase']
        # check for online connection strings
        if 'oracle://cms_orcon_prod' in targetOracleConnect:
            targetOracleConnect = 'oracle://cms_orcon_adg/CMS_COND_'+metadatamap['destinationDatabase'].split('CMS_COND_')[1]

        print "     Target tag in Oracle:",targetOracleTag,'in account',targetOracleConnect


        # list IOV for the target tag (cache the list of IOV by pclTag: in case has not changed there is no need to re-run listIOv)
        iovtable_oracle = gtTools.IOVTable()
        if not targetOracleTag in oracleTables:
            # IOV for this tag in ORACLE has not yet been cached -> will now list IOV
            listiov_oracle = gtTools.listIov(targetOracleConnect, targetOracleTag, config.passwdfile)
            print "      listing IOV..."
            if listiov_oracle[0] == 0:
                iovtable_oracle.setFromListIOV(listiov_oracle[1])
                oracleTables[targetOracleTag] = iovtable_oracle
        else:
            # get the IOV from the cache dictionary
            print "      getting IOV list from cache..."
            iovtable_oracle = oracleTables[targetOracleTag]




        # check if the IOVs of the sqlite are found in oracle and flip the corresponding flag in rRep
        missingIOV = False
        for iov in iovtable_sqlite._iovList:
            iovOracle = gtTools.IOVEntry()
            if not iovtable_oracle.search(iov.since(), iovOracle):
                    print "    " + colorTools.warning("Warning:") + " lumibased IOV not found in Oracle for since: " + str(iov.since())
                    missingIOV = True

        if missingIOV:
            print "      " + colorTools.warning("Warning:") + " not all IOVs found in Oracle!!!"
        else:
            print "      All IOVs found in oracle: upload OK!"

        rRep.uploadSucceeded = not missingIOV



        # no need to check the following files
        break



    return rRep




class PclTagReport:
    def __init__(self, tagname):
        self._properties = {}
        self._properties['tagName'] = tagname
        self._properties['status'] = 0
        self._properties['statusMsg'] = 'OK'
        self._properties['runs'] = []
        
    def getProperty(self, key):
        return self._properties[key]

    def addRunStatus(self, run, status):
        self._properties['runs'].append(run)
        self._properties[run] = status
        # FIXME: is this the right way? The logic sits in the status value?
        if status[0] > self._properties['status']:
            self._properties['status'] = status[0]
            self._properties['statusMsg'] = status[1]
            

class PCLTagsJson:
    def __init__(self, name):
        self._name = name
        self._tagMap = {}

    def addTag(self, tagName, report):
        self._tagMap[tagName] = report._properties

        
    def writeJsonFile(self, dirName):
        filename =  self._name + ".json"
        # get a string with JSON encoding the list
        #dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        dump = json.dumps(self._tagMap)
        file = open(dirName + '/' + filename, 'w')
        file.write(dump + "\n")
        file.close()

    def readJsonFile(self, dirName):
        filename = self._name + ".json"
        jsonData = open(dirName + '/' + filename)
        self._tagMap = json.load(jsonData)
        jsonData.close()

    def getTagReport(self, tagName):
        tagRep = PclTagReport(tagName)
        tagRep._properties = self._tagMap[tagName]
        return tagRep

    def getTagNames(self):
        return self._tagMap.keys()


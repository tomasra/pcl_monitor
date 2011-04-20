#!/usr/bin/env python

import os,sys, DLFCN
sys.setdlopenflags(DLFCN.RTLD_GLOBAL+DLFCN.RTLD_LAZY)

from Tools.MyCondTools.gt_tools import *
from Tools.MyCondTools.color_tools import *
#from Tools.MyCondTools.Tier0LastRun import *
from Tools.MyCondTools.RunValues import *
from Tools.MyCondTools.tableWriter import *

import shutil

from pluginCondDBPyInterface import *

a = FWIncantation()

# --------------------------------------------------------------------------------
# configuratio
runinfoTag             = 'runinfo_31X_hlt'
tagLumi                = "BeamSpotObject_ByLumi"
tagRun                 = "BeamSpotObject_ByRun"
tier0DasSrc            = "https://cmsweb.cern.ch/tier0/runs"
passwd                 = "/afs/cern.ch/cms/DB/conddb"
connectOracle          =  "oracle://cms_orcoff_prod/CMS_COND_31X_BEAMSPOT"
tagRunOracle           = "BeamSpotObjects_PCL_byRun_v0_offline"
tagLumiOracle          = "BeamSpotObjects_PCL_byLumi_v0_prompt"
cacheFileName          = "cache_monitoring.txt"
writeToWeb             = False
nRunsToPlot            = 100

#os.putenv("CORAL_AUTH_PATH","/afs/cern.ch/cms/DB/conddb")
rdbms = RDBMS("/afs/cern.ch/cms/DB/conddb")
dbName =  "oracle://cms_orcoff_prod/CMS_COND_31X_RUN_INFO"
logName = "oracle://cms_orcoff_prod/CMS_COND_31X_POPCONLOG"

rdbms.setLogger(logName)
from CondCore.Utilities import iovInspector as inspect

db = rdbms.getDB(dbName)
tags = db.allTags()



#webArea = './'
# for inspecting last run after run has stopped  
#tag = 'runsummary_test'


from ROOT import *
from array import array

import datetime

import os,string,sys,commands,time
import xmlrpclib


class AlcaRecoDetails:
    def __init__(self, dataset, pd, epoch, version):
        self._datasetname = dataset
        self._epoch = epoch
        self._version = version
        self._pd = pd
        self._shortname = dataset.split('/')[2].split('-')[1]

    def dataset(self):
        return self._datasetname

    def epoch(self):
        return self._epoch

    def name(self):
        return self._shortname

class WebPageIndex:
    def __init__(self):
        self._epochs = []
        self._versions = []
        self._filenames = []

    def scan(self, dir):
        dirlist = os.listdir(dir)
        for fname in dirlist:
            if ".html" in fname and fname != 'index.html':
                self._filenames.append(fname)
                self._epochs.append(fname.split('-')[0])
                self._versions.append(fname.split('-')[1].split('.')[0])

    def buildPage(self):
        htmlpage = file('index.html',"w")
        htmlpage.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n')
        htmlpage.write('<html><head>\n')
        htmlpage.write('<link rel="stylesheet" type="text/css" href="./PromptCalibMonitoring.css">\n')
        htmlpage.write('<title>Monitoring of AlCaReco Production</title>\n')
        htmlpage.write('</head>\n')
        htmlpage.write('<body>\n')
        htmlpage.write('<center><h1>Monitoring of AlCaReco Production</h1></center>\n<hr>\n')
        htmlpage.write('<p>\n')
        htmlpage.write('<center><table width="40%"><tr><td><b>Data acquisition Era</b></td><td><b>Processing version<b></td><td><b>Link to plots</b></td></tr>\n')
        for index in range(0, len(self._filenames)):
            htmlpage.write('<tr><td>' + self._epochs[index] + '</td><td>' + self._versions[index] +
                           '</td><td><a href=./' + self._filenames[index] + '>plots</a></td></tr>\n')
        htmlpage.write('</table></center><hr>\n')
        htmlpage.write('<address>Gianluca Cerminara</address>\n')
        htmlpage.write('</body>\n')
        htmlpage.write('</html>\n')
        htmlpage.close()
        
class WebPageWriter:
    def __init__(self, name, epoch, version):
        self._fineName = name + ".html"
        self._title = "pippo"
        self._pds = []
        self._datasets = dict()
        self._epoch = epoch
        self._version = version
        self._title = "AlcaReco Monitoring for " + self._epoch + " " + self._version 

        
    def addDataset(self, pd, alcarecodetails):
        if not pd in self._datasets:
            self._pds.append(pd)
            self._datasets[pd] = []
        self._datasets[pd].append(alcarecodetails)
        return

    def buildPage(self):
        htmlpage = file(self._fineName,"w")
        htmlpage.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n')
        htmlpage.write('<html><head>\n')
        htmlpage.write('<link rel="stylesheet" type="text/css" href="./PromptCalibMonitoring.css">\n')
        htmlpage.write('<title>' + self._title + '</title>\n')
        htmlpage.write('</head>\n')
        htmlpage.write('<body>\n')
        htmlpage.write('<center><h1>' + self._title + '</h1></center>\n<hr>\n')
        htmlpage.write('<p>\n')
        for pd in self._pds:
            htmlpage.write('<b>' + pd + '</b>:\n')
            listofalcarecos = self._datasets[pd]
            for alcareco in listofalcarecos:
                anchor = "#" + pd +  alcareco.name()
                htmlpage.write(' <a href=' + anchor + '>' + alcareco.name() + '</a> \n')
            htmlpage.write('<br>\n')
        htmlpage.write('</p>\n')
        htmlpage.write('<p>The monitoring is based on DBS and is limited to runs defined as <i>Collision11</i> in Run Registry.</p>\n')

        for pd in self._pds: 
            htmlpage.write('<h3>' + pd + '</h3>\n')
            htmlpage.write('<table width="100%">\n')
            listofalcarecos = self._datasets[pd] 
            for alcareco in listofalcarecos:
                anchor = pd +  alcareco.name()
                effpng = pd + '-' + self._epoch + '-' + alcareco.name() + '-' + self._version + '-hEff.png'
                neventspng = pd + '-' + self._epoch + '-' + alcareco.name() + '-' + self._version + '-hNEvents.png'
                htmlpage.write('<tr><td><a name=' + anchor + '></a><b>' + alcareco.name() + '</b></td>\n')
                htmlpage.write('<td>' + alcareco.dataset() + '</td></tr>\n')
                htmlpage.write('<tr><td><h4>Number of events per run</h4></td>\n')
                htmlpage.write('<td><h4>Selection efficiency per run</h4></td></tr>\n')
                htmlpage.write('<tr><td><a href=./' + neventspng + '><img src="./' + neventspng + '" width="590"></a></td>\n')
                htmlpage.write('<td><a href=./' + effpng + '><img src="./' + effpng + '" width="590"></a></td></tr>\n')
            htmlpage.write('</table>\n')
            htmlpage.write('<hr>\n')

        htmlpage.write('<address>Gianluca Cerminara</address>\n')
        htmlpage.write('</body>\n')
        htmlpage.write('</html>\n')
        htmlpage.close()
                            
def getRunList(minRun):
    runlist = []
    
    FULLADDRESS="http://pccmsdqm04.cern.ch/runregistry/xmlrpc"
    #FULLADDRESS="http://pccmsdqm04.cern.ch/runregistry_api/"
    print "RunRegistry from: ",FULLADDRESS
    server = xmlrpclib.ServerProxy(FULLADDRESS)
    # you can use this for single run query
#    sel_runtable="{runNumber} = "+run+" and {datasetName} LIKE '%Express%'"
    sel_runtable="{groupName} ='Collisions11' and {runNumber} >= " + str(minRun) + " and {datasetName} LIKE '%Express%'"
    #sel_runtable="{groupName} ='Commissioning11' and {runNumber} >= " + str(minRun)# + " and {datasetName} LIKE '%Express%'"

    run_data = server.DataExporter.export('RUN', 'GLOBAL', 'csv_runs', sel_runtable)
    for line in run_data.split("\n"):
        #print line
        run=line.split(',')[0]
        if "RUN_NUMBER" in run or run == "":
            continue
        #print "RUN: " + run
        runlist.append(int(run))
    return runlist



def dbsQuery(dataset, minRun = 1):
    dbs_cmd = 'dbs search --noheader --query="find run,sum(file.numevents) where dataset=' + dataset
    if minRun > 1:
        dbs_cmd += ' and run > ' + str(minRun)
    dbs_cmd += '"'
    #print dbs_cmd
    dbs_out = commands.getstatusoutput(dbs_cmd)
    return dbs_out


class DBSAlCaRecoRunInfo():
    def __init__(self):
        self._runnumber = -1
        #self._nlumi = -1
        self._nevents = -1.
        self._nEventsParent = -1
        return
    
    def run(self):
        return self._runnumber

    #def nLumi(self):
    #    return self._nlumi

    def nEvents(self):
        return self._nevents

    def setNEventsParent(self, nevents):
        self._nEventsParent = nevents

    def nEventsParent(self):
        return self._nEventsParent


    #def nEventsPerLumi(self):
    #    return self._nevents/self._nlumi

    def setFromQuery(self, queryLine):
        values = queryLine.split()
        self.setValues(values)

    def setValues(self, values):
        self._runnumber = int(values[0])
        self._nevents = float(values[1])
        if len(values) == 3:
            self._nEventsParent = float(values[2])
        
    def selEfficiency(self):
        if self._nEventsParent == -1 or self._nEventsParent == 0.:
            return 0
        return self._nevents/self._nEventsParent

    def getList(self):
        theList = [str(self.run()), str(self.nEvents()), str(self.nEventsParent())]
        return theList



class DBSAlCaRecoResults():
    def __init__(self, name, parent):
        self._datasetname = str(name)
        self._parent = str(parent)
        self._infoPerRun = []
        pd = name.split("/")[1]
        othername = name.split("/")[2]
        self._cachefilename = pd + '-' + othername
        return


    def name(self):
        return self._datasetname



    def parent(self):
        return self._parent

    def sort(self):
        self._infoPerRun.sort(key=lambda rr: rr._runnumber)
        return

    def appendQuery(self, queryOut):
        lines = queryOut.split("\n")
        #print len(lines)
        for line in lines:
            #print line
            if line != "":
                alcaRun = DBSAlCaRecoRunInfo()
                alcaRun.setFromQuery(line)
                self._infoPerRun.append(alcaRun)

    def printAll(self):
        self.sort()
        for run in  self._infoPerRun:
            print "run #: " + str(run.run() ) + " # events: " + str(run.nEvents()) + " eff.: "  + str(run.selEfficiency())

    def size(self):
        return len(self._infoPerRun)
    
    def search(self, run):
        self.sort()
        hi = self.size()
        lo = 0
        while lo < hi:
            mid = (lo+hi)//2
            midval = self._infoPerRun[mid].run()
            if midval < run:
                lo = mid+1
            elif midval > run:
                hi = mid
            else:
                return mid

        return -1

    def addParentQuery(self, query):
        for line in query.split("\n"):
            if line != "":
                run = int(line.split()[0])
                nevents = float(line.split()[1])
                index = self.search(run)
                if index != -1:
                    rrep = self._infoPerRun[index].setNEventsParent(nevents)


    def purgeList(self, runs):
        for rrep in self._infoPerRun:
            if not rrep.run() in runs:
                #print "run: " + str(rrep.run()) + " is not a Collision run: remove!"
                self._infoPerRun.remove(rrep)
    

    def writeCache(self):
        cacheFileName = self._cachefilename + ".cache"
        tableForCache =[]
        tableForCache.append(["# run", "# events", "# events parent"])
        for rrep in self._infoPerRun:
            tableForCache.append(rrep.getList())
            
        cacheFile = file(cacheFileName,"w")
        pprint_table(cacheFile, tableForCache)
        cacheFile.close()
        return

    def readCache(self):
        cacheFileName = self._cachefilename + ".cache"
        if os.path.exists(cacheFileName):
            cache = file(cacheFileName,"r")
            data = cache.readlines()
            for line in data:
                if line[0] != '#' and line != "":
                    items = line.split()
                    rrep = DBSAlCaRecoRunInfo()
                    rrep.setValues(items)
                    self._infoPerRun.append(rrep)
            cache.close()      
            if len(self._infoPerRun) != 0:
                return self._infoPerRun[len(self._infoPerRun)-1].run()
        return 1
        

    def buildHistoNEvents(self):
        nRuns = self.size()
        hNEvents = TH1F(self._cachefilename + "-hNEvents","# events",nRuns, 0, nRuns);
        binN = 1
        for rrep in self._infoPerRun:
            hNEvents.SetBinContent(binN, rrep.nEvents())
            hNEvents.GetXaxis().SetBinLabel(binN, str(rrep.run()))
            binN += 1
        hNEvents.GetXaxis().SetTitle("run #")
        hNEvents.GetXaxis().SetTitleOffset(1.6)
        hNEvents.GetYaxis().SetTitle("# events")
        hNEvents.SetFillColor(kRed-9)
        hNEvents.LabelsOption("v","X")
        return hNEvents


    def buildHistoEff(self):
        nRuns = self.size()
        hEff = TH1F(self._cachefilename + "-hEff","# events",nRuns, 0, nRuns);
        binN = 1
        for rrep in self._infoPerRun:
            hEff.SetBinContent(binN, rrep.selEfficiency())
            hEff.GetXaxis().SetBinLabel(binN, str(rrep.run()))
            binN += 1
        hEff.GetXaxis().SetTitle("run #")
        hEff.GetXaxis().SetTitleOffset(1.6)
        hEff.GetYaxis().SetTitle("Sel. eff.")
        hEff.SetFillColor(kBlue-1)
        hEff.LabelsOption("v","X")
        return hEff

def getDatasets(pd, epoch, version, tier):
    dbs_cmd = 'dbs search --noheader --query="find dataset where dataset=/' + pd + '/' + epoch + '*' + version + '/' + tier +'"'
    print dbs_cmd
    dbs_out = commands.getstatusoutput(dbs_cmd)
    listofgroups = dbs_out[1].split("\n")
    return listofgroups

    
if __name__ == "__main__":

    configfile = ConfigParser()
    configfile.optionxform = str


    configfile.read('GT_branches/AlCaRecoMonitoring.cfg')
    webArea = configfile.get('Common','webArea')
    groups = configfile.get('Common','groups').split(",")

    alcarecoDatasets = []
        


    # get the list of interesting runs from RR
    runList = []
    runList = getRunList(1)    
    #print runList

    os.chdir(webArea)

    for group in groups:
        if group == "":
            continue
        print group
        epoch = configfile.get(group, 'epoch')
        version = configfile.get(group, 'version')
        rawversion = configfile.get(group, 'rawversion')
        htmlwriter = WebPageWriter(group, epoch, version)
        datasets = getDatasets("*",epoch, version, "ALCARECO")
        for dataset in datasets:
            pd = dataset.split("/")[1]
            parenttier = "RECO"
            pdforhtml = pd
            details = AlcaRecoDetails(dataset, pdforhtml, epoch, version)
            if pd == 'StreamExpressCosmics':
                continue
            htmlwriter.addDataset(pdforhtml, details)
            if pd == 'StreamExpress':
                pd = 'ExpressPhysics'
                parenttier = "FEVT"
            parent = getDatasets(pd,epoch, version, parenttier)
            if parent[0] == '':
                parent = getDatasets(pd,epoch, rawversion,"RAW")
            print "--------------------------------------------"
            print dataset
            print pd
            print parent
            alcarecoDatasets.append(DBSAlCaRecoResults(dataset, parent[0]))
            
        htmlwriter.buildPage()
    
    #alcarecoDatasets.append(DBSAlCaRecoResults("/StreamExpress/Run2011A-TkAlMinBias-v2/ALCARECO", "/ExpressPhysics/Run2011A-Express-v2/FEVT"))

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
        lastCached = dataset.readCache()
        query = dbsQuery(dataset.name(), lastCached)
        dataset.appendQuery(query[1])
        queryParent = dbsQuery(dataset.parent(), lastCached)
        dataset.addParentQuery(queryParent[1])
        dataset.purgeList(runList)
        dataset.printAll()
        dataset.writeCache()

        label1 = TLatex(0.015, 0.93007, dataset.name())
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


    indexBuilder = WebPageIndex()
    indexBuilder.scan(webArea)
    indexBuilder.buildPage()

    #raw_input ("Enter to quit")
    sys.exit(0)
    
    

    

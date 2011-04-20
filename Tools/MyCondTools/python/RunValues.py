import sys
import json
#import socket
import urllib2

from DBChecker import DBChecker
from Tier0LastRun import Tier0LastRun

class RunValues(object):

    def getLargestReleasedForPrompt(self,src = "https://cmsweb.cern.ch/tier0/runs", proxy = None, out = 5):
        try:
            if proxy:
                print "setting proxy"
                opener = urllib2.build_opener(urllib2.HTTPHandler(), urllib2.HTTPSHandler(), urllib2.ProxyHandler({'http':proxy, 'https':proxy}))
                urllib2.install_opener(opener)
            #socket.setdefaulttimeout(out)
            req = urllib2.Request(src)
            req.add_header("User-Agent","ConditionOfflineDropBox/1.0 python/%d.%d.%d" % sys.version_info[:3])
            req.add_header("Accept","application/json")
            jsonCall = urllib2.urlopen(req, timeout = out)
            jsonText = jsonCall.read()
            data = json.loads(jsonText)
            tr = Tier0LastRun(data)
            rn = tr.getBiggestNum('run',('reco_started', 1))+1
            
            return str(rn)
        except:
            errStr = "Cannot retrieve next run released for Prompt at Tier-0 from URL \"" +src+"\""
            if proxy:
                errStr += " using proxy \"" + proxy + "\""
            raise ValueError(errStr)

    def getSmallestWaitingForPrompt(self,src = "https://cmsweb.cern.ch/tier0/runs", proxy = None, out = 5):
        try:
            if proxy:
                print "setting proxy"
                opener = urllib2.build_opener(urllib2.HTTPHandler(), urllib2.HTTPSHandler(), urllib2.ProxyHandler({'http':proxy, 'https':proxy}))
                urllib2.install_opener(opener)
            #socket.setdefaulttimeout(out)
            req = urllib2.Request(src)
            req.add_header("User-Agent","ConditionOfflineDropBox/1.0 Python-urllib/%d.%d.%d" % sys.version_info[:3])
            req.add_header("Accept","application/json")
            jsonCall = urllib2.urlopen(req, timeout = out)
            jsonText = jsonCall.read()
            data = json.loads(jsonText)
            tr = Tier0LastRun(data)
            rn = tr.getSmallestNum('run',('reco_started', 0))
            
            return str(rn)
        except:
            errStr = "Cannot retrieve the smallest run waiting for Prompt at Tier-0 from URL \"" +src+"\""
            if proxy:
                errStr += " using proxy \"" + proxy + "\""
            raise ValueError(errStr)
    
    def getNewHLT(self,authPath = "/nfshome0/popcondev/conddb",dbName = "oracle://cms_orcon_prod/CMS_COND_31X_RUN_INFO",tag = "runinfo_start_31X_hlt"):
        try:
            d = DBChecker(dbName, authPath)
            rn = d.lastSince(tag)+1
            return str(rn)
        except ValueError:
            raise ValueError("Cannot retrieve next HLT run from tag \"" + tag + "\" in \"" +dbName+"\" for RDBMS in \""+authPath+"\"")

if __name__ == "__main__":
    rv = RunValues()
    print rv.getNewHLT("/afs/cern.ch/cms/DB/conddb", "oracle://cms_orcoff_prod/CMS_COND_31X_RUN_INFO", "runinfo_start_31X_hlt")
    try:
        print rv.getNewHLT("/afs/cern.ch/cms/DB/conddb", "oracle://cms_orcoff_prod/CMS_COND_31X_RUN_INFO", "runinfo_start_31X_dummy")
    except ValueError, v:
        print "KNOWN ERROR", str(v)
    except:
        print "UNKNOWN ERROR"
    largestReleased = rv.getLargestReleasedForPrompt("https://cmsweb.cern.ch/tier0/runs")
    smallestWaiting = rv.getSmallestWaitingForPrompt("https://cmsweb.cern.ch/tier0/runs")
    print "largestReleased: %s, smallestWaiting: %s" %(largestReleased, smallestWaiting)
    if int(largestReleased) <= int(smallestWaiting):
        print "Runs in order"
    else:
        print "WARNING: Runs not in order!"
    try:
        print rv.getSmallestWaitingForPrompt("http://vocms115.cern.ch:8070/tier0/runs") #"http://vocms115.cern.ch:8304/tier0/runs"
    except ValueError, v:
        print "KNOWN ERROR", str(v)
    except:
        print "UNKNOWN ERROR"    

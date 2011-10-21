import json
import sys, urllib2
import time

#from xml.dom import minidom

class Tier0DasInterface:
    def __init__(self, url = 'https://cmsweb.cern.ch/tier0/'):
        #self._t0DasBaseUrl = "http://gowdy-wttest.cern.ch:8304/tier0/"
        self._t0DasBaseUrl = url
        self._debug = False
        self._retry = 0
        self._maxretry = 5
        
    def getData(self, src, tout = 5, proxy = None ):
        # actually get the json file from the given url of the T0-Das service
        # and returns the data
        
        try:
            if proxy:
                print "setting proxy"
                opener = urllib2.build_opener(urllib2.HTTPHandler(),
                                              urllib2.HTTPSHandler(),
                                              urllib2.ProxyHandler({'http':proxy, 'https':proxy}))
                urllib2.install_opener(opener)
            req = urllib2.Request(src)
            req.add_header("User-Agent",
                           "PCLMonitor/1.0 python/%d.%d.%d" % sys.version_info[:3])
            req.add_header("Accept","application/json")
            jsonCall = urllib2.urlopen(req, timeout = tout)
            url = jsonCall.geturl()
        except urllib2.HTTPError,  error:
            #print error.url
            errStr = "Cannot retrieve Tier-0 DAS data from URL \"" + error.url + "\""
            if proxy:
                errStr += " using proxy \"" + proxy + "\""
            print errStr
            print error
            raise urllib2.HTTPError("FIXME: handle exceptions")
        except urllib2.URLError,  error:
            if self._retry < self._maxretry:
                print 'Try # ' + str(self._retry) + " connection to Tier-0 DAS timed-out"
                self._retry += 1
                newtout = tout*self._retry
                time.sleep(3*self._retry)
                return self.getData(src,newtout,proxy)
            else:
                errStr = "Cannot retrieve Tier-0 DAS data from URL \"" + src + "\""
                if proxy:
                    errStr += " using proxy \"" + proxy + "\""
                self._retry = 0
                print errStr
                print error
                raise urllib2.URLError('TimeOut reading ' + src)

        except:
            raise
        else:
            if self._debug:
                print url
            jsonInfo = jsonCall.info()
            if self._debug:
                print jsonInfo
            jsonText = jsonCall.read()
            data = json.loads(jsonText)
            if self._debug:
                print "data:",data
            return data

    def getValues(self, json, key, selection = ''):
        # lookup for a key in a json file applying possible selections
        data = []
        check = 0
        if selection != '':
            check = 1
            (k, v) = selection

        for o in json:
            #print o
            try:
                if check == 1:
                    if (o[k] == v): 
                        data.append(o[key])
                else:
                    data.append(o[key])
            except KeyError as error:
                print "[Tier0DasInterface::getValues] key: " + key + " not found in json file"
                print error
                raise
            except:
                print "[Tier0DasInterface::getValues] unknown error"
                raise
                #pass
        #print data
        return data

    def lastPromptRun(self):
        url = self._t0DasBaseUrl + "runs"
        try:
            json = self.getData(url)
            return max(self.getValues(json, 'run', ('reco_started', 1)))+1
        except:
            print "[Tier0DasInterface::lastPromptRun] error"
            raise
            return 0




    def firstConditionSafeRun(self):
        url = self._t0DasBaseUrl + "firstconditionsaferun"
        try:
            json = self.getData(url)
            return max(self.getValues(json, 'run_id'))
        except Exception:
            print "[Tier0DasInterface::firstConditionSafeRun] error"
            raise
            return 0


if __name__ == "__main__":

    
    test = Tier0DasInterface()
    try:
        print "Tier0 DAS last run released for PROMPT:       ", test.lastPromptRun()
    except Exception as error:
        print 'Error 1'
        print error
    try:
        print "Tier0 DAS first run safe for condition update:", test.firstConditionSafeRun()
    except Exception as error:
        print 'Error 2'
        print error


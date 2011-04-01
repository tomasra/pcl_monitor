import json
import urllib
#from xml.dom import minidom

class Tier0LastRun(object):

    def __init__(self, json):
        self.__json__ = json['results']

    # objectName = (key, value)
    def isObjectEqual(self, (key, value)):
        for o in self.__json__:
            try:
                if o[key] == value:
                    return 1
            except Exception:
                pass

        return 0

    # options = [(key, value),...]
    def getValues(self, key, option = ''):
        data = []
        check = 0
        if option != '':
            check = 1
            (k, v) = option

        for o in self.__json__:
            try:
                if check == 1:
                    if (o[k] == v): 
                        data.append(o[key])
                else:
                    data.append(o[key])
            except Exception:
                pass

        return data

    def getBiggestNum(self, key, option = ''):
        
        try:
            return max(self.getValues(key, option))
        except Exception:
            return 0

    def getSmallestNum(self, key, option = ''):
        
        try:
            return min(self.getValues(key, option))
        except Exception:
            return 0
    
    def performTest(self, json, delay = 0):
        if delay == 0:
            if json.isObjectEqual(('reco_started', 1)):
                return json.getBiggestNum('run', ('reco_started', 1))+1
            else:
            	return json.getSmallestNum('run', ('reco_started', 0))
        else:
    	    if json.isObjectEqual(('status', 'CloseOutRepackMerge')):
            	return json.getSmallestNum('run')
            else:
                if json.isObjectEqual(('reco_started', 1)):
                    return json.getBiggestNum('run', ('reco_started', 1))+1
                else:
                    return json.getSmallestNum('run', ('reco_started', 0))

if __name__ == "__main__":
    #src = "http://vocms52.cern.ch:8888/tier0/runs"
    #jsonData = minidom.parse(urllib.urlopen(src)).getElementsByTagName('das')[0].firstChild.nodeValue.replace("'", "\"")
    #src = "http://vocms52.cern.ch:8889/tier0/runs"
    src = "https://cmsweb.cern.ch/tier0/runs"
    jsonData = urllib.urlopen(src).read().replace("'", "\"")
    #src = "tier0.js"
    #jsonData = open(src, 'r').read().replace("'", "\"")
    data = json.loads(jsonData)
    wrapper = Tier0LastRun(data)

    #obj		=	Tier0LastRun_wf()

    print wrapper.performTest(wrapper)


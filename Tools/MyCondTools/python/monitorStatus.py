import json
import sys


class MonitorStatus:
    def __init__(self, name):
        self._statusMap = {}
        self._statusMap['name'] = name

    def setWebUrl(self, url):
        self._statusMap['weburl'] = url

    def setStatus(self, status, msg):
        self._statusMap['status'] = int(status)
        self._statusMap['msg'] = str(msg)

    def setUpdateTime(self, date):
        self._statusMap['update'] = str(date)
        print date
        print str(date)
        print self._statusMap['update']
        
    def writeJsonFile(self, filename):
        # get a string with JSON encoding the list
        #dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        dump = json.dumps(self._statusMap)
        file = open(filename, 'w')
        file.write(dump + "\n")
        file.close()

    def readJsonFile(self, filename):
        jsonData = open(filename)
        self._statusMap = json.load(jsonData)
        jsonData.close()

    def getField(self, key):
        return self._statusMap[key]

if __name__ == "__main__":
    import datetime
    status = MonitorStatus("TestApp")
    status.setStatus(1,"run 333333: No PLC Upload")
    status.setUpdateTime(datetime.datetime.today())
    status.writeJsonFile("test.json")

    readstatus =  MonitorStatus("TestApp")
    readstatus.readJsonFile("test.json")
    print readstatus._statusMap
    print readstatus.getField("msg")

    

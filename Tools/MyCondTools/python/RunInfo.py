import datetime

def getDate(string):
    date = string.split()[0].split('-')
    time = string.split()[1].split(':')
    datet = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]),int(float(time[2])))
    return datet

class RunInfoContent:
    def __init__(self, summary):
        listofEntries = summary.split(',')
        self._run = listofEntries[0].lstrip('RUN:').lstrip()
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
        date = string.split('T')[0].split('-')
        time = string.split('T')[1].split(':')
        datet = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]),int(float(time[2])))
        return datet

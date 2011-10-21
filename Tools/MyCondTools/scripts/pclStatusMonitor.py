#!/usr/bin/env python
from optparse import OptionParser
import urllib2
import json
import datetime

# Nagios plugin to monitor the PCL status


# Exit statuses recognized by Nagios
UNKNOWN = -1
OK = 0
WARNING = 1
CRITICAL = 2


def outJSON(hostname,port,url,serviceName):
    dict=[]
    try:
        url = 'http://%s:%s%s' % (hostname, port, url)
        #Checking if we get response from server, timeout after 10 sec.
	dict	=	eval(urllib2.urlopen(url).read())
    except Exception, e:
        print 'WARNING - Could not reach page at %s: %s' % (url, e)
        raise SystemExit, UNKNOWN

    return dict



if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-H', '--hostname', dest='hostname')
    parser.add_option('-p', '--port', dest='port')
    parser.add_option('-u', '--url', dest='url')
    parser.add_option('-s', '--serviceName', dest='serviceName')
    
    options, args = parser.parse_args()

    # Check for required options
    for option in ('hostname', 'port', 'url', 'serviceName'):
        if not getattr(options, option):
            print 'UNKNOWN - %s not specified' % option.capitalize()
            raise SystemExit, UNKNOWN

    # Check for expected result
    statusdict = outJSON(options.hostname,options.port,options.url,options.serviceName)


    try:
        status  = statusdict['status']
        message = statusdict['msg']
        webinterface = statusdict['weburl']
        lastupdate = datetime.datetime.strptime(statusdict['update'],"%Y-%m-%d %H:%M:%S.%f")
        
        if datetime.datetime.today() - lastupdate > datetime.timedelta(hours=8,minutes=10):
            print "WARNING: reading staled information, last update on: %s.  &#60a target='newpage' href&#61\"%s\"&#62 More details &#60/a&#62 " % (statusdict['update'], webinterface)
            raise SystemExit, UNKNOWN

        if status == 0:
            print "%s. &#60a target='newpage' href&#61\"%s\"&#62 More details &#60/a&#62 " % (message,webinterface)
            raise SystemExit, OK
        elif status < 0:
            print "%s. &#60a target='newpage' href&#61\"%s\"&#62 More details &#60/a&#62 " % (message,webinterface)
            raise SystemExit, UNKNOWN
        elif status > 1000:
            print "%s. &#60a target='newpage' href&#61\"%s\"&#62 More details &#60/a&#62 " % (message,webinterface)
            raise SystemExit, CRITICAL
        elif status > 100:
            print "%s. &#60a target='newpage' href&#61\"%s\"&#62 More details &#60/a&#62 " % (message,webinterface)
            raise SystemExit, WARNING
        
    except Exception, e:
        print 'WARNING - Could not assess the status: %s' % ( e)
        raise SystemExit, WARNING


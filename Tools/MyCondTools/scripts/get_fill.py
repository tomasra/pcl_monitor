#!/usr/bin/env python
import os,string,sys,commands,time
import xmlrpclib


def get_map():
    runfillmap={}
    fill=-1
    FULLADDRESS="http://pccmsdqm04.cern.ch/runregistry/xmlrpc"
    print "RunRegistry from: ",FULLADDRESS
    server = xmlrpclib.ServerProxy(FULLADDRESS)
    # you can use this for single run query
#    sel_runtable="{runNumber} = "+run+" and {datasetName} LIKE '%Express%'"
    sel_runtable="{groupName} ='Collisions11' and {runNumber} >= 132440 and {datasetName} LIKE '%Online%'"

    run_data = server.DataExporter.export('RUN', 'GLOBAL', 'csv_runs', sel_runtable)
    for line in run_data.split("\n"):
        run=line.split(',')[0]
        print run
        print line
        if run.isdigit():

            # we need to do something to avoid parsing commas in comment column
            group=line.split(',')[8]
            #energy=group.split(',')[0]
            fill=line.split(',')[line.count(",") - 7]
            runfillmap[run]=fill
            print fill
    items = runfillmap.items()
    #print items
    items.sort()
    #print items

    for runAndFill in items:
        print 'Run #: ' + str( runAndFill[0] ) + "  fill: " + str( runAndFill[1])
    
    
    return runfillmap



#main
#print get_map()
get_map()

import os,string,sys,commands,time,json
import xmlrpclib
from Tools.MyCondTools.rrapi import RRApi, RRApiError

"""
Module providing an interface to the RunRegistry 2 and RunRegistry 3 APIs.

$Date: 2012/09/20 14:34:32 $
$Revision: 1.6 $
Author: G.Cerminara

"""



def getRunList(minRun):
    """
    Gets the list of Collision runs registered as 'Online' and 'Collision11' in RR2.
    The only input parameter is the minRun #, all the rest is hard-coded...sorry about it.
    """
    runlist = []

    #FULLADDRESS="http://pccmsdqm04.cern.ch/runregistry_api/"    
    #FULLADDRESS="http://pccmsdqm04.cern.ch/runregistry/xmlrpc"
    FULLADDRESS="http://cms-service-runregistry-api.web.cern.ch/cms-service-runregistry-api/xmlrpc"

    print "RunRegistry from: ",FULLADDRESS
    server = xmlrpclib.ServerProxy(FULLADDRESS)
    # you can use this for single run query
#    sel_runtable="{runNumber} = "+run+" and {datasetName} LIKE '%Express%'"
    #sel_runtable="{groupName} ='Collisions11' and {runNumber} >= " + str(minRun) + " and {datasetName} LIKE '%Express%'"
    sel_runtable="{groupName} ='Collisions11' and {runNumber} >= " + str(minRun) + " and {datasetName} LIKE '%Online%'"

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


def getValues(json, key, selection = ''):
    """
    Extract a value for a particular key in a json file.
    """
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
            print "[RunRegistryTools::getValues] key: " + key + " not found in json file"
            print error
            raise
        except:
            print "[RunRegistryTools::getValues] unknown error"
            raise
            #pass
    #print data
    return data



def getRunListRR3(minRun, datasetName, runClassName):
    """
    Get the run-list from RR3. In this case the datasetName and run-class can be passed as
    input together with the min run #
    """
    FULLADDRESS  = "http://runregistry.web.cern.ch/runregistry/"

    print "RunRegistry from: ",FULLADDRESS

    # connect to API
    try:
        api = RRApi(FULLADDRESS, debug = True)
    except RRApiError, error:
        print error


    filter = {}
    filter['runNumber'] = ">= %s" % str(minRun)
    filter['datasetName'] = " LIKE '%" + datasetName + "%'"
    #filter = {'runNumber': ">= %s" % str(minRun), 'datasetName':  " LIKE '%" + datasetName + "%'"}

    if runClassName != '':
        filter['runClassName'] = " = '%s'" % runClassName

    print filter

    template = 'json'
    table = 'datasets'
    data = api.data(workspace = 'GLOBAL', columns = ['runNumber', 'datasetName', 'runClassName'], table = table, template = template, filter = filter)

    #print json.dumps(data)

    #print getValues(data, 'runNumber')
    

    return getValues(data, 'runNumber')



if __name__ == "__main__":
    print getRunListRR3(200246, "Online", "Commissioning12")
    

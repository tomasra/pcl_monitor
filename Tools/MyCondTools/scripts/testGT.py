#!/usr/bin/env python

import os
import sys
import fileinput
from subprocess import Popen, PIPE
import getpass

def modifyCfgs(wf, GT, local, hltVersion):
    """ This function finds the directory created by runTheMatrix for the given workflow number assuming it starts by that number.
    It finds all the cfgs assuming they are the only files in that directory ending with \".py\".
    It modifes them by replacing the GlobalTag with the one to test. It also modifies the connection string if the test is local.
    It returns the dir and the list of cfgs.
    """
    print "discovering cfgs"
    cfgList = []
    testDir = ""
    for dir in os.listdir(os.getcwd()):
        if os.path.isdir(dir) and dir.startswith(str(wf)):
            testDir = GT+'_'+dir
            os.system('rm -rf '+testDir)
            print "testDir =", testDir
            os.system('mv '+dir+' '+testDir)
            for file in os.listdir(testDir):
                if file.endswith(".py"):
                    print file
                    cfgList.append(file)
                    #FIXME this can be done directly with a runTheMatrix option
                    for line in fileinput.FileInput(testDir+"/"+file,inplace=1):
                        # Remove any unneeded pre-existing connection string if running in local
                        localConnect = local and line.find("process.GlobalTag.connect") != -1
                        if localConnect:
                            line = "\n"
                        if GT.startswith("FT") and line.find("process.GlobalTag.pfnPrefix") != -1 and line.find("frontier://FrontierProd/") != -1:
                            # line = line.replace("FrontierProd", "FrontierArc")
                            line = "\n"
                        if line.find('HLTrigger.Configuration.HLT_') != -1 and hltVersion != "":
                            line = "process.load('HLTrigger.Configuration.HLT_"+hltVersion+"_cff')\n"
                        # Replace the globalTag name
                        notHltStepGreaterThan1 = (not GT.startswith("GR_H")) or (GT.startswith("GR_H") and file.find("HLT") != -1)
                        if notHltStepGreaterThan1:
                            if line.find("process.GlobalTag = GlobalTag(process.GlobalTag,") != -1 or line.find("process.GlobalTag.globaltag") != -1:
                                line = "process.GlobalTag.globaltag = '"+GT+"::All'\n"
                                if local:
                                    userName = getpass.getuser()
                                    if userName:
                                        letter = userName[0]
                                    else:
                                        print "Error: empty user name"
                                        sys.exit(1)
                                    line += 'process.GlobalTag.connect = "sqlite_file:/afs/cern.ch/user/'+letter+'/'+userName+'/public/Alca/GlobalTag/'+GT+'.db"\n'
                        print line,
    return testDir, cfgList

def runTest(GT, wf, local, option, HLTVersion, stdoutFile, stderrFile, exitCodeFile, recycle):
    """ This function runs creates the configuration files, modifes them for the GT to be tested and runs the jobs.
    The outputs are saved in local files and they can be retrieved after the tests.
    """
    cmd = "runTheMatrix.py -l "+str(wf)+" "+option+" -j 0"
    print "runTheMatrix.py -l "+str(wf)+" "+option+" -j 0"

    if local:
        where = "local"
    else:
        where = "db"
    exitCodeFile.write(GT+" "+str(wf)+" "+where+"\n")
    exitCodeFile.write(cmd+"\n")

    # Create the cfgs
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
    stdout, stderr = p.communicate()

    # modify the cfgs before running
    testDir, cfgList = modifyCfgs(wf, GT, local, hltVersion)

    # FIXME: it happens that sorting is enough with the current workflows. It could be that the first
    # file is not the correct one, in that case this should be adapted
    cfgList.sort()
    print cfgList

    for cfg in cfgList:
        if recycle and not cfg.startswith("step"):
            continue
        cmd = "cd "+testDir+"; cmsRun "+cfg
        print cmd
        test = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        stdout, stderr = test.communicate()
        stdoutFile.write(stdout+"\n")
        stderrFile.write(stderr+"\n")
        exitCodeFile.write(str(test.returncode)+" ")
        print "exit code = ", test.returncode
    exitCodeFile.write("\n\n")

def getWfList(GT):
    """ Decide whether the GT is for data or MC from its name.
    """
    if GT.startswith("STARTHI") or GT.startswith("PRE_SH"):
        return [40] # , 41, 42]
    elif GT.startswith("DES") or GT.startswith("MC") or GT.startswith("START") or GT.startswith("POST") or GT.startswith("PRE_MC") or GT.startswith("PRE_ST") or GT.startswith("PRE_PO") :
        if option == "--what upgrade":
            return [3310]
        else:
            return [29]
    elif GT.startswith("GR_H"):
        return [4.291]
    elif GT.startswith("GR_E"):
        # return [1001]
        # return [4.17] # RunMinBias2011A
        # return [4.29] # RunMinBias2011B
        # return [4.40] # RunMinBias2012A
        return [4.51] # RunMinBias2012B
    elif GT.startswith("GR_P") or GT.startswith("PRE_P"):
        # return [1000, 4.17] # RunMinBias2011A
        # return [1000, 4.29] # RunMinBias2011B
        # return [1000, 4.40] # RunMinBias2012A
        return [1000, 4.51] # RunMinBias2012B
    elif GT.startswith("GR") or GT.startswith("FT") or GT.startswith("PRE"):
        # return [4.17] # RunMinBias2011A
        # return [4.29] # RunMinBias2011B
        # return [4.40] # RunMinBias2012A
        return [4.51] # RunMinBias2012B
    else:
        print "Error: unknonwn GT type for ", GT
    return []

if __name__ == '__main__':

    # Parse input parameters
    local = False
    option = ""
    hltVersion = ""
    if len(sys.argv) < 2 or len(sys.argv) > 5:
        print "Usage: testGT.py GT_NAME local|remote [option] [HLTVERSION]"
        sys.exit(1)
    GT = sys.argv[1]
    if sys.argv[2] == "local":
        local = True
    elif sys.argv[2] != "remote":
        print "The second argument can only be local or remote, received", sys.argv[2], "exiting."
        sys.exit(1)
    # This is a string containing optional parameters to be passed to runTheMatrix.py
    if len(sys.argv) > 3:
        option = sys.argv[3]
    if len(sys.argv) == 5:
        hltVersion = sys.argv[4]

    # if True skip the generation of mc samples
    recycle = False

    stdoutFileName = "stdoutFile.txt"
    stderrFileName = "stderrFile.txt"
    exitCodeFileName = "exitCodeFile.txt"

    stdoutFile = open(stdoutFileName, "w")
    stderrFile = open(stderrFileName, "w")
    exitCodeFile = open(exitCodeFileName, "w")

    wfList = getWfList(GT)
    # Run all the tests
    for wf in wfList:
        runTest(GT, wf, local, option, hltVersion, stdoutFile, stderrFile, exitCodeFile, recycle)

    stdoutFile.close()
    stderrFile.close()
    exitCodeFile.close()

    stdoutFile = open(stdoutFileName, "r")
    stderrFile = open(stderrFileName, "r")
    exitCodeFile = open(exitCodeFileName, "r")

    # All tests done, send a mail.
    separator = "\n\n----------------------------\n\n"
    mailFileName = "mail.txt"
    mail = open(mailFileName, "w")
    mail.write(exitCodeFile.read() + separator + stdoutFile.read() + separator + stderrFile.read())
    mail.close()
    # os.system("mail -s \"Global Tag test\" \"marco.de.mattia@cern.ch\" < \""+mailFileName+"\"")
    os.system("mail -s \"Tagset validation\" \"cms-alca-globaltag@cern.ch\" < \""+mailFileName+"\"")
    # os.system("mail -s \"Tagset validation\" \"cms-alca-globaltag@cern.ch\" < \""+mailFileName+"\"")

    stdoutFile.close()
    stderrFile.close()
    exitCodeFile.close()


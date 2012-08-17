#!/usr/bin/env python

import os
import sys
import fileinput
from subprocess import Popen, PIPE
import getpass

def modifyCfgs(wf, GT, local):
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
            testDir = dir
            for file in os.listdir(dir):
                if file.endswith(".py"):
                    print file
                    cfgList.append(file)
                    #FIXME this can be done directly with a runTheMatrix option
                    for line in fileinput.FileInput(dir+"/"+file,inplace=1):
                        # Remove any unneeded pre-existing connection string if running in local
                        localConnect = local and line.find("process.GlobalTag.connect") != -1
                        if localConnect:
                            line = "\n"
                        if GT.startswith("FT") and line.find("process.GlobalTag.pfnPrefix") != -1 and line.find("frontier://FrontierProd/") != -1:
                            line = line.replace("FrontierProd", "FrontierArc")
                        # Replace the globalTag name
                        notHltStepGreaterThan1 = (not GT.startswith("GR_H")) or (GT.startswith("GR_H") and file.find("HLT") != -1)
                        if notHltStepGreaterThan1:
                            if line.find("process.GlobalTag.globaltag") != -1:
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

def runTest(GT, wf, local, stdoutFile, stderrFile, exitCodeFile, recycle):
    """ This function runs creates the configuration files, modifes them for the GT to be tested and runs the jobs.
    The outputs are saved in local files and they can be retrieved after the tests.
    """
    cmd = "runTheMatrix.py -l "+str(wf)+" -j 0"

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
    testDir, cfgList = modifyCfgs(wf, GT, local)

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
    if GT.startswith("STARTHI"):
        return [40, 41, 42]
    elif GT.startswith("DESIGN") or GT.startswith("MC") or GT.startswith("START"):
        return [29, 35]
    elif GT.startswith("GR_H"):
        return [4.291]
    elif GT.startswith("GR_E"):
        # return [1001]
        return [4.17]
    elif GT.startswith("GR_P"):
        return [1000, 4.17]
    elif GT.startswith("GR") or GT.startswith("FT"):
        return [4.17]
    else:
        print "Error: unknonwn GT type for ", GT
    return []

if __name__ == '__main__':

    # Parse input parameters
    local = False
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print "Usage: testGT.py GT_NAME [local]"
        sys.exit(1)
    if len(sys.argv) == 2:
        GT = sys.argv[1]
    elif sys.argv[2] == "local":
        GT = sys.argv[1]
        local = True
    else:
        print "The second argument can only be local, received", sys.argv[2], "exiting."
        sys.exit(1)

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
        runTest(GT, wf, local, stdoutFile, stderrFile, exitCodeFile, recycle)

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

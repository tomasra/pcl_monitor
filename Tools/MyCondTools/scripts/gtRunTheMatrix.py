#!/usr/bin/env python

import os, sys, re, time

import random
from threading import Thread
try:
    from Configuration.PyReleaseValidation.WorkFlow import WorkFlow
except ImportError:
    print "ops..old API!"

from runTheMatrix import *


def modifyCommandForGT(command, gtName, isLocal):
    if command == None:
        return command


    command = command.replace('EVENTS: 2000000', 'EVENTS: 200')
    #print "COMMAND: " + command

    releasearea = os.environ["CMSSW_BASE"]
    username = os.environ["USER"]
    usernameinit = username[0]
    if 'CMSSW_3_6' in  releasearea  or 'CMSSW_3_5' in  releasearea :
        command = command.replace('auto:mc',gtName+"::All")
        command = command.replace('auto:startup',gtName+"::All")
        command = command.replace('auto:craft08',gtName+"::All")
        command = command.replace('auto:craft09',gtName+"::All")
        command = command.replace('auto:com10',gtName+"::All")
        command = command.replace('auto:starthi',gtName+"::All")

        if isLocal and "cmsDriver" in command:
            command = command + " --customise  Configuration/StandardSequences/customGT_" + gtName + ".py"

    else:
        conditionOpt = gtName + "::All"
        if isLocal:
            conditionOpt += ",sqlite_file:/afs/cern.ch/user/" + usernameinit + "/" + username + "/public/Alca/GlobalTag/" + gtName + ".db"
        command = command.replace('auto:mc',conditionOpt)
        command = command.replace('auto:startup',conditionOpt)
        command = command.replace('auto:craft08',conditionOpt)
        command = command.replace('auto:craft09',conditionOpt)
        command = command.replace('auto:com10',conditionOpt)
        command = command.replace('auto:starthi',conditionOpt)
        

    return command



def duplicateWorkflowForGTTest(matrixreader, wfid, newwfid, gtName, isLocal=False):
    print "# of workflows in the matrix: " + str(len(matrixreader.workFlows))

    for wf in matrixreader.workFlows:
        if float(wfid) == float(wf.numId):
            print "Duplicate workflow: " + wf.nameId + " for GT: " + gtName
            if isLocal == False:
                newWfname = gtName + '_FRONTIER+' + wf.nameId
            else:
                newWfname = gtName + '_LOCAL+' + wf.nameId
            if hasattr(wf, 'input'):
                # this is the new version of the API (> 43X)
                step2addition = ""
                if wfid == '40':
                    # don't genererate a sample in the acse of the HI workflow
                    step2addition = " --himix  --process HIMIX --filein   /store/relval/CMSSW_3_9_7/RelValPyquen_ZeemumuJets_pt10_2760GeV/GEN-SIM-DIGI-RAW-HLTDEBUG/START39_V7HI-v1/0054/102FF831-9B0F-E011-A3E9-003048678BC6.root"
                    
                matrixreader.workFlows.append(WorkFlow(str(newwfid), newWfname, modifyCommandForGT(wf.cmdStep1,gtName, isLocal), modifyCommandForGT(wf.cmdStep2,gtName, isLocal) + step2addition, modifyCommandForGT(wf.cmdStep3,gtName, isLocal), modifyCommandForGT(wf.cmdStep4,gtName, isLocal), wf.input))
            else:
                # old versin of the API
                matrixreader.workFlows.append(WorkFlow(str(newwfid), newWfname, modifyCommandForGT(wf.cmdStep1,gtName, isLocal), modifyCommandForGT(wf.cmdStep2,gtName, isLocal), modifyCommandForGT(wf.cmdStep3,gtName, isLocal), modifyCommandForGT(wf.cmdStep4,gtName, isLocal)))


def runGTSelectionFrom52(gts, gtmap, isLocal, nThreads=4, original=False, show=False):

    print "new release"
    stdList = ['5.2', # SingleMu10 FastSim
               '7',   # Cosmics+RECOCOS+ALCACOS
               '8',   # BeamHalo+RECOCOS+ALCABH
               '25',  # TTbar+RECO2+ALCATT2  STARTUP
               ]
    hiStatList = [
                  '121',   # TTbar_Tauola
                  '123.3', # TTBar FastSim
                   ]







    import optparse
    usage = 'usage: runTheMatrix.py --show -s '

    # parser = optparse.OptionParser(usage)

    parser.add_option('-j','--nproc',
                      help='number of threads. 0 Will use 4 threads, not execute anything but create the wfs',
                      dest='nThreads',
                      default=4
                     )
    parser.add_option('-n','--showMatrix',
                      help='Only show the worflows. Use --ext to show more',
                      dest='show',
                      default=False,
                      action='store_true'
                      )
    parser.add_option('-e','--extended',
                      help='Show details of workflows, used with --show',
                      dest='extended',
                      default=False,
                      action='store_true'
                      )
    parser.add_option('-s','--selected',
                      help='Run a pre-defined selected matrix of wf',
                      dest='restricted',
                      default=False,
                      action='store_true'
                      )
    parser.add_option('-l','--list',
                     help='Coma separated list of workflow to be shown or ran',
                     dest='testList',
                     default=None
                     )
    parser.add_option('-r','--raw',
                      help='Temporary dump the .txt needed for prodAgent interface. To be discontinued soon. Argument must be the name of the set (standard, pileup,...)',
                      dest='raw'
                      )
    parser.add_option('-i','--useInput',
                      help='Use recyling where available',
                      dest='useInput',
                      default=None
                      )
    parser.add_option('-w','--what',
                      help='Specify the set to be used. Argument must be the name of the set (standard, pileup,...)',
                      dest='what',
                      default='all'
                      )
    parser.add_option('--step1',
                      help='Used with --raw. Limit the production to step1',
                      dest='step1Only',
                      default=False
                      )
    parser.add_option('--fromScratch',
                      help='Coma separated list of wf to be run without recycling',
                      dest='fromScratch',
                      default=None
                       )
    parser.add_option('--refRelease',
                      help='Allow to modify the recycling dataset version',
                      dest='refRel',
                      default=None
                      )
    parser.add_option('--wmcontrol',
                      help='Create the workflows for injection to WMAgent. In the WORKING. -wmcontrol init will create the the workflows, -wmcontrol test will dryRun a test, -wmcontrol submit will submit to wmagent',
                      dest='wmcontrol',
                      default=None,
                      )
    parser.add_option('--command',
                      help='provide a way to add additional command to all of the cmsDriver commands in the matrix',
                      dest='command',
                      default=None
                      )
    parser.add_option('--workflow',
                      help='define a workflow to be created or altered from the matrix',
                      action='append',
                      dest='workflow',
                      default=None
                      )
    
    opt,args = parser.parse_args()
    if opt.testList: opt.testList = map(float,opt.testList.split(','))
    if opt.restricted:
        limitedMatrix=[5.1, #FastSim ttbar
                       8, #BH/Cosmic MC
                       25, #MC ttbar
                       4.22, #cosmic data
                       4.291, #hlt data
                       1000, #data+prompt
                       1001, #data+express
                       4.53, #HI data
                       40, #HI MC
                       ]
        if opt.testList:
            opt.testList.extend(limitedMatrix)
        else:
            opt.testList=limitedMatrix
    if opt.useInput: opt.useInput = opt.useInput.split(',')
    if opt.fromScratch: opt.fromScratch = opt.fromScratch.split(',')
    if opt.nThreads: opt.nThreads=int(opt.nThreads)

    # if opt.wmcontrol:
    #     if opt.show:
    #         print 'Not injecting to wmagent in --show mode. Need to run the worklfows.'
    #         sys.exit(-1)
    #     if opt.wmcontrol=='submit' and opt.nThreads==0:
    #         print 'Not injecting to wmagent in -j 0 mode. Need to run the worklfows.'
    #         sys.exit(-1)
    #     if opt.wmcontrol=='init':        opt.nThreads=0

        
    # # some sanity checking:
    # if opt.useInput and opt.useInput != 'all' :
    #     for item in opt.useInput:
    #         if opt.fromScratch and item in opt.fromScratch:
    #             print 'FATAL error: request to run workflow ',item,'from scratch and using input. '
    #             sys.exit(-1)

    # if opt.raw and opt.show: ###prodAgent to be discontinued
    #     ret = showRaw(opt)
    # else:
    #     ret = runSelected(opt)




    mrd = MatrixReader(opt)
    mrd.prepare(opt.useInput, opt.refRel, opt.fromScratch)

    testList = []
    index = 10000
    for gt in gts:
        # print "about to duplicate: " + gt
        wfidtodup = gtmap[gt]
        # add the workflows for the test of the GT (local)
        if wfidtodup == 40:
            index = 40
        duplicateWorkflowForGTTest(mrd, wfidtodup, index, gt, isLocal) 
        if original:
            testList.append(wfidtodup)
        else:
            testList.append(index)
        index = index + 1

    if len(testList) == 0 :
        print "No process selected"
        return 0

    ret = 0
    if show:
        mrd.show([float(x) for x in testList])
        print 'selected items:', testList
    else:
        mRunnerHi = MatrixRunner(mrd.workFlows, nThreads)
        ret = mRunnerHi.runTests(testList)

    return ret


def runGTSelectionNew(gts, gtmap, isLocal, nThreads=4, original=False, show=False, useInput=None) :

    stdList = ['5.2', # SingleMu10 FastSim
               '7',   # Cosmics+RECOCOS+ALCACOS
               '8',   # BeamHalo+RECOCOS+ALCABH
               '25',  # TTbar+RECO2+ALCATT2  STARTUP
               ]
    hiStatList = [
                  '121',   # TTbar_Tauola
                  '123.3', # TTBar FastSim
                   ]

    mrd = MatrixReader()
    mrd.prepare(useInput)

    testList = []
    index = 10000
    for gt in gts:
        # print "about to duplicate: " + gt
        wfidtodup = gtmap[gt]
        # add the workflows for the test of the GT (local)
        if wfidtodup == 40:
            index = 40
        duplicateWorkflowForGTTest(mrd, wfidtodup, index, gt, isLocal) 
        if original:
            testList.append(wfidtodup)
        else:
            testList.append(index)
        index = index + 1

    if len(testList) == 0 :
        print "No process selected"
        return 0

    ret = 0
    if show:
        mrd.show([float(x) for x in testList])
        print 'selected items:', testList
    else:
        mRunnerHi = MatrixRunner(mrd.workFlows, nThreads)
        ret = mRunnerHi.runTests(testList)

    return ret


def runGTSelection(gts, gtmap, isLocal, nThreads=4, original=False, show=False) :

    stdList = ['5.2', # SingleMu10 FastSim
               '7',   # Cosmics+RECOCOS+ALCACOS
               '8',   # BeamHalo+RECOCOS+ALCABH
               '25',  # TTbar+RECO2+ALCATT2  STARTUP
               ]
    hiStatList = [
                  '121',   # TTbar_Tauola
                  '123.3', # TTBar FastSim
                   ]

    mrd = MatrixReader()
    files = ['cmsDriver_standard_hlt.txt', 'cmsDriver_highstats_hlt.txt']
    offset = 0
    for matrixFile in files:
        try:
            mrd.readMatrix(matrixFile, offset=offset)
#            mrd.readMatrix(matrixFile)
        except Exception, e:
            print "ERROR reading file:", matrixFile, str(e)
        offset += 100

    try:
        mrd.createWorkFlows()
    except Exception, e:
        print "ERROR creating workflows :", str(e)


    testList = []
    index = 1000
    for gt in gts:
        # print "about to duplicate: " + gt
        wfidtodup = gtmap[gt]
        # add the workflows for the test of the GT (local)
        duplicateWorkflowForGTTest(mrd, wfidtodup, index, gt, isLocal) 
        if original:
            testList.append(wfidtodup)
        else:
            testList.append(index)
        index = index + 1

    if len(testList) == 0 :
        print "No process selected"
        return 0

    ret = 0
    if show:
        mrd.show([float(x) for x in testList])
        print 'selected items:', testList
    else:
        mRunnerHi = MatrixRunner(mrd.workFlows, nThreads)
        ret = mRunnerHi.runTests(testList)

    return ret


        
# ================================================================================
from ConfigParser import ConfigParser

if __name__ == '__main__':


    from optparse import OptionParser

    
    # set the command line options
    parser = OptionParser()
    parser.add_option("--query", action="store_true",dest="show")
    parser.add_option("--local", action="store_true",dest="local",default=False)
    parser.add_option("--original", action="store_true",dest="original")

    parser.add_option("-i","--useInput", dest="useInputStr",
                     help="recycle input", type="str", metavar="<workflows>")
    
    #parser.add_option("-r", "--release", dest="release",
    #                 help="CMSSW release", type="str", metavar="<release>")
     
     
    (options, args) = parser.parse_args()
    #print "OPTIONS: ", options
    #print "ARGS: ", args
    
    #print options.useInputStr
    useInput = options.useInputStr.split(',')
    #print useInput
    
    CONFIGFILE = 'gtValid.cfg'

    if not os.path.isfile(CONFIGFILE):
        print error("*** Error:") + " cfg file: " + CONFIGFILE + " doesn't exist!"
        sys.exit(1)

    diffconfig = ConfigParser()
    diffconfig.optionxform = str

    print 'Reading configuration file from ',CONFIGFILE
    diffconfig.read(CONFIGFILE)

    globaltagsandWfIds = dict()
    if diffconfig.has_section('Tags'):
        globaltagsandWfIds = dict(diffconfig.items('Tags'))

    print globaltagsandWfIds

    # arguments: list of GTS, might be all
    gts = []
    if 'all' in args:
        gts = globaltagsandWfIds.keys()
    else:
        gts = args
    
    print gts
    #sys.exit(0)

    np=4 # default: four threads
    releasearea = os.environ["CMSSW_BASE"]

    if 'CMSSW_3_6' in releasearea or 'CMSSW_3_7' in  releasearea :
        ret = runGTSelection(gts, globaltagsandWfIds, options.local, np, options.original, options.show)
    elif 'CMSSW_3' in releasearea or 'CMSSW_4' in releasearea or 'CMSSW_5_0' in releasearea or 'CMSSW_5_1' in releasearea:
        ret = runGTSelectionNew(gts, globaltagsandWfIds, options.local, np, options.original, options.show)
    else:
<<<<<<< gtRunTheMatrix.py
        ret = runGTSelectionFrom52(gts, globaltagsandWfIds, options.local, np, options.original, options.show)
=======
        ret = runGTSelectionNew(gts, globaltagsandWfIds, options.local, np, options.original, options.show, useInput)
>>>>>>> 1.11
    #sys.exit(ret)

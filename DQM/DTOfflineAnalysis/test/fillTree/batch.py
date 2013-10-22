#!/bin/env python
#import sys
import imp
import copy
import os
#import shutil
#import pickle
#import math


def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]


def batchScriptCERN( index, remoteDir=''):
   '''prepare the LSF version of the batch script, to run on LSF'''
#   print "INDEX", index
#   print "remotedir", remoteDir
   script = """#!/bin/tcsh
#BSUB -q 8nh
#BSUB -o job_%J.txt
#ulimit -v 3000000
limit
cat /proc/cpuinfo
cat /proc/meminfo
cd $CMSSW_BASE/src
cmsenv
cd -
echo 'Environment:'
echo
env
echo
echo 'Copying' ${LS_SUBCWD} to ${PWD} 
cp -rf $LS_SUBCWD .
echo '...done'
echo
echo Workdir content:
ls -l
echo
cd `find . -type d | grep /`
pwd
echo 'Running at:' `date`
cmsRun run_cfg.py >& log.txt
set cmsRunStatus=$?
echo 'cmsRun done at: ' `date` with exit status: $cmsRunStatus
if ( $cmsRunStatus != 0 ) echo $cmsRunStatus > exitStatus.txt
gzip log.txt
echo
echo 'ls: '
pwd
ls -l
echo
echo 'Sending the job directory back...'
cp *.root *.txt *.gz $LS_SUBCWD
if ( -z DTLocalReco.root ) then
 echo 'Empty file:  DTLocalReco.root'
 if ( -s DTLocalReco.root ) then
   echo Retrying...
   sleep 10
   cp *.root $LS_SUBCWD
 endif
endif
echo 'destination dir: ls: '
cd $LS_SUBCWD
pwd
ls -l 
if ( -s DTLocalReco.root ) then
 root -q -b '${CMSSW_BASE}/src/DQM/DTOfflineAnalysis/test/fillTree/rootFileIntegrity.r(\"DTLocalReco.root\")'
else
 echo moving empty file
 mv DTLocalReco.root DTLocalReco.root.empty
endif

echo '...done at' `date`
exit $cmsRunStatus
""" 
   return script




if __name__ == '__main__':
    cfgFileName = "fillDTTree_rereco.py"
    batchSet=""
    jobName = "Chunk"
    numFiles = 5

    if batchSet != "" :
        os.mkdir(batchSet)
    else :
        batchSet = "."

    handle = open(cfgFileName, 'r')
    cfo = imp.load_source("pycfg", cfgFileName, handle)
    handle.close()

    fullList = copy.deepcopy(cfo.process.source.fileNames)

    fileBlocks =  chunks(fullList,numFiles)
    

    i=0
    for files in fileBlocks :
       jobDir=jobName+"_"+str(i)
       print jobDir
       path = batchSet+"/"+jobDir
       os.mkdir(path)
       cfo.process.source.fileNames = files
       cfo.process.maxEvents.input = -1
       i=i+1
       cfgFile = open(path+'/run_cfg.py','w')
       cfgFile.write( cfo.process.dumpPython() )
       cfgFile.write( '\n' )
       cfgFile.close()

       scriptFile = open(path+'/batchScript.sh','w')
       scriptFile.write( batchScriptCERN( i ) )
       scriptFile.close()

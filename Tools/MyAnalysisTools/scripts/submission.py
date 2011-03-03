#!/usr/bin/env python

import os
import sys
import commands
import shutil
from optparse import OptionParser, Option, OptionValueError

import FWCore.ParameterSet.Config as cms

def createJobSetups(inputCfg, inputDir, outputDir, outputBaseName, JobName, nFilesPerJob, queue):

    JobName += "/"

    submissionArea = os.environ["PWD"] + "/" + JobName


    outputBaseName = outputBaseName + "_" + JobName

    if not os.path.exists(JobName):
        print " directory " + JobName + " doesn't exist: creating it"
        os.mkdir(JobName)


    #shutil.copy(inputCfg, "input_cfg.py")
    shutil.copy(inputCfg, JobName + "input_cfg.py")

    os.chdir(JobName)

    # list the files in the dir
    castorDir_cmd = "rfdir " + inputDir
    castorDir_out = commands.getstatusoutput(castorDir_cmd)
    if castorDir_out[0] != 0:
        print castorDir_out[1]
        sys.exit(1)

    # check the output dir
    outCastorDir_cmd = "rfdir " + outputDir
    outCastorDir_out = commands.getstatusoutput(outCastorDir_cmd)
    if outCastorDir_out[0] != 0:
        print outCastorDir_out[1]
        sys.exit(1)



    castorFileList = []
    #storeDir = inputDir.split("cern.ch/cms")[1]
    storeDir = "rfio://" + inputDir
    for castorFileLine in castorDir_out[1].split("\n"):
        castorFile = castorFileLine.split()[8]
        if "root" in castorFile:

            #print castorFile
            castorFileList.append(storeDir + castorFile)

    print "Input dir: " + inputDir
    print "# fo files: " + str(len(castorFileList))




    from input_cfg import process

    # do the manipulatio on output and input files
    indexPart = 0
    indexTot  = 0
    indexJob = 0
    for inputFile in castorFileList:
        if indexPart == 0:
            if indexTot != 0:
                print "Writing cfg file for job # " + str(indexJob) + "...."
                outputFileName = outputBaseName + "_" + str(indexJob) + ".root"
                process.out.fileName = outputFileName
                # write the previous cfg
                cfgfilename = "expanded_" + str(indexJob) + "_cfg.py"
                # dump it
                expanded = process.dumpPython()
                expandedFile = file(cfgfilename,"w")
                expandedFile.write(expanded)
                expandedFile.close()
                print "Writing submission script for job # " + str(indexJob) + "...."
                scriptname = "SubmissionJob_" +  str(indexJob) + ".csh"
                scriptfile = open(scriptname, 'w')
                scriptfile.write("#!/bin/tcsh\n")
                scriptfile.write("#BSUB -j " + JobName + "\n")
                scriptfile.write("#BSUB -q " + queue + "\n")
                scriptfile.write("setenv runningDir $PWD\n")
                scriptfile.write("cd " +  submissionArea + "\n")
                scriptfile.write("eval `scram runtime -csh`\n")
                scriptfile.write("cp " + cfgfilename + " $runningDir\n")
                scriptfile.write("cd $runningDir\n")
                scriptfile.write("cmsRun " + cfgfilename + "\n")
                scriptfile.write("rfcp " + outputFileName + " " + outputDir + "\n")
                scriptfile.write("rfcp histograms.root " + outputDir + "/histograms_" +  str(indexJob) + ".root\n")
                scriptfile.write("\n")
                scriptfile.close()

                indexJob += 1
            # reset the linst of input files    
            process.source.fileNames = cms.untracked.vstring()

        process.source.fileNames.append(inputFile)
        indexPart+=1
        indexTot+=1
        if indexPart == nFilesPerJob:
            indexPart = 0


if __name__     ==  "__main__":
    # --- set the command line options
    parser = OptionParser()

    parser.add_option("-q", "--queue", dest="queue",
                      help="queue", type="str", metavar="<queue>")
    parser.add_option("-s", "--split", dest="split",
                      help="# files per job", type="int", metavar="<split>", default=100)
    parser.add_option("-c", "--cfg", dest="config",
                      help="configuration file", type="str", metavar="<config>")
    parser.add_option("-i", "--input-dir", dest="inputdir",
                      help="input directory", type="str", metavar="<input dir>")
    parser.add_option("-o", "--output-dir", dest="outputdir",
                      help="output directory", type="str", metavar="<output dir>")
    parser.add_option("-j", "--job-name", dest="jobname",
                      help="job name", type="str", metavar="<job name>")
    parser.add_option("-f", "--file-basename", dest="basename",
                      help="file basename", type="str", metavar="<file basename>")

    parser.add_option("--submit", action="store_true",dest="submit",default=False, help="submit the jobs")


    (options, args) = parser.parse_args()


    if options.submit:
        #
        for job in args:
            if not os.path.exists(job):
                print "Dir: " + job + " doesn't exist!"
            else:
                os.chdir(job)
                fileList = os.listdir(".")
                for filename  in fileList:
                    if "SubmissionJob" in filename:
                        print "Submitting: " + filename + "..."
                        submit_cmd = "bsub " + filename
                        submit_out = commands.getstatusoutput(submit_cmd)
                        print submit_out[1]

    else:

        if options.queue == None:
            print "no queue specified!"
            sys.exit(1)
        if options.config == None:
            print "no cfg specified!"
            sys.exit(1)
        if options.inputdir == None:
            print "no input dir. specified!"
            sys.exit(1)
        if options.outputdir == None:
            print "no output dir. specified!"
            sys.exit(1)
        if options.jobname == None:
            print "no job name specified!"
            sys.exit(1)
        if options.basename == None:
            print "no fine basename specified!"
            sys.exit(1)

        # -----------------------------------------------------------------------
        inputCfg = options.config
        inputDir = options.inputdir
        outputDir = options.outputdir
        outputBaseName = options.basename
        JobName  = options.jobname
        nFilesPerJob = options.split
        queue = options.queue
        # -----------------------------------------------------------------------

        createJobSetups(inputCfg, inputDir, outputDir, outputBaseName, JobName, nFilesPerJob, queue)

sys.exit(0)
    

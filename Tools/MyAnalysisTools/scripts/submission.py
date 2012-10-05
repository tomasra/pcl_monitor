#!/usr/bin/env python

import os
import sys
import commands
import shutil
import time
from optparse import OptionParser, Option, OptionValueError
from ConfigParser import ConfigParser
from Tools.MyAnalysisTools.color_tools import *
import FWCore.ParameterSet.Config as cms


class TaskConfig:
    def __init__(self, taskName, cfgfile):
        self.taskName      = taskName
        self.version       = cfgfile.get('General','selFlag')
        self.configFile    = cfgfile.get('General','configFile')
        if cfgfile.has_option(taskName,'configFile'):
            # override from single task
             self.configFile = cfgfile.get(taskName,'configFile')
        self.filesPerJob   = int(cfgfile.get('General','filesPerJob'))
        self.outputDir     = cfgfile.get('General','outputDirBase') + '/' + self.version  + '/' + taskName
        self.outputFiles  = cfgfile.get('General','outputFiles').split(',')
        self.inputDir      = cfgfile.get(taskName,'inputDir')
        self.queue         = cfgfile.get('General','queue')
        if cfgfile.has_option('General','doJson'):
            self.doJson        = bool(cfgfile.get('General','doJson'))
        self.isProduction  = False
        self.additionalVariables = {}
        for item in cfgfile.items('General'):
            if item[0][0] == '@':
                #print item[0]
                self.additionalVariables[item[0].split("@")[1]] = item[1]
        for item in cfgfile.items(taskName):
            if item[0][0] == '@':
                #print item[0]
                self.additionalVariables[item[0].split("@")[1]] = item[1]
        #print self.additionalVariables

def createJobSetups(inputCfg,
                    inputDir,
                    outputDir,
                    outputFiles,
                    JobName,
                    nFilesPerJob,
                    queue,
                    doJson = False,
                    additionalVars = {}):

    JobName += "/"

    pwd = os.environ["PWD"]

    submissionArea = pwd + "/" + JobName


    if not os.path.exists(JobName):
        print " directory " + JobName + " doesn't exist: creating it"
        os.mkdir(JobName)


    #shutil.copy(inputCfg, "input_cfg.py")
    shutil.copy(inputCfg, JobName + "input_cfg.py")

    if len(additionalVars) != 0:
        print "Setting userdefined additional variables:"
    for variable,value in additionalVars.iteritems():
        globals()[variable] = value
        print "   var: " + str(variable) + " to value: " + str(value)

    print "Input dir: " + inputDir

    os.chdir(submissionArea)
    sys.path.append(submissionArea)
    # list the files in the dir
    castorDir_cmd = "cmsLs " + inputDir
    castorDir_out = commands.getstatusoutput(castorDir_cmd)
    if castorDir_out[0] != 0:
        print castorDir_out[1]
        sys.exit(1)




    # check the output dir
    outCastorDir_cmd = "cmsLs " + outputDir
    outCastorDir_out = commands.getstatusoutput(outCastorDir_cmd)
    if outCastorDir_out[0] != 0:
        print outCastorDir_out[1]
        sys.exit(1)



    inputFileList = []
    for fileLine in castorDir_out[1].split("\n"):
        if 'root' in fileLine:
            fileName = fileLine.split()[4]
            cmsPfn_cmd = 'cmsPfn ' + fileName
            cmsPfn_out = commands.getstatusoutput(cmsPfn_cmd)
            if cmsPfn_out[0] == 0:
                inputFileList.append(cmsPfn_out[1])


    print "# fo files: " + str(len(inputFileList))

    toNFiles = len(inputFileList)
    if len(inputFileList) < nFilesPerJob:
        nFilesPerJob = len(inputFileList)


    # in case we need to generate the JSON files for the input
    inputJson_cmd = "edmLumisInFiles.py --output=input.json "        
    if doJson:
        # make sure that the json is copied
        outputFiles.append('input.json')
        if "JSON_FILE" in additionalVars:
            outputFiles.append('output.json')
            
    #print globals()
    globalsFromCfg = globals()
    execfile("input_cfg.py",globalsFromCfg)
    #from input_cfg import process
    process = globalsFromCfg.get('process')
    process.source.fileNames = cms.untracked.vstring()
    process.maxEvents.input = -1
    # do the manipulatio on output and input files
    indexPart = 0
    indexTot  = 0
    indexJob = 0

    for inputFile in inputFileList:
        process.source.fileNames.append(inputFile)
        indexPart+=1
        indexTot+=1

        if doJson:
            inputJson_cmd += inputFile + ' '

                

        #print inputFile
        if indexPart == nFilesPerJob or indexTot == toNFiles:
            print "Writing cfg file for job # " + str(indexJob) + "...."
            #             outputFileName = outputBaseName + "_" + str(indexJob) + ".root"
            #             outputFileNameTmp =  outputBaseName + ".root"
            #             try:
            #                 process.out.fileName = outputFileNameTmp
            #             except AttributeError:
            #                 print "no output module \"out\" was found..."
            # write the previous cfg
            cfgfilename = "expanded_" + str(indexJob) + "_cfg.py"
            # dump it
            expanded = process.dumpPython()
            expandedFile = file(cfgfilename,"w")
            expandedFile.write(expanded)
            expandedFile.close()

            # zip it
            gzip_cmd = "gzip " + cfgfilename
            gzip_out = commands.getstatusoutput(gzip_cmd)
            if gzip_out[0]:
                print gzip_out[1]
                sys.exit(1)
                
            print "Writing submission script for job # " + str(indexJob) + "...."
            scriptname = "SubmissionJob_" +  str(indexJob) + ".csh"
            scriptfile = open(scriptname, 'w')
            scriptfile.write("#!/bin/tcsh\n")
            scriptfile.write("#BSUB -j " + JobName + "\n")
            scriptfile.write("#BSUB -q " + queue + "\n")
            scriptfile.write("setenv runningDir $PWD\n")
            scriptfile.write("cd " +  submissionArea + "\n")
            # FIXME: get the arch from env
            # scriptfile.write("setenv SCRAM_ARCH slc5_amd64_gcc462 \n")
            scriptfile.write("eval `scram runtime -csh`\n")
            scriptfile.write("cp " + cfgfilename + ".gz $runningDir\n")
            scriptfile.write("cd $runningDir\n")
            scriptfile.write("gunzip " + cfgfilename + ".gz\n")
            scriptfile.write("cmsRun " + cfgfilename + "\n")
            scriptfile.write("set CMSSW_EXIT = $status\n")
            scriptfile.write('echo "--- CMSSW terminated with exit code: $CMSSW_EXIT"\n')
            scriptfile.write("set EXIT = 0\n")
            scriptfile.write("@ EXIT = $EXIT + $CMSSW_EXIT\n")
            if doJson: 
                scriptfile.write('echo "--- Computing input JSON file:"\n')
                scriptfile.write(inputJson_cmd + "\n")
                scriptfile.write("set JSON_EXIT = $status\n")
                scriptfile.write("@ EXIT = $EXIT + $JSON_EXIT\n")                
                scriptfile.write('echo "--- Done with exit code: $JSON_EXIT"\n')
                if 'JSON_FILE' in additionalVars:
                    # than compute the end with the input and write it in the output.json file
                    scriptfile.write('echo "--- Computing output JSON file:"\n')
                    andJson_cmd = "compareJSON.py --and input.json " + str(JSON_FILE) + " output.json"
                    scriptfile.write(andJson_cmd + "\n")
                    scriptfile.write("set JSON_EXIT = $status\n")
                    scriptfile.write("@ EXIT = $EXIT + $JSON_EXIT\n")                
                    scriptfile.write('echo "--- Done with exit code: $JSON_EXIT"\n')
            scriptfile.write('echo "--- Copy output files:"\n')
            for outFileName in outputFiles:
                outFileNameTmp = outFileName
                scriptfile.write('echo "   file: ' + outFileNameTmp + '"\n')
                outFileNameTask = outFileName.split(".")[0]+ '_' +  str(indexJob) + '.' + outFileName.split(".")[1]
                scriptfile.write("cp " + outFileNameTmp + " " + outputDir + '/' + outFileNameTask + "\n")
                scriptfile.write("set RFCP_EXIT = $status\n")
                scriptfile.write("@ EXIT = $EXIT + $RFCP_EXIT\n")
                scriptfile.write('echo "    Done with exit code: $RFCP_EXIT"\n')
            scriptfile.write("echo Exit status: $EXIT\n")
            scriptfile.write("exit $EXIT\n")
            scriptfile.write("\n")
            scriptfile.close()
            os.chmod(scriptname, 0777)

            indexJob += 1
            # reset the list of input files    
            process.source.fileNames = cms.untracked.vstring()
            inputJson_cmd = "edmLumisInFiles.py --output=input.json "        
        
            indexPart = 0

    os.chdir(pwd)

if __name__     ==  "__main__":
    # --- set the command line options
    # description
    usage = '\n'+\
            '   * create Job Configurations from cfg file:\n'+ \
            '     %prog [options] --create --file <conffile>\n\n'+ \
            '   * submit jobs from cfg file:\n'+\
            '     %prog [options] --queue <queue> --submit --file <conffile>\n\n'+\
            '   * check job status:\n'+\
            '     %prog [options] --status --file <conffile>\n\n'+\
            '   * copy the output files of the various tasks in the cfg to a target dir.:\n'+\
            '     %prog [options] --copy --file <conffile> <targetdir>\n\n'

    revision = '$Revision: 1.5 $'
    vnum = revision.lstrip('$')
    vnum = vnum.lstrip('Revision: ')
    vnum = vnum.rstrip(' $')
    
    version="%prog version: " + vnum
    description = "Create one or more GTs starting from the conf file. The destination can be an sqlite or can be modified to write to oracle"
    
    # instantiate the parser
    parser = OptionParser(usage=usage, version=version, description=description)
                                      


    #parser = OptionParser()

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
    parser.add_option("-n", "--n-jobs", dest="njobs",
                      help="# of jobs", type="int", metavar="<# jobs>")



    parser.add_option("--submit", action="store_true",dest="submit",default=False, help="submit the jobs")
    parser.add_option("--copy", action="store_true",dest="copy",default=False, help="copy the output of the jobs from castor to a local dir (argument)")
    parser.add_option("--status", action="store_true",dest="status",default=False, help="check the status of the jobs")
    parser.add_option("--create", action="store_true",dest="create",default=False, help="create the job configuration ")
    
    parser.add_option("--file", dest="file",
                      help="submission config file", type="str", metavar="<file>")


    (options, args) = parser.parse_args()

    taskCfgList = []
    # read the configuration file
    if options.file != None:
        print 'Reading configuration file from ',options.file
        # read a global configuration file
        cfgfile = ConfigParser()
        cfgfile.optionxform = str
        
        cfgfile.read([options.file ])
        
        # get the releases currently managed
        taskToSubmit = cfgfile.get('General','jobsToSubmit').split(',')
        for task in taskToSubmit:
            taskCfg = TaskConfig(task, cfgfile)
            taskCfgList.append(taskCfg)
        print "# tasks: " + str(len(taskCfgList))

    # check the status of the jobs for each particular task
    if options.status:
        for taskCfg in taskCfgList:
            task = taskCfg.taskName
            flag = taskCfg.version
            print "--- Task name: " + blue(task) + "  (" + taskCfg.version + "_" + task + ")"            
            status = ok("OK")
            ls_cmd = "ls " + flag + "_" + task
            ls_out = commands.getstatusoutput(ls_cmd)
            nJobs = 0
            if ls_out[0] == 0:
                lslines = ls_out[1].split("\n")
                for lsline in lslines:
                    if "SubmissionJob" in lsline:
                        nJobs += 1
            else:
                print ls_out[1]
            print "    # of jobs: " + str(nJobs)

            bjobs_cmd = "bjobs -J " + flag + "_" + task
            bjobs_out = commands.getstatusoutput(bjobs_cmd)
            if bjobs_out[0] == 0:
                if not "not found" in bjobs_out[1]:
                    print bjobs_out[1]
            else:
                print bjobs_out[1]
            pending = False
            if len(bjobs_out[1].split("\n")) > 1:
                status = warning("PENDING")
                pending = True

            print "    Output dir: " + taskCfg.outputDir
            rfdir_cmd = "rfdir " + taskCfg.outputDir
            nOutFile = 0
            outCastorDir_out = commands.getstatusoutput(rfdir_cmd)
            if outCastorDir_out[0] == 0:
                castorLines = outCastorDir_out[1].split("\n")
                if len(castorLines) != 0:
                    for castorFileLine in castorLines:
                        if 'cerminar' in castorFileLine and "root" in castorFileLine:
                            print "        - " + castorFileLine.split()[8]
                            nOutFile += 1
            else:
                print outCastorDir_out[1]
            print "    # of output files: " + str(nOutFile)
            if nOutFile != nJobs and not pending:
                status = error("ERROR")
            print "    Status: " + status
        sys.exit(0)

    # copy to the target directory the output files of all the tasks listed in the cfg file
    if options.copy:
        # read the target directory from command line
        targetDir = args[0]
        for taskCfg in taskCfgList:
            task = taskCfg.taskName
            # list the content of the output directory
            rfdir_cmd = "rfdir " + taskCfg.outputDir
            outCastorDir_out = commands.getstatusoutput(rfdir_cmd)
            if outCastorDir_out[0] != 0:
                print outCastorDir_out[1]
                sys.exit(1)
            
            filesToCopy = []
            inputFileList = []
            castorLines = outCastorDir_out[1].split("\n")
            if len(castorLines) != 0:
                for castorFileLine in castorLines:
                    if 'root' in castorFileLine:
                        castorFile = castorFileLine.split()[8]
                        if "root" in castorFile:
                            for filebase in taskCfg.fileBaseName:
                                if filebase in castorFile:
                                    filesToCopy.append(taskCfg.outputDir + '/' +castorFile)
                            
            else:
                print 'dir ' + taskCfg.outputDir + " empty..."

            # do the actual copy
            unique = False
            if len(filesToCopy) == 1:
                unique = True

            

            for filename in filesToCopy:
                fileBaseName = ''
                for namebase in taskCfg.fileBaseName:
                    if namebase in filename:
                        fileBaseName = namebase
                
                cp_cmd = "xrdcp root://castorcms/" + filename + " " + targetDir
                outputFile = ""
                if unique:
                    outputFile = fileBaseName + "_" + task + ".root"
                else:
                    outputFile = fileBaseName + "_" + task + filename.split(fileBaseName)[1]
                cp_cmd += "/" + outputFile
                
                if os.path.exists(targetDir + "/" + outputFile):
                      print "*** Warning, the file: " + targetDir + "/" + outputFile + " already exists!"
                      confirm = raw_input('Overwrite? (y/N)')
                      confirm = confirm.lower() #convert to lowercase
                      if confirm != 'y':
                          continue
                #print cp_cmd
                cp_out = commands.getstatusoutput(cp_cmd)
                print cp_out[1]

        sys.exit(0)
            
    if options.submit:
        #
        pwd = os.environ["PWD"]

        if options.queue == None:
            print "no queue specified!"
            sys.exit(1)

        

        
        if len(args) == 0:
            if options.file == None:
                print "no workflow specified!"
                sys.exit(1)
            else:
                
                # read a global configuration file
                cfgfile = ConfigParser()
                cfgfile.optionxform = str

                print 'Reading configuration file from ',options.file
                cfgfile.read([options.file ])

                # get the releases currently managed
                listOfJobs = cfgfile.get('General','jobsToSubmit').split(',')
                flag = cfgfile.get('General','selFlag')
                for job in listOfJobs:
                    args.append(flag + "_" + job)


        counterSub = 0
        for job in args:
            if not os.path.exists(job):
                print "Dir: " + job + " doesn't exist!"
            else:
                os.chdir(job)
                fileList = os.listdir(".")
                for filename  in fileList:
                    if "SubmissionJob" in filename:
                        print "Submitting: " + filename + "..."
                        submit_cmd = "bsub -q " + options.queue + " -J " + job + " " + filename
                        submit_out = commands.getstatusoutput(submit_cmd)
                        print submit_out[1]
                        time.sleep(10)
                        counterSub += 1
                        if counterSub == 10:
                            print "will wait 50 sec....sorry!"
                            time.sleep(50)
                            counterSub = 0
                os.chdir(pwd)
                

    if options.create:
        # tis creates the various configurations
        for taskCfg in taskCfgList:
            task = taskCfg.taskName
            print "Task: " + blue(task)
            # list the content of the output directory
            mkdir_cmd = "mkdir -p " + taskCfg.outputDir
            print mkdir_cmd
            mkdir_out =  commands.getstatusoutput(mkdir_cmd)
            if mkdir_out[0] != 0:
                print mkdir_out[1]
                #sys.exit(1)
            createJobSetups(taskCfg.configFile,
                            taskCfg.inputDir,
                            taskCfg.outputDir,
                            taskCfg.outputFiles,
                            taskCfg.version + "_" + task,
                            taskCfg.filesPerJob ,
                            taskCfg.queue,
                            taskCfg.doJson,
                            taskCfg.additionalVariables)


            
#     elif options.file != None:
#         # read a global configuration file
#         cfgfile = ConfigParser()
#         cfgfile.optionxform = str

#         print 'Reading configuration file from ',options.file
#         cfgfile.read([options.file ])

#         # get the releases currently managed
#         listOfJobs = cfgfile.get('General','jobsToSubmit').split(',')
#         flag = cfgfile.get('General','selFlag')
#         configFile = cfgfile.get('General','configFile')
#         filesPerJob = int(cfgfile.get('General','filesPerJob'))
#         outputDirBase = cfgfile.get('General','outputDirBase')
#         fileBaseName = cfgfile.get('General','fileBaseName')
#         queue = cfgfile.get('General','queue')

#         for job in listOfJobs:
#             inputDir = cfgfile.get(job,'inputDir')
#             outputDir = outputDirBase + "/" + flag + "/" + job + "/"
#             mkdir_cmd = "rfmkdir -p " + outputDir
#             mkdir_out =  commands.getstatusoutput(mkdir_cmd)
#             print mkdir_out[1]
#             createJobSetups(configFile, inputDir, outputDir, fileBaseName, flag + "_" + job, filesPerJob , queue)
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
    

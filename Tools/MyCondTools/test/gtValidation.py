#!/usr/bin/env python
import os
import sys
from optparse import OptionParser
import commands
from stat import *
from ConfigParser import ConfigParser

from datetime import date
import shutil

username = os.environ["USER"]
userinit = username[0]

# ---- SETUP -----------------------------------------------------------------
# directory where the sqlite of the Global-Tags are created
GTCREATIONAREA = "/afs/cern.ch/user/" + userinit + "/" + username + "/Alca/GlobalTag/CMSSW_3_10_0/src"
# directory where the sqlite of the Global-Tag are stored and read from after creation
GTSQLITESTORE = "/afs/cern.ch/user/" + userinit + "/" + username + "/public/Alca/GlobalTag"
# ----------------------------------------------------------------------------

if __name__     ==  "__main__":
    
    # set the command line options
    parser = OptionParser()
    
    #    parser.add_option("-t", "--globaltag", dest="gt",
    #                      help="Global-Tag", type="str", metavar="<globaltag>")
    parser.add_option("-r", "--release", dest="release",
                      help="CMSSW release", type="str", metavar="<release>")
    parser.add_option("-t", "--type", dest="type",
                      help="type of GT: ideal - startup - mc - data - hlt - cosmics", type="str", metavar="<type>",default="Auto")
    parser.add_option("--force", action="store_true",dest="force",default=False, help="force even if no sqlite found")
    parser.add_option("-f", "--file", dest="file",
                      help="file with tags for addpkg", type="str", metavar="<filename>",default="None")
    parser.add_option("--auto", action="store_true",dest="auto",default=False, help="guess the global-tag type from the name")
    
    (options, args) = parser.parse_args()
    #print "OPTIONS: ", options
    #print "ARGS: ", args


    # create the top level directory
    today = date.today()
    topdirname = str(today)

    swScramArch = os.environ["SCRAM_ARCH"]

    # check that the dir does not yet exist
    releasearea = ''
    try:
        print "Looking for already existing CMSSW area"
        releasearea = os.environ["CMSSW_BASE"]
    except:
        print "no release area found...will create a new one"

        
    if not releasearea == '':
        if not topdirname in releasearea or not options.release in releasearea:
            print "Different release area already set: open a new shell!"
            print releasearea
            sys.exit(1)
        print "Release area found: " + releasearea

    if releasearea == '':
        if not os.path.exists(topdirname):
            print " directory", topdirname," doesn't exist: creating it"
            os.mkdir(topdirname)

        os.chdir(topdirname)
        # print "Now in dir: " + os.getcwd()

        if os.path.exists(options.release):
            print "Release area already existing!"
            releasearea =  os.getcwd() + "/" + options.release
        else:
            # create the CMSSW area
            scramproj = 'export SCRAM_ARCH=' + swScramArch + '; scram project CMSSW ' + options.release
            scramprojOutAndStat = commands.getstatusoutput(scramproj)
            if scramprojOutAndStat[0] != 0:
                print scramprojOutAndStat[1]
                sys.exit(1)
            releasearea =  os.getcwd() + "/" + options.release

    os.chdir(releasearea + '/src/')
    evaloutands = commands.getstatusoutput('export SCRAM_ARCH=' + swScramArch + '; eval `scramv1 runtime -sh`')
    if evaloutands[0] != 0:
        print evaloutands[1]

    # copy the sqlite file in the public if not already there
    for gt in args:
        newsqlite = GTCREATIONAREA+'/'+gt+'.db'
        sqlitefile = GTSQLITESTORE+'/'+gt+'.db'
        if os.path.exists(newsqlite):
            shutil.move(newsqlite, sqlitefile)
            print 'move sql file: ' + newsqlite + ' to ' + GTSQLITESTORE
        else:
            if not os.path.exists(sqlitefile):            
                print '***Error: no sqlite file for GT: ' + gt
                if not options.force:
                    args.remove(gt)
            newsqlite = GTCREATIONAREA+'/'+gt+'.db'
#             if not os.path.exists(newsqlite):
#                 print '***Error: no sqlite file for GT: ' + gt
#                 args.remove(gt) # FIXME: really needed?
#             else:
#                 shutil.move(newsqlite, sqlitefile)
#                 print 'copy file: ' + newsqlite + ' to ' + GTSQLITESTORE

    #print "ARGS: ", args

    if(len(args) == 0):
        print "***Error: no GT found!"
        sys.exit(1)

    
    isOnline = False
    if options.type == 'hlt':
        print "this is HLT"
        isOnline = True

    isMc = False
    if options.type == 'ideal' or options.type == 'startup' or options.type == 'mc' or options.type == 'hi' :
        print 'this is MC'
        isMc = True
    
    # prepare the loadall test
    if not os.path.exists("loadall_from_gt_cfg.py"):
        statandout = commands.getstatusoutput("cp /afs/cern.ch/user/c/cerminar/public/Alca/GlobalTag/loadall_from_gt_cfg.py .")
        if statandout[0] != 0:
            print statandout[1]
            sys.exit(1)
        
    # check if GTTools are already here
    if not os.path.exists('Tools/MyCondTools/'):
        print "addpkg Tools/MyCondTools"
        testGTPart = "cvs co UserCode/cerminar/Tools/MyCondTools/scripts/testGT.py ; mv UserCode/cerminar/Tools/MyCondTools/scripts/testGT.py . ; rm -rf UserCode/"
        outandstat = commands.getstatusoutput('cvs co -d Tools/MyCondTools -r VTOOLS10 UserCode/cerminar/Tools/MyCondTools'+"; "+testGTPart)
        if outandstat[0] != 0:
            print outandstat[1]


    for gt in args:
        if options.auto:
            # determine the type from the GT name
            if "_H_" in gt:
                isOnline = True
                isMc = False
            elif "DESING" in gt or "MC" in gt or "START" in gt:
                isOnline = False
                isMC = True
            elif "GR_R" in gt or "CRFT" in gt or "CRAFT" in gt:
                isOnline = False
                isMc = False
                


        # reaqd from sqlite file
        loadallcommand_local = "cmsRun loadall_from_gt_cfg.py globalTag=" + gt + " connect=sqlite_file:" + GTSQLITESTORE + "/" + gt + ".db"
        if isMc:
            loadallcommand_local = loadallcommand_local + " runNumber=2"
        if isOnline:
            loadallcommand_local = loadallcommand_local + " pfnReplace=frontier://FrontierProd/"

        loadallcommand_local = loadallcommand_local + " >&! loadall_test_" + gt + "_local.out\n"            

        loadallscript_local_name = "test_loadAll_" + gt + "_local.csh"
        loadallscript_local = open(loadallscript_local_name, 'w')
        loadallscript_local.write("#!/bin/tcsh\n")
        loadallscript_local.write("export SCRAM_ARCH=' + swScramArch + '; eval `scram runtime -csh`\n")
        loadallscript_local.write(loadallcommand_local)
        loadallscript_local.write("if($status != 0) then\n")
        loadallscript_local.write('    echo \"*** Failure in loadall_from_gt test! Check the output file: loadall_test_'+gt+'_local.out\"\n')
        loadallscript_local.write('    exit 100\n')
        loadallscript_local.write("endif\n")
        loadallscript_local.close()
        os.chmod(loadallscript_local_name,0755)


        # read from frontier
        loadallcommand_frontier = "cmsRun loadall_from_gt_cfg.py globalTag=" + gt
        if isMc:
            loadallcommand_frontier = loadallcommand_frontier + " runNumber=2"
        if isOnline:
            loadallcommand_frontier = loadallcommand_frontier + " pfnReplace=frontier://FrontierProd/"

        loadallcommand_frontier = loadallcommand_frontier + " >&! loadall_test_" + gt + "_frontier.out\n"            

        loadallscript_frontier_name = "test_loadAll_" + gt + "_frontier.csh"
        loadallscript_frontier = open(loadallscript_frontier_name, 'w')
        loadallscript_frontier.write("#!/bin/tcsh\n")
        loadallscript_frontier.write("export SCRAM_ARCH=' + swScramArch + '; eval `scram runtime -csh`\n")
        loadallscript_frontier.write(loadallcommand_frontier)
        loadallscript_frontier.write("if($status != 0) then\n")
        loadallscript_frontier.write('    echo \"*** Failure in loadall_from_gt test! Check the output file: loadall_test_'+gt+'_frontier.out\"\n')
        loadallscript_frontier.write('    exit 100\n')
        loadallscript_frontier.write("endif\n")
        loadallscript_frontier.close()
        os.chmod(loadallscript_frontier_name,0755)
        
        ## make a dir which will store the results for this GT
        #os.mkdir(gt)
        #os.chdir(gt)
        #print "Now in dir: " + os.getcwd()

    # for older release use the customization file...
    if 'CMSSW_3_7' in  options.release or 'CMSSW_3_6' in  options.release:

        # check if Standard Sequence already exists
        if not os.path.exists('Configuration/StandardSequences/'):
            print "addpkg Configuration/StandardSequences"
            outandstat = commands.getstatusoutput('eval `scramv1 runtime -sh`; addpkg Configuration/StandardSequences')
            if outandstat[0] != 0:
                print outandstat[1]

        # add the custom cfg to read the GT from sqlite
        for gt in args:
            sedcommand = "cat /afs/cern.ch/user/c/cerminar/public/Alca/GlobalTag/customGT.py_template | sed s/TEMPLATEGLOBALTAG/" + gt + "/g > Configuration/StandardSequences/python/customGT_" + gt + ".py"
            outandstat = commands.getstatusoutput(sedcommand)
            if outandstat[0] != 0:
                print outandstat[1]

    # check-out sw tags if addpkg file has been provided
    if not options.file == 'None':
        print "Checkout tags from file: " +  options.file
        outandstat = commands.getstatusoutput('export SCRAM_ARCH=' + swScramArch + '; eval `scramv1 runtime -sh`; addpkg -f ' + options.file + " ; checkdeps -a")
        if outandstat[0] != 0:
            print outandstat[1]


    if not os.path.exists('env.csh'):
        env = open('env.csh', 'w')
        env.write('# source this script\n')
        env.write('setenv SCRAM_ARCH ' + swScramArch + '; eval `scram runtime -csh`\n')
        env.write('scram b -j 4\n')
        env.write('if( $status != 0) then\n')
        env.write('    echo "Compilation Error"\n')
        env.write('    touch compilationError.log\n')
        env.write('endif\n')
        env.write('setenv PYTHONPATH ${PYTHONPATH}:${CMSSW_RELEASE_BASE}/bin/' + swScramArch + '/\n')
        env.write('edmPluginRefresh\n')
        env.write('rehash\n')
        env.close()


    # map between relval process and GT type
    RELVALMAP = dict()
    if 'CMSSW_3_7' in  options.release or 'CMSSW_3_6' in  options.release or 'CMSSW_3_8' in  options.release or 'CMSSW_3_9' in  options.release :
        RELVALMAP['mc'] = '2'
        RELVALMAP['design'] = '2'
        RELVALMAP['ideal'] = '2'
        RELVALMAP['startup'] = '25'
        RELVALMAP['hlt'] = '4.1'
        RELVALMAP['data'] = '4.1'
        RELVALMAP['cosmics'] = '4.2'
        RELVALMAP['hi'] = '40'

    else:
        RELVALMAP['mc'] = '11'
        RELVALMAP['design'] = '11'
        RELVALMAP['ideal'] = '11'
        RELVALMAP['startup'] = '25'
        RELVALMAP['hlt'] = '4.6'
        RELVALMAP['data'] = '4.6'
        RELVALMAP['cosmics'] = '4.2'
        RELVALMAP['hi'] = '40'



    diffconfig = ConfigParser()
    diffconfig.optionxform = str

    CONFIGFILE = 'gtValid.cfg'

    if os.path.isfile(CONFIGFILE):
        # print 'Reading configuration file from ',CONFIGFILE
        diffconfig.read(CONFIGFILE)
    else:
        diffconfig.add_section('Tags')

    for gt in args:
        if options.auto:
            # determine the type from the GT name
            if "_H_" in gt:
                options.type = 'hlt'
            elif "DESIGN" in gt:
                options.type = 'ideal'
            elif "MC" in gt:
                options.type = 'mc'
            elif "STARTHI" in gt:
                options.type = 'hi'
            elif "START" in gt:
                options.type = 'startup'
            elif "GR_R" in gt:
                options.type = 'data'
            elif "CRFT" in gt or "CRAFT" in gt:
                options.type = 'cosmics'
        #print gt + " : " + options.type
        diffconfig.set('Tags', gt, RELVALMAP[options.type])
    
    configfile = open(CONFIGFILE, 'wb')
    #with open("pippo.cfg", 'wb') as configfile:
    diffconfig.write(configfile)

    print "Working dir: " + os.getcwd()

    sys.exit(0)
        

    

#!/usr/bin/env python

import os
import sys
from ConfigParser import ConfigParser
from copy import copy
from optparse import OptionParser, Option, OptionValueError
#import coral
#from CondCore.TagCollection import Node,tagInventory,CommonUtils,entryComment
from operator import itemgetter

# tools for color printout
#from color_tools import *
import datetime
from datetime import date
import commands
import shutil

from Tools.MyCondTools.gt_tools import *

#from gt_tools import *
#from odict import *




def executeCommad(command):
    output = commands.getstatusoutput(command)
    if output[0] != 0:
        print output[1]

    return output


if __name__     ==  "__main__":

    # set the command line options
    parser = OptionParser()

    
    parser.add_option("-s", "--scenario", dest="scenario",
                      help="GT scenario: ideal - mc - startup - data - craft09",
                      type="str", metavar="<scenario>",action="append")
    parser.add_option("-r", "--release", dest="releases",
                      help="CMSSW release", type="str",
                      metavar="<release>",action="append")
    # to substitute a tag or a record you need to specify one of these
    parser.add_option("-t", "--tag", dest="oldtag",
                      help="tag", type="str", metavar="<tag>",default="NONE")

    #    parser.add_option("-t", "--globaltag", dest="gt",
    #                      help="Global-Tag", type="str", metavar="<globaltag>")
    parser.add_option("--nightly", action="store_true",dest="nightly",default=False)

    (options, args) = parser.parse_args()


    config = ConfigParser()
    config.optionxform = str
    config.read(['GT_branches/Common.cfg']) 
    gpnArea = config.get("Common","gpnArea")
    cmsswVersion = config.get("Common","gpnCMSSWVersion")
    gtStore = config.get("Common","GTStoreArea")

    # get the releases currently managed
    swScramArch         = config.get('Common','scramArch')
    passwd              = config.get('Common','Passwd')


    
    GTCREATIONAREA = gpnArea + cmsswVersion + "/src"
    GTVALIDATIONAREA =  config.get("Common","testArea")
    CONFSTORE = gtStore + "Nightly/"


    # 1 - create the conf files for the various GTs
    os.chdir(GTCREATIONAREA)

    gtsByRelease = dict()

    if  'all' in options.scenario:
        options.scenario = ['DESIGN','MC','START','GR_R','START_HI']
    elif 'mc' in options.scenario:
        options.scenario = ['DESIGN','MC','START','START_HI']
        
    cvsstatus = []
    gtchanges = []
    
    for release in options.releases:
        gtNames = []
        gtlistnames = ''
        for scenario in options.scenario:
            cfgfile = "GT_branches/GT_" + release + "_" + scenario + ".cfg"

            confbuild_cmd = "cmsenv; gtConfManager.py --force " + cfgfile
            print confbuild_cmd
            confbuild_out = executeCommad(confbuild_cmd)
            gtchanges.append(confbuild_out[1])

            diffconfig = ConfigParser()
            diffconfig.optionxform = str
            diffconfig.read(cfgfile)
            gtName = diffconfig.get('Common','NewGT')
            gtNameOld = diffconfig.get('Common','OldGT')

            gtNames.append(gtName)
            gtlistnames = gtlistnames + " " + gtName


            # copy the new conf file on the public
            shutil.copy(gtName + ".conf", CONFSTORE + gtName + ".conf")
            # remove the old one
            try:
                os.remove(CONFSTORE + gtNameOld + ".conf")
            except:
                print "No file: " + CONFSTORE + gtNameOld + ".conf was found!"
            cvs_cmd = "cvs status " + cfgfile
            cvs_out = executeCommad(cvs_cmd)
            cvsstatus.append(cvs_out[1])
            

        gtsByRelease[release] = gtNames
        # 2 - produce the sqlite files
        gtcreate_cmd = "cmsenv; gtCreate.py " + gtlistnames
        print gtcreate_cmd
        gtcreate_out = executeCommad(gtcreate_cmd)

        # 3 - create the validation area
        #os.chdir(GTVALIDATIONAREA)

        
        if not options.nightly:
            relType = 'pre,final'
        else:
            relType = "nightly"

        # get the list of available release
        releasesAndArea = getReleaseList(swScramArch, relType)
        #print releases
        maxRel = getLastRelease(releasesAndArea, release)
        releaseVal1 = maxRel[0]


        # get the tag file
        tagfile = GTVALIDATIONAREA + "/RelIntegration/swTags_" + release + ".txt"
        cvstag_cmd = 'ssh lxbuild170 "cd ' + GTVALIDATIONAREA + '/RelIntegration/; cvs update -A swTags_' + release + '.txt"'
        cvstag_out = executeCommad(cvstag_cmd)
        
        today = date.today()
        topdirname = str(today)
        runDir = GTVALIDATIONAREA + '/' + topdirname + '/' + releaseVal1 + '/src/'
        relDir = GTVALIDATIONAREA + '/' + topdirname + '/' + releaseVal1 +'/'
        
        gtvalidation_cmd = 'ssh lxbuild170 "cd ' + GTVALIDATIONAREA + '; gtValidation.py -f ' + tagfile + ' -r ' + releaseVal1 + ' --auto ' + gtlistnames + '"'

        print gtvalidation_cmd
        gtvalidation_out = executeCommad(gtvalidation_cmd)
#         gtvalidation_out = commands.getstatusoutput(gtvalidation_cmd)
#         if gtvalidation_out[0] != 100:
#             print gtvalidation_out[1]

        # 3a - compile and report about the compilatin status
        compile_cmd = 'ssh lxbuild170 "cd ' + runDir + '; source env.csh |& tee compilation.out"'
        compile_out = executeCommad(compile_cmd)

        # check that the compilation was succesfull using the file 'compilationError.log'
        compilationResults = 'Success!\n' 
        if os.path.exists(runDir + 'compilationError.log'):
            print "*** Compilation ERROR: details in " +  runDir + 'compilation.out'
            print compile_out[1]
            compilationResults = "*** Compilation ERROR: details in:\n " +  runDir + 'compilation.out\n'
            
        showtags_cmd = 'ssh lxbuild170 "cd ' + runDir + '; source env.csh; showtags -r "'
        print showtags_cmd 
        showtags_out = executeCommad(showtags_cmd)
        
        # 4 - run_all test
        #os.chdir(runDir)
        runAll_cmd = 'ssh lxbuild170 "cd ' + runDir + '; source env.csh; rehash; gtLoadAll.py --local all"'
        print runAll_cmd
        runAll_out = executeCommad(runAll_cmd)

        # 5 - run the matrix in screen
        runTheMatrix_cmd = 'ssh lxbuild170 "cd ' + runDir + '; source env.csh; rehash; gtRunTheMatrix.py  --local all "'
        print runTheMatrix_cmd
        runTheMatrix_out = executeCommad(runTheMatrix_cmd)
        
        # 6 - build the report
        # read the loadall results
        loadallfile = open(runDir + "/loadAllTest_local.out", "r")
        loadallfilelines = loadallfile.readlines()
        loadallfile.close()
        #print loadallfilelines
        # 7 - send the report

        runmatrixfile = open(runDir + "/runall-report-step123-.log", "r")
        runmatrixfilelines = runmatrixfile.readlines()
        runmatrixfile.close()
        #print runmatrixfilelines
        

        SENDMAIL = "/usr/sbin/sendmail" # sendmail location
    
        p = os.popen("%s -t" % SENDMAIL, "w")
        p.write("To: cms-alca-globaltag@cern.ch\n")
        p.write("Subject: [GT-Nightly] " + releaseVal1 + " GTs: " + gtlistnames + "\n")

        
        p.write("\n") # blank line separating headers from body
        p.write("Nightly build for: " + gtlistnames + "\n")
        p.write("Release: " + releaseVal1 + "\n")
        p.write("Run dir: " + runDir + "\n")

        p.write("\n")
        p.write('--- compilation:\n')
        for tags in showtags_out[1].splitlines():
            if not 'Test Release based on' in tags and not 'Base Release in' in tags and not 'Your Test release' in tags and not 'MyCondTools' in tags:
                p.write(tags + '\n')
        p.write('\n')
        p.write('Status: ' + compilationResults)

        
        p.write("\n")
        p.write('--- GT versioning:\n')
        for cvss in cvsstatus:
            revisionline = ''
            for line in cvss.splitlines():
                if 'File' in line:
                    revisionline = revisionline + line
                    print line
                if 'Working revision' in line:
                    print '    ' + line + '\n'
                    revisionline = revisionline + line
            p.write(revisionline)
            p.write("\n")

        p.write("\n")
        p.write('--- load all:\n')
        #p.write(runAll_out[1])
        for line in loadallfilelines:
            print line.rstrip()
            p.write("  " + line)
        p.write("\n")
        p.write("\n")
        p.write('--- run the matrix:\n')
        for line in runmatrixfilelines:
            print line.rstrip()
            if not 'exit: 0 0 0 0' in line:
                p.write("  " + line)
        p.write("\n")
        p.write('--- GT details:\n')
        for gtchange in gtchanges:
            p.write('\n   ------- \n')
            p.write(gtchange)
            
        p.write('\n\n')


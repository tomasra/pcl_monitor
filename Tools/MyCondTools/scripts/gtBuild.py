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

#from gt_tools import *
#from odict import *


def getLatestRelNames(release):
    #print release
    firstDigi = release[0]
    secondDigi = release.lstrip(release[0]).rstrip('X')
    #print firstDigi + " - " + secondDigi
    scram_cmd = 'scram list -c CMSSW'
    scram_out = commands.getstatusoutput(scram_cmd)
    if scram_out[0] == 0:
        maxThirdDigitsRel = -1
        maxPatchDigitsRel = -1
        maxRel = None
        
        maxThirdDigitsPre = -1
        maxPreDigitsPre = -1
        maxPre = None
        
        maxDate = datetime.datetime(1979,10,06,9,0,0)
        maxNightly = None
            

        # print scram_out[1]

        for line in scram_out[1].splitlines():
            #print "Linea: " + line
            onerel = line.split()[1]
            match = 'CMSSW_' + firstDigi + '_' + secondDigi + '_'
            if match in onerel:
                if "_X_" in onerel:
                    #print 'Nightly: ' + onerel
                    datestring = onerel.lstrip(match+"_X_")
                    datedigits = datestring.split('-')
                    nightlyDate = datetime.datetime(int(datedigits[0]),int(datedigits[1]),int(datedigits[2]),int(datedigits[3].lstrip('0').rstrip('00')),0,0)
                    if nightlyDate > maxDate:
                        maxDate = nightlyDate
                        maxNightly = onerel
                        
                elif "pre" in  onerel:
                    #print "pre: " + onerel
                    digis = onerel.split('_')
                    thirdDigits = int(digis[3])
                    #print thirdDigits
                    if thirdDigits >= maxThirdDigitsPre:
                        maxThirdDigitsPre = thirdDigits
                        if 'pre' in onerel:
                            if len(digis[4].lstrip('pre')) > 2:
                                continue
                            preDigits = int(digis[4].lstrip('pre'))
                            #print ' pre: ' + str(preDigits)
                            if preDigits > maxPreDigitsPre:
                                maxPreDigitsPre = preDigits
                                maxPre = onerel
                        else:
                            maxPre = onerel
                else:
                    #print "rel: " + onerel
                    digis = onerel.split('_')
                    thirdDigits = int(digis[3])
                    #print thirdDigits
                    if thirdDigits >= maxThirdDigitsRel:
                        #print 'A'
                        maxThirdDigitsRel = thirdDigits
                        if 'patch' in onerel:
                            patchDigits = int(digis[4].lstrip('patch'))
                            #print ' patch: ' + str(patchDigits)
                            if patchDigits > maxPatchDigitsRel:
                                maxPatchDigitsRel = patchDigits
                                maxRel = onerel
                        else:
                            maxRel = onerel

        if maxRel != None:
            print "Max rel: " + maxRel
        else:
            print "Max pre: " + maxPre
        print "Max Nightly: " + maxNightly

        return [maxRel, maxPre, maxNightly]


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


    GTCREATIONAREA = "/afs/cern.ch/user/c/cerminar/Alca/GlobalTag/CMSSW_3_5_4/src"
    GTVALIDATIONAREA = "/build/cerminar/GlobalTag/Nightly"



    # 1 - create the conf files for the various GTs
    os.chdir(GTCREATIONAREA)

    gtsByRelease = dict()

    if  'all' in options.scenario:
        options.scenario = ['DESIGN','MC','START','GR_R','CRAFT09']

    cvsstatus = []
    
    for release in options.releases:
        gtNames = []
        gtlistnames = ''
        for scenario in options.scenario:
            cfgfile = "GT_branches/GT_" + release + "_" + scenario + ".cfg"
            gtName = scenario + release + "_T"
            gtNames.append(gtName)
            gtlistnames = gtlistnames + " " + gtName
            confbuild_cmd = "cmsenv; gtConfManager.py --force -t " + gtName + " " + cfgfile
            print confbuild_cmd
            confbuild_out = commands.getstatusoutput(confbuild_cmd)
            if confbuild_out[0] != 0:
                print confbuild_out[1]
            cvs_cmd = "cvs status " + cfgfile
            cvs_out = commands.getstatusoutput(cvs_cmd)
            if cvs_out[0] != 0:
                print cvs_out[1]
            cvsstatus.append(cvs_out[1])
            

        gtsByRelease[release] = gtNames
        # 2 - produce the sqlite files
        gtcreate_cmd = "cmsenv; gtCreate.py " + gtlistnames
        print gtcreate_cmd
        gtcreate_out = commands.getstatusoutput(gtcreate_cmd)
        if gtcreate_out[0] != 0:
            print gtcreate_out[1]

        # 3 - create the validation area
        #os.chdir(GTVALIDATIONAREA)
        latestRels = getLatestRelNames(release)

        # build area for last nightly and for last pre (or release)
        releaseVal1 = ''
        if not options.nightly:
            if latestRels[0] != None:
                releaseVal1 = latestRels[0]
            else:
                releaseVal1 = latestRels[1]
        else:
            releaseVal1 = latestRels[2]

        gtvalidation_cmd = "ssh lxbuild150 \" cd " + GTVALIDATIONAREA + "; gtValidation.py -r " + releaseVal1 + " --auto " + gtlistnames + "\""

        print gtvalidation_cmd
        gtvalidation_out = commands.getstatusoutput(gtvalidation_cmd)
        if gtvalidation_out[0] != 100:
            print gtvalidation_out[1]
        
        # 4 - run_all test
        today = date.today()
        topdirname = str(today)
        runDir = GTVALIDATIONAREA + '/' + topdirname + '/' + releaseVal1 + '/src/'
        #os.chdir(runDir)
        runAll_cmd = 'ssh lxbuild150 \" cd ' + runDir + '; source env.csh; rehash; gtLoadAll.py --local all \"'
        print runAll_cmd
        runAll_out = commands.getstatusoutput(runAll_cmd)
        if runAll_out[0] != 0:
            print runAll_out[1]

        # 5 - run the matrix in screen
        runTheMatrix_cmd = 'ssh lxbuild150 \" cd ' + runDir + '; source env.csh; rehash; gtRunTheMatrix.py --local all \"'
        print runTheMatrix_cmd
        runTheMatrix_out = commands.getstatusoutput(runTheMatrix_cmd)
        if runTheMatrix_out[0] != 0:
            print runTheMatrix_out[1]
        
        # 6 - build the report
        # read the loadall results
        loadallfile = open(runDir + "/loadAllTest_local.out", "r")
        loadallfilelines = loadallfile.readlines()
        loadallfile.close()
        print loadallfilelines
        # 7 - send the report

        runmatrixfile = open(runDir + "/runall-report-step123-.log", "r")
        runmatrixfilelines = runmatrixfile.readlines()
        runmatrixfile.close()
        print runmatrixfilelines
        

        SENDMAIL = "/usr/sbin/sendmail" # sendmail location
    
        p = os.popen("%s -t" % SENDMAIL, "w")
        p.write("To: gianluca.cerminara@cern.ch\n")
        p.write("Subject: [GT-Nightly] " + releaseVal1 + " GTs: " + gtlistnames + "\n")

        
        p.write("\n") # blank line separating headers from body
        p.write("Nightly build for: " + gtlistnames + "\n")
        p.write("Release: " + releaseVal1 + "\n")
        p.write("Run dir: " + runDir + "\n")

        p.write("\n")
        p.write('--- versioning:\n')
        for cvss in cvsstatus:
            p.write(cvss)
            p.write("\n")

        p.write("\n")
        p.write('--- load all:\n')
        #p.write(runAll_out[1])
        for line in loadallfilelines:
            print line
            p.write("  " + line)
        p.write("\n")
        p.write("\n")
        p.write('--- run the matrix:\n')
        for line in runmatrixfilelines:
            print line
            p.write("  " + line)
        p.write("\n")
        p.write('--- details:\n')
        p.write(gtvalidation_out[1])
        p.write('\n\n')


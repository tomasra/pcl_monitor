#!/bin/tcsh

source /afs/cern.ch/user/a/alcaprod/scripts/gtEnv.csh

cd  ${GT_DIR}/${GT_CMSSW_VERSION}/src
cmsenv
generateDoc.py
cd /afs/cern.ch/user/a/alcaprod/www/GlobalTag/wiki-doc
cvs update -Ad > /dev/null


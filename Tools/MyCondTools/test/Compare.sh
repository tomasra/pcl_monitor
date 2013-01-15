#!/bin/tcsh

source /afs/cern.ch/user/a/alcaprod/scripts/gtEnv.csh

cd  ${GT_DIR}/${GT_CMSSW_VERSION}/src
cmsenv;
# setenv SCRAM_ARCH slc5_amd64_gcc462
# export SCRAM_ARCH=slc5_amd64_gcc462
/afs/cern.ch/user/a/alcaprod/public/Compare.py "GR_P_V40" "GR_R_52_V8" "/afs/cern.ch/user/a/alcaprod/www/GTComparisons/GTPromptVsGTOffline/GR_P_V40_lastIOVs_previous.html"
/afs/cern.ch/user/a/alcaprod/public/Compare.py "GR_E_V33" "GR_R_52_V8" "/afs/cern.ch/user/a/alcaprod/www/GTComparisons/GTPromptVsGTOffline/GR_E_V33_lastIOVs_previous.html"

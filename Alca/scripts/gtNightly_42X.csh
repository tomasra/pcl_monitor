#!/bin/tcsh

source /afs/cern.ch/user/a/alcaprod/scripts/gtEnv.csh

cd  ${GT_DIR}/${GT_CMSSW_VERSION}/src
cmsenv;
gtBuild.py -r 42X -s all  --nightly



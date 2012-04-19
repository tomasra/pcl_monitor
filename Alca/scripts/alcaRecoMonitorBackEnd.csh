#!/bin/tcsh
#set echo
source /afs/cern.ch/user/a/alcaprod/scripts/gtEnv.csh

cd  ${GT_DIR}/${GT_CMSSW_VERSION}/src
cmsenv
setenv PYTHONPATH ${PYTHONPATH}:/afs/cern.ch/sw/lcg/external/pytools/1.4_python2.6/x86_64-slc5-gcc43-opt/lib/python2.6/site-packages/
alcaRecoMonitor.py




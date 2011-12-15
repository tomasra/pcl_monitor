#!/bin/tcsh

if($#argv == 0) then
    echo "Error: missing username"
    exit
endif

source /afs/cern.ch/user/a/alcaprod/scripts/gtEnv.csh $1

set GPNDIR=${GT_DIR}/${GT_CMSSW_VERSION}/src
set CMSDIR=${GT_P5_DIR}/${GT_P5_CMSSW_VERSION}/src

rsync -uv ${GPNDIR}/*.conf $1@cmsusrslc50:${CMSDIR}/


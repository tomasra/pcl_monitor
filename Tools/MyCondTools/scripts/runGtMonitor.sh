!/bin/tcsh

source /afs/cern.ch/user/a/alcaprod/scripts/gtEnv.csh

cd  ${GT_DIR}/${GT_CMSSW_VERSION}/src
cmsenv;
# setenv SCRAM_ARCH slc5_amd64_gcc462

# Run the monitoring
/afs/cern.ch/user/a/alcaprod/public/gtMonitor.py GR_H_V29
/afs/cern.ch/user/a/alcaprod/public/gtMonitor.py GR_E_V25
/afs/cern.ch/user/a/alcaprod/public/gtMonitor.py GR_P_V32
/afs/cern.ch/user/a/alcaprod/public/gtMonitor.py GR_R_52_V7

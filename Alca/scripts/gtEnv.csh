#
# source this file to setup the environment for the GT management
#
# settings for Area in the GPN



setenv GT_DIR /afs/cern.ch/user/a/alcaprod/Alca/GlobalTag/
setenv GT_CMSSW_VERSION CMSSW_4_4_2_patch8

# settings for area in the P5 network

setenv GT_P5_DIR /nfshome0/demattia/Alca/GlobalTag/
if($#argv == 1) then
    setenv GT_P5_DIR /nfshome0/$1/Alca/GlobalTag/
endif
setenv GT_P5_CMSSW_VERSION CMSSW_4_4_2

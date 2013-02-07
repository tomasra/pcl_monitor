#!/bin/csh

# Usage example: ssh -Y lxbuild170 ./runTheTest.sh CMSSW_5_3 mc START53_V17

if ( "$#argv" < 3 ) then
    echo "The required arguments are (in this order): CMSSW_RELEASE, GT_TYPE, GTNAME, local"
    echo "For the release, the script will find the most recent one matching the given name."
    echo "The last optional input (local) specifies if the test is to be ran on a local sqlite file or from the db. If no value is passed the test runs on the db"
    echo "Usage example: ssh -Y lxbuild170 ./runTheTest.sh CMSSW_5_3 mc START53_V17 local"
    echo "Usage example: ssh -Y lxbuild170 ./runTheTest.sh CMSSW_5_3 mc START53_V17"
    exit
endif
if ( "$#argv" > 3 && "$4" !~ "local" ) then
	echo "Error: argument 4 can be local or empty. Received: $4"
    exit
endif

set CMSSW_RELEASE=$1
set GT_TYPE=$2
set GT_NAME=$3

if ($CMSSW_RELEASE =~ {CMSSW_6_1,CMSSW_6_2}) then
    setenv SCRAM_ARCH slc5_amd64_gcc472
endif

echo "Running the test for:"
echo "CMSSW release : ${CMSSW_RELEASE}"
echo "GT type : ${GT_TYPE}"
echo "GT name : ${GT_NAME}"

set BASEDIR=/build/alcaprod/GTValidation
cd ${BASEDIR}

# Take the last one (might fail in some cases. In that case, please fix the script)
set CMSSW_VERSION=`scramv1 list CMSSW | grep ${CMSSW_RELEASE} | sort | sed 's/ *$//g' | tr " " "\n" | tail -1`

# Uncomment this to force using the release name passed as argument
# set CMSSW_VERSION=${CMSSW_RELEASE}

echo "Using CMSSW : ${CMSSW_VERSION}"
set RELEASE=`gtValidation.py -r ${CMSSW_VERSION} -t ${GT_TYPE} ${GT_NAME}`

set DIR=${BASEDIR}/`date +"%Y-%m-%d"`/${CMSSW_VERSION}/src

echo $DIR

cd $DIR

cmsenv
source env.csh

if ( "$#argv" > 3 ) then
    echo "Running test on sqlite file"
    gtLoadAll.py --local all
    nohup python testGT.py ${GT_NAME} local >&! log.txt &
else
    echo "Running test on db"
    gtLoadAll.py all
    nohup python testGT.py ${GT_NAME} >&! log.txt &
endif

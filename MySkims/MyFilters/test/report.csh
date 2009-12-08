#!/bin/tcsh

set CRAB_TASK_DIR=$1

set DATASET=`grep -e "CMSSW.datasetpath" ${CRAB_TASK_DIR}/log/crab.log | awk '{ print $3 }'`
set RUNN=`grep -e "CMSSW.runselection" ${CRAB_TASK_DIR}/log/crab.log | awk '{ print $3 }'`
set OUTPUTDIR=`grep -e "USER.user_remote_dir" ${CRAB_TASK_DIR}/log/crab.log | awk '{ print $3 }'`


set NPASS=`grep -e "TrigReport Events total" ${CRAB_TASK_DIR}/res/CMSSW_*.stdout | awk '{ sum= sum + $8  } END {print sum}'`

set NTOTAL=`grep -e "TrigReport Events total" ${CRAB_TASK_DIR}/res/CMSSW_*.stdout | awk '{ sum= sum + $11  } END {print sum}'`



echo "--- Report crab task: $CRAB_TASK_DIR"
echo "    Dataset: ${DATASET}"
echo "    Run: ${RUNN}"
echo "    # passed events: $NPASS / $NTOTAL"
echo "    Output dir: /castor/cern.ch/${OUTPUTDIR}"

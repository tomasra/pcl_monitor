#!/bin/tcsh

source /afs/cern.ch/user/a/alcaprod/scripts/gtEnv.csh

cd  ${GT_DIR}/${GT_CMSSW_VERSION}/src
cmsenv
set MESSAGE=`pclStatusMonitor.py -H cms-alcadb.web.cern.ch -p 80 -u/cms-alcadb/Monitoring/PCLTier0Workflow/status.json -s PCLMonitor`

#echo $MESSAGE | /usr/sbin/sendmail -s "[PCL-Monitor] Status message" gianluca.cerminara@cern.ch

echo $MESSAGE | /bin/mail -s "[PCL-Monitor] Status message" cms-alca-globaltag@cern.ch

# cat <<EOF | /usr/lib/sendmail cms-alca-globaltag@cern.ch
# Subject: [PCL-Monitor] Status message
# $MESSAGE
# EOF


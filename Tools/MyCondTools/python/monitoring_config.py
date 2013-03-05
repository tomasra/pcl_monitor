import ConfigParser as ConfigParser



# --------------------------------------------------------------------------------
# configuration

# read a global configuration file
cfgfile = ConfigParser.ConfigParser()
cfgfile.optionxform = str

CONFIGFILE = "GT_branches/pclMonitoring.cfg"
print 'Reading configuration file from ',CONFIGFILE
cfgfile.read([ CONFIGFILE ])


runInfoConnect              = cfgfile.get('Common','runInfoConnect')
runInfoTag_stop             = cfgfile.get('Common','runInfoTag_stop')
runInfoTag_start            = cfgfile.get('Common','runInfoTag_start')

tier0DasSrc                 = cfgfile.get('Common','tier0DasSrc')
passwdfile                  = cfgfile.get('Common','passwdfile')



taskName                    = cfgfile.get('PCLMonitor','taskName')
promptCalibDir              = cfgfile.get('PCLMonitor','promptCalibDir')
weburl                      = cfgfile.get('PCLMonitor','weburl')
webArea                     = cfgfile.get('PCLMonitor','webArea')
tagLumi                     = cfgfile.get('PCLMonitor','tagBSLumi')
tagRun                      = cfgfile.get('PCLMonitor','tagBSRun')
connectOracle               = cfgfile.get('PCLMonitor','connectBSOracle')
tagRunOracle                = cfgfile.get('PCLMonitor','tagBSRunOracle')
tagLumiOracle               = cfgfile.get('PCLMonitor','tagBSLumiOracle')
cacheFileName               = cfgfile.get('PCLMonitor','cacheFileName')
rrDatasetName               = cfgfile.get('PCLMonitor','rrDatasetName')
# FIXME: the run-types can be specialized "by tag"
rrRunClassName              = cfgfile.get('PCLMonitor','rrRunClassName')
firstRunToMonitor           = int(cfgfile.get('PCLMonitor','firstRunToMonitor'))

pclTasks                    = cfgfile.get('PCLMonitor','pclTasks').split(',')
refreshDays                 = int(cfgfile.get('PCLMonitor','daysToCheck'))

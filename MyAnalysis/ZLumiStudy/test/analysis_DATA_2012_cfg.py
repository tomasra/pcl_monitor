
# Get absolute path
import os
PyFilePath = os.environ['CMSSW_BASE'] + "/src/MyAnalysis/ZLumiStudy/test/"

### ----------------------------------------------------------------------
### Standard sequence
### ----------------------------------------------------------------------

IsMC = False
LEPTON_SETUP = 2012
PD = "DoubleMu"

execfile(PyFilePath + "analysis_cfg.py")


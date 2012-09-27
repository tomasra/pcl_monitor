### ----------------------------------------------------------------------
###
### Example analayzer
###
###----------------------------------------------------------------------


try:
    IsMC
except NameError:
    IsMC = False

try:
    LEPTON_SETUP
except NameError:
    LEPTON_SETUP = 2012 # define the set of effective areas, rho corrections, etc.

try:
    PD
except NameError:
    PD = "DoubleMu"             # "" for MC, "DoubleEle", "DoubleMu", or "MuEG" for data 

try:
    MCFILTER
except NameError:
    MCFILTER = ""


# Get absolute path
import os
PyFilePath = os.environ['CMSSW_BASE'] + "/src/MyAnalysis/ZLumiStudy/test/"

### ----------------------------------------------------------------------
### Standard sequence
### ----------------------------------------------------------------------

#execfile(PyFilePath + "MasterPy/ZZ4lAnalysisPRL2011.py")         # 2011 reference analysis
execfile(PyFilePath + "MasterPy/ZLumiStudyMaster.py")         # 2012 reference analysis


### ----------------------------------------------------------------------
### Replace parameters
### ----------------------------------------------------------------------
process.source.fileNames = cms.untracked.vstring(

#        'root://cmsphys05//data/b/botta/V5_2_0/cmgTuple_H120Fall11_noSmearing.root' #Fall11 H120 for May, 21 synch exercise
#        'root://cmsphys05//data/b/botta/V5_4_0/cmgTuple_H120Fall11_noSmearing.root' #Fall11 H120 for FSR synch
#         'root://cmsphys05//data/b/botta/V5_4_0/cmgTuple_H126Summer12.root' #Summer12 H126 for FSR synch
         '/store/cmst3/user/cmgtools/CMG/DoubleMu/Run2012A-13Jul2012-v1/AOD/V5_B/PAT_CMG_V5_7_0/cmgTuple_94.root'
    )


# from CMGTools.Production.datasetToSource import *
# process.source = datasetToSource(
#    'cmgtools',
#    '/GluGluToHToZZTo4L_M-120_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM/V5/PAT_CMG_V5_2_0/',
#    'patTuple.*.root'
#    )

process.maxEvents.input = -1
#process.options.wantSummary = False


#Add my own cuts
#process.EEMMCand.flags +=
# SIPcut = cms.string("userFloat('SIP4')<4.")


### ----------------------------------------------------------------------
### Output root file (monitoring histograms)
### ----------------------------------------------------------------------
process.TFileService=cms.Service('TFileService',
                                fileName=cms.string('ZLumiStudy.root')
                                )



### ----------------------------------------------------------------------
### Analyzer for Trees
### ----------------------------------------------------------------------

TreeSetup = cms.EDAnalyzer("ZTreeMaker",
                                   channel = cms.untracked.string('aChannel'),
                                   CandCollection = cms.untracked.string('aCand'),
                                   fileName = cms.untracked.string('candTree'),
                                   isMC = cms.untracked.bool(IsMC),
                                   sampleType = cms.int32(SAMPLE_TYPE),
                                   setup = cms.int32(LEPTON_SETUP),
                                   skimPaths = cms.vstring(SkimPaths),
                                   PD = cms.string(PD),
                                   MCFilterPath = cms.string(MCFILTER),
                                   skipEmptyEvents = cms.bool(True),
                                   )

process.Z2muTree = TreeSetup.clone()
process.Z2muTree.channel = 'MM'
process.Z2muTree.CandCollection = 'MMCand'


process.trees = cms.EndPath( process.Z2muTree)


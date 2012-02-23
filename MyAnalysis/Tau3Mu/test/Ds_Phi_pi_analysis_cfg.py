import FWCore.ParameterSet.Config as cms

process = cms.Process('GenLevel')


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("DsPhiPi_Analysis.root"),
                                   closeFileFast = cms.untracked.bool(True)
                                   )


process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.GlobalTag.globaltag = 'START44_V10::All'

# Source
process.source = cms.Source("PoolSource",
                          fileNames = cms.untracked.vstring(
    "/store/data/Run2011B/MuOnia/AOD/PromptReco-v1/000/179/452/1CC70987-AFFE-E011-A5D9-001D09F24D8A.root",
    "/store/data/Run2011B/MuOnia/AOD/PromptReco-v1/000/179/434/A823EE1A-35FF-E011-9CDD-BCAEC518FF65.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_000.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_001.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_002.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_003.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_004.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_005.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_006.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_007.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_008.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_009.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_010.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_011.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_012.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_013.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_014.root",
    "file:/gpfs/gpfsddn/cms/user/fiori//Tau3Mu_Data/DsTau3Mu_015.root"
    )
)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(100))

process.ana = cms.EDAnalyzer('Tau3MuAnalysis')

process.analysisPath = cms.Path(process.ana)

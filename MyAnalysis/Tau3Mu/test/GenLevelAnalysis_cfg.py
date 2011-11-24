import FWCore.ParameterSet.Config as cms

process = cms.Process('GenLevel')


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("GenLevelAnalysis.root"),
                                   closeFileFast = cms.untracked.bool(True)
                                   )

process.muonParticlesInAcc = cms.EDFilter("GenParticleSelector",
                                     filter = cms.bool(False),
                                     src = cms.InputTag("genParticles"),
                                     cut = cms.string('pt > 1. && abs(pdgId) == 13 && abs(eta) < 2.4'),
                                     stableOnly = cms.bool(True)
 )


process.threeMuonFilter = cms.EDFilter("CandViewCountFilter",
                                       src = cms.InputTag("muonParticlesInAcc"),
                                       minNumber = cms.uint32(3))





# Source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_000.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_001.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_002.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_003.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_004.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_005.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_006.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_007.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_008.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_009.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_010.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_011.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_012.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_013.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_014.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_015.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_016.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_017.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_018.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_019.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_020.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_021.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_022.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_023.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_024.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_025.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_026.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_027.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_028.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_029.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_030.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_031.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_032.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_033.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_034.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_035.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_036.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_037.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_038.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_039.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_040.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_041.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_042.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_043.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_044.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_045.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_046.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_047.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_048.root',
'root://castorcms//castor/cern.ch/user/g/guiducci/Tau3Mu/DsTau3Mu_GEN_FASTSIM_HLT_PU/DsTau3Mu_049.root',
)
                            )
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))



process.genLevelAnalysis = cms.EDAnalyzer('GenLevelAnalysis')

process.analysisPath = cms.Path(process.muonParticlesInAcc + process.threeMuonFilter + process.genLevelAnalysis)

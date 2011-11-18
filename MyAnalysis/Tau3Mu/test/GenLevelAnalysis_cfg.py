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
                            fileNames = cms.untracked.vstring(#'file:/afs/cern.ch/user/g/guiducci/scratch0/tau3mu/GENsamples/MinBias_TuneZ2_7TeV_pythia6_DsTau3Mu_GEN_1.root'
"file:/afs/cern.ch/user/g/guiducci/scratch0/tau3mu/GENsamples/MinBias_TuneZ2_Ds-Tau-3Mu.root")
                            )
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))



process.genLevelAnalysis = cms.EDAnalyzer('GenLevelAnalysis')

process.analysisPath = cms.Path(process.muonParticlesInAcc + process.threeMuonFilter + process.genLevelAnalysis)

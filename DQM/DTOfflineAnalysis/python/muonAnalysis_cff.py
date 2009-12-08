import FWCore.ParameterSet.Config as cms


muonAnalysis = cms.EDAnalyzer("MuonAnalysis",
                              debug = cms.untracked.bool(False),
                              dtDigiLabel = cms.untracked.InputTag("muonDTDigis"),
                              dtRecHitLabel = cms.untracked.InputTag("dt1DRecHits"),
                              dtRecHit4DLabel = cms.untracked.InputTag("dt4DSegments"),
                              muonLabel =  cms.untracked.InputTag("muons"),
                              rootFileName = cms.untracked.string("pippo.root"))



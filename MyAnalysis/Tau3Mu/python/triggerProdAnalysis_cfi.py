import FWCore.ParameterSet.Config as cms

triggerProdAnalysis = cms.EDAnalyzer("TriggerProdAnalysis",
                                     l1ExtraParticles             = cms.untracked.InputTag("l1extraParticles"),
                                     TriggerResults               = cms.untracked.InputTag("TriggerResults"),
                                     diMuDisplacedVertex          = cms.untracked.InputTag("hltDisplacedmumuVtxProducerTauTo2Mu"),
                                     diMuDisplacedVertexFiltLabel = cms.untracked.InputTag("hltDisplacedmumuFilterTauTo2Mu"),
                                     beamSpot                     = cms.untracked.InputTag("offlineBeamSpot"),
                                     l3MuonCands                  = cms.untracked.InputTag("hltL3MuonCandidates"),
                                     mmkVtxLabel                  = cms.untracked.InputTag("hltTau2MuTkMuMuTkFilter"),
                                     debug                        = cms.untracked.bool(False)
                                     )

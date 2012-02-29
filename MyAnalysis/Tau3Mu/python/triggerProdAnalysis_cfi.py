import FWCore.ParameterSet.Config as cms

triggerProdAnalysis = cms.EDAnalyzer("TriggerProdAnalysis",
                                     l1ExtraParticles             = cms.untracked.InputTag("l1extraParticles",""),
                                     TriggerResults               = cms.untracked.InputTag("TriggerResults", "", "HLT"),
                                     diMuDisplacedVertex          = cms.untracked.InputTag("TriggerResults", "", "HLT"),
                                     diMuDisplacedVertexFiltLabel = cms.untracked.InputTag("hltDisplacedmumuVtxProducerTauTo2Mu"),
                                     beamSpot                     = cms.untracked.InputTag("hltDisplacedmumuFilterTauTo2Mu::reHLT"),
                                     l3MuonCands                  = cms.untracked.InputTag("hltL3MuonCandidates::reHLT"),
                                     mmkVtxLabel                  = cms.untracked.InputTag("hltTau2MuTkMuMuTkFilter::HLT"),
                                     debug                        = cms.untracked.bool(False)
                                     )

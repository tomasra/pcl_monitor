import FWCore.ParameterSet.Config as cms

bxNumberFilter = cms.EDFilter("BxNumberFilter",
                              #inputLabel = cms.InputTag("source"),
                              goldenBXIds = cms.vint32(901,832),
                              range = cms.untracked.uint32(1),
                              debug = cms.untracked.uint32(1))

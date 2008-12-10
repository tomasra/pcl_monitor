import FWCore.ParameterSet.Config as cms

bxDistanceFilter = cms.EDFilter("BXDistanceFilter",
                                inputLabel = cms.untracked.InputTag("source"),
                                maxDistance = cms.untracked.uint32(10),
                                debug = cms.untracked.uint32(1),
                                listInstance = cms.untracked.string("All"))

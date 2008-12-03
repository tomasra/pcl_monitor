import FWCore.ParameterSet.Config as cms

eventListProducer = cms.EDProducer("EventListProducer",
                                   maxDistance = cms.untracked.uint32(10))

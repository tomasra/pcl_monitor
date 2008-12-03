import FWCore.ParameterSet.Config as cms

dtOfflineOccupancy = cms.EDAnalyzer("DTOfflineOccupancy",
                                    # the label to retrieve the collections from the event
                                    dtDigiLabel = cms.InputTag("dtunpacker"),
                                    dtRecHitLabel = cms.InputTag("dt1DRecHits"),
                                    dtRecHit4DLabel = cms.InputTag("dt4DSegments"),
                                    rootFileName = cms.untracked.string("DTOfflineOccupancy.root"),
                                    mode = cms.untracked.string("")
                                    )



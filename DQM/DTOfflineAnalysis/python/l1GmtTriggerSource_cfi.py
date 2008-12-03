import FWCore.ParameterSet.Config as cms

l1GmtTriggerSource = cms.EDAnalyzer("L1GmtTriggerSource",
                                    inputLabel = cms.InputTag("source"),             
                                    GMTInputTag = cms.InputTag("gtDigis"),
                                    debug = cms.untracked.bool(False)
                                    )

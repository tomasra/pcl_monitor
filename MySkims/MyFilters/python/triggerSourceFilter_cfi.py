import FWCore.ParameterSet.Config as cms

triggerSourceFilter = cms.EDFilter("TriggerSourceFilter",
                                   GMTInputTag = cms.InputTag("gtDigis"),
                                   # Trigger source:
                                   # 1 -> DT
                                   # 2 -> CSC
                                   # 3 -> CSC Halo
                                   # 4 -> RPC barrel
                                   # 5 -> RPC endcap
                                   triggerSource = cms.untracked.int32(1),
                                   debug = cms.untracked.bool(False)
                                   )




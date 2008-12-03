import FWCore.ParameterSet.Config as cms

triggerFilter = cms.EDFilter("TriggerPathFilter",
                             triggerResults = cms.InputTag("TriggerResults::FU"),
                             l1GtData = cms.InputTag("hltGtDigis"),
                             l1Bits = cms.vint32(1, 2, 54, 55),
                             hltBits = cms.vstring("HLT_L1_CSCMuonHalo"),
                             resultDefinition = cms.int32(4),
                             debug = cms.untracked.bool(False)
                             )

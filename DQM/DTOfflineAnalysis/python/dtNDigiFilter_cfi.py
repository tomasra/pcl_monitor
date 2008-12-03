import FWCore.ParameterSet.Config as cms

dtNDigiFilter = cms.EDFilter("DTNDigiFilter",
                             dtDigiLabel = cms.InputTag("dtunpacker"),
                             debug = cms.untracked.bool(False),
                             threshold = cms.untracked.int32(10),
                             # perChamber -> cut on # digis per chamber
                             # global -> cut on total # of digis
                             granularity = cms.untracked.string("global"),
                             # moreThan -> require # digis > threshold
                             # lessThan -> require # digis < threshold
                             cutType =  cms.untracked.string("lessThan")
                             )

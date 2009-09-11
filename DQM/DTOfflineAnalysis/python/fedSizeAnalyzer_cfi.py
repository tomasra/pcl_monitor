import FWCore.ParameterSet.Config as cms

fedSizeAnalyzer = cms.EDProducer("FEDSizeAnalysis",
                                 rootFileName = cms.untracked.string("FEDSizeAnalysis.root"),
                                 inputLabel = cms.untracked.InputTag("source")
                                 )

import FWCore.ParameterSet.Config as cms





dtLocalRecoAnal = cms.EDAnalyzer("DTLocalRecoAnalysis",
                                 debug = cms.untracked.bool(True),
                                 rootFileName =  cms.untracked.string("DTLocalRecoAnalysis.root"),
                                 doSegmentAnalysis = cms.untracked.bool(True),
                                 doResolutionAnalysis = cms.untracked.bool(False),
                                 segmentAnalysisConfig = cms.PSet(debug = cms.untracked.bool(True),
                                                                  recHits4DLabel  = cms.string('dt4DSegments')
                                                                  ),
                                 resolutionAnalysisConfig = cms.PSet(debug = cms.untracked.bool(False),
                                                                     recHits4DLabel  = cms.string('dt4DSegments'),
                                                                     recHitLabel =  cms.string('dt1DRecHits'),
                                                                     checkNoisyChannels = cms.untracked.bool(False)
                                                                     )
                                 )

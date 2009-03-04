import FWCore.ParameterSet.Config as cms





dtLocalRecoAnal = cms.EDAnalyzer("DTLocalRecoAnalysis",
                                 debug = cms.untracked.bool(False),
                                 rootFileName =  cms.untracked.string("DTLocalRecoAnalysisStd.root"),
                                 doSegmentAnalysis = cms.untracked.bool(True),
                                 doResolutionAnalysis = cms.untracked.bool(True),
                                 segmentAnalysisConfig = cms.PSet(debug = cms.untracked.bool(False),
                                                                  recHits4DLabel  = cms.string('dt4DSegments'),
                                                                  readVdrift = cms.bool(False)
                                                                  ),
                                 resolutionAnalysisConfig = cms.PSet(debug = cms.untracked.bool(False),
                                                                     recHits4DLabel  = cms.string('dt4DSegments'),
                                                                     recHitLabel =  cms.string('dt1DRecHits'),
                                                                     checkNoisyChannels = cms.untracked.bool(False)
                                                                     )
                                 )

dtLocalRecoAnalT0Seg = cms.EDAnalyzer("DTLocalRecoAnalysis",
                                 debug = cms.untracked.bool(False),
                                 rootFileName =  cms.untracked.string("DTLocalRecoAnalysisT0Seg.root"),
                                 doSegmentAnalysis = cms.untracked.bool(True),
                                 doResolutionAnalysis = cms.untracked.bool(True),
                                 segmentAnalysisConfig = cms.PSet(debug = cms.untracked.bool(False),
                                                                  recHits4DLabel  = cms.string('dt4DSegmentsT0Seg'),
                                                                  readVdrift = cms.bool(True)
                                                                  ),
                                 resolutionAnalysisConfig = cms.PSet(debug = cms.untracked.bool(False),
                                                                     recHits4DLabel  = cms.string('dt4DSegmentsT0Seg'),
                                                                     recHitLabel =  cms.string('dt1DRecHits'),
                                                                     checkNoisyChannels = cms.untracked.bool(False)
                                                                     )
                                 )

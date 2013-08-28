import FWCore.ParameterSet.Config as cms


from RecoLocalMuon.DTRecHit.DTLinearDriftFromDBAlgo_cfi import *

#from RecoLocalMuon.DTRecHit.DTParametrizedDriftAlgo_cfi import DTParametrizedDriftAlgo



dtLocalRecoAnal = cms.EDAnalyzer("DTLocalRecoAnalysis",
                                 debug = cms.untracked.bool(False),
                                 rootFileName =  cms.untracked.string("DTLocalRecoAnalysisStd.root"),
                                 doSegmentAnalysis = cms.untracked.bool(False),
                                 doResolutionAnalysis = cms.untracked.bool(False),
                                 doTreeBuilder = cms.untracked.bool(True),
                                 segmentAnalysisConfig = cms.PSet(debug = cms.untracked.bool(False),
                                                                  recHits4DLabel  = cms.string('dt4DSegments'),

                                                                  readVdrift = cms.bool(False)
                                                                  ),
                                 resolutionAnalysisConfig = cms.PSet(debug = cms.untracked.bool(False),
                                                                     recHits4DLabel  = cms.string('dt4DSegments'),
                                                                     recHitLabel =  cms.string('dt1DRecHits'),
                                                                     checkNoisyChannels = cms.untracked.bool(False)
                                                                     ),
                                 treeBuilderConfig = cms.PSet(
#                                     DTParametrizedDriftAlgo,
                                     DTLinearDriftFromDBAlgo,
                                     debug = cms.untracked.bool(False),
                                     recHits4DLabel  = cms.string('dt4DSegments'),
                                     #recHits2DLabel  = cms.string('dt2DSegments'),
                                     recHits2DLabel  = cms.string(''),
                                     recHitLabel =  cms.string('dt1DRecHits'),
                                     muonLabel =  cms.string('muons'),
                                     checkNoisyChannels = cms.untracked.bool(False),       
                                     segmentUpdatorConfig = cms.PSet(
                                         DTLinearDriftFromDBAlgo,
                                         hit_afterT0_resolution = cms.double(0.03),
                                         performT0_vdriftSegCorrection = cms.bool(False),
                                         perform_delta_rejecting = cms.bool(False),
                                         )
                                     )                                
                                 )

dtLocalRecoAnalT0Seg = cms.EDAnalyzer("DTLocalRecoAnalysis",
                                      debug = cms.untracked.bool(False),
                                      rootFileName =  cms.untracked.string("DTLocalRecoAnalysisT0Seg.root"),
                                      doSegmentAnalysis = cms.untracked.bool(False),
                                      doResolutionAnalysis = cms.untracked.bool(False),
                                      doTreeBuilder = cms.untracked.bool(True),
                                      segmentAnalysisConfig = cms.PSet(debug = cms.untracked.bool(False),
                                                                  recHits4DLabel  = cms.string('dt4DSegmentsT0Seg'),                                                                       
                                                                  readVdrift = cms.bool(True)
                                                                  ),
                                      resolutionAnalysisConfig = cms.PSet(debug = cms.untracked.bool(False),
                                                                     recHits4DLabel  = cms.string('dt4DSegmentsT0Seg'),
                                                                     recHitLabel =  cms.string('dt1DRecHits'),
                                                                     checkNoisyChannels = cms.untracked.bool(False)
                                                                     ),
                                      treeBuilderConfig = cms.PSet(debug = cms.untracked.bool(False),
                                                                   recHits4DLabel  = cms.string('dt4DSegments'),
                                                                   recHits2DLabel  = cms.string('dt2DSegments'),
                                                                   recHitLabel =  cms.string('dt1DRecHits'),
                                                                   muonLabel =  cms.string('muons'),
                                                                   checkNoisyChannels = cms.untracked.bool(False)
                                                                   )
                                      
                                 )

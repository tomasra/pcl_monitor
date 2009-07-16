import FWCore.ParameterSet.Config as cms

# filter on trigger type
calibrationEventsFilter = cms.EDFilter("HLTTriggerTypeFilter",
                                       InputLabel = cms.string('source'),
                                       TriggerFedId = cms.int32(812),
                                       # 1=Physics, 2=Calibration, 3=Random, 4=Technical
                                       SelectedTriggerType = cms.int32(1) 
                                       )

# DT digitization and reconstruction
dtunpacker = cms.EDProducer("DTUnpackingModule",
    dataType = cms.string('DDU'),
    useStandardFEDid = cms.untracked.bool(True),
    inputLabel = cms.untracked.InputTag('source'),
    fedbyType = cms.untracked.bool(True),
    readOutParameters = cms.PSet(
        debug = cms.untracked.bool(False),
        rosParameters = cms.PSet(
            writeSC = cms.untracked.bool(True),
            readingDDU = cms.untracked.bool(True),
            performDataIntegrityMonitor = cms.untracked.bool(False),
            readDDUIDfromDDU = cms.untracked.bool(True),
            debug = cms.untracked.bool(False),
            localDAQ = cms.untracked.bool(False)
        ),
        localDAQ = cms.untracked.bool(False),
        performDataIntegrityMonitor = cms.untracked.bool(False)
    )
)

from Configuration.StandardSequences.Geometry_cff import *
from Configuration.StandardSequences.ReconstructionCosmics_cff import *
#from RecoLocalMuon.Configuration.RecoLocalMuonCosmics_cff import *
#dt1DRecHits.dtDigiLabel = 'dtunpacker'

# # switch on code for t0 correction
# dt2DSegments.Reco2DAlgoConfig.performT0SegCorrection = True
# dt2DSegments.Reco2DAlgoConfig.T0_hit_resolution = cms.untracked.double(0.0250)

# dt4DSegments.Reco4DAlgoConfig.performT0SegCorrection = True
# dt4DSegments.Reco4DAlgoConfig.T0_hit_resolution = cms.untracked.double(0.0250)
# dt4DSegments.Reco4DAlgoConfig.T0SegCorrectionDebug = False


from Configuration.StandardSequences.FrontierConditions_GlobalTag_cff import *


#reco = cms.Sequence(dtunpacker + dtlocalreco + dtlocalrecoT0Seg)
reco = cms.Sequence(dtunpacker + dtlocalreco)

#dt4DSegmentsT0Seg.Reco4DAlgoConfig.Reco2DAlgoConfig.performT0SegCorrection = True
#dt4DSegmentsT0Seg.Reco4DAlgoConfig.Reco2DAlgoConfig.performT0_vdriftSegCorrection = True

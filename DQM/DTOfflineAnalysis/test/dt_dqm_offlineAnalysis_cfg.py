import FWCore.ParameterSet.Config as cms

process = cms.Process("DTOffAna")

# the source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
  '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/FEF751C0-0BA3-DD11-9D95-000423D9A212.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/FE573C17-47A3-DD11-8BD3-001D09F24664.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/FE4944AF-3CA3-DD11-BDEE-000423D99AAA.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/FCFFF80E-51A3-DD11-BBC2-001D09F252DA.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/FCC91EA4-6CA3-DD11-B66C-000423D98F98.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/FCABAB02-04A3-DD11-8192-001D09F29538.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/FC95ABE8-06A3-DD11-A964-001617C3B654.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/FC5D7150-34A3-DD11-94BA-000423D9989E.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/FAC88766-0DA3-DD11-A90B-0030487BC68E.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/FA824797-76A3-DD11-A0C6-001D09F23D04.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/FA813B87-F8A2-DD11-9325-0030487A18A4.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/FA74B515-02A3-DD11-82AB-001D09F2532F.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/FA717B22-69A3-DD11-8F9C-001D09F24F1F.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/FA212672-F6A2-DD11-A174-001D09F28E80.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/FA08C573-F1A2-DD11-903E-001D09F252DA.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/F8DEC579-2FA3-DD11-9AA2-001D09F2932B.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/F8836370-55A3-DD11-B8B4-001617C3B6CC.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/F8828E6F-18A3-DD11-AD77-000423D99AAE.root',
          '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/647/F87F6BC5-3DA3-DD11-9518-001D09F27003.root'
      ))


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
    )


process.load("DQM.DTOfflineAnalysis.dt_dqm_offlineAnalysis_common_cff")
process.load("DQM.DTOfflineAnalysis.dtLocalRecoAnalysis_cfi")
process.GlobalTag.globaltag = "GR09_31X_V3P::All"
process.dt1DRecHits.dtDigiLabel = 'dtunpacker'

from CondCore.DBCommon.CondDBSetup_cfi import *
process.ttrigsource = cms.ESSource("PoolDBESSource",
                                   CondDBSetup,
                                   timetype = cms.string('runnumber'),
                                   toGet = cms.VPSet(cms.PSet(record = cms.string('DTTtrigRcd'),
                                                              tag = cms.string('ttrig')
                                                              )
                                                     ),
                                   connect = cms.string('sqlite_file:/afs/cern.ch/user/c/cerminar/scratch0/DTCalibration/CMSSW_3_1_1/src/DQM/DTOfflineAnalysis/test/dbs/r67647/merda_t-4.db'),
                                   authenticationMethod = cms.untracked.uint32(0)
                                   )
process.preferTTrigMap = cms.ESPrefer('PoolDBESSource','ttrigsource')


# message logger
process.MessageLogger = cms.Service("MessageLogger",
                                    debugModules = cms.untracked.vstring('*'),
                                    destinations = cms.untracked.vstring('cout'),
                                    categories = cms.untracked.vstring('DTNoiseAnalysisTest'), 
                                    cout = cms.untracked.PSet(threshold = cms.untracked.string('DEBUG'),
                                                              noLineBreaks = cms.untracked.bool(False),
                                                              DEBUG = cms.untracked.PSet(
                                                                      limit = cms.untracked.int32(0)),
                                                              INFO = cms.untracked.PSet(
                                                                      limit = cms.untracked.int32(0)),
                                                              DTNoiseAnalysisTest = cms.untracked.PSet(
                                                                                 limit = cms.untracked.int32(-1))
                                                              )
                                    )


# --- IGUANA cfg --------------------------------------------------------
process.add_(
    cms.Service("IguanaService",
    outputFileName = cms.untracked.string('DTSegments_r67647_t-4.ig'),
    online = cms.untracked.bool(False),
    debug = cms.untracked.bool(True)
    )
)

process.load("VisReco.Analyzer.VisDTRecSegment4D_cfi")
process.load('VisReco.Analyzer.VisDTDigi_cfi')
process.load('VisReco.Analyzer.VisDTRecHit_cfi')
process.VisDTRecHit.visDTRecHitTag = cms.InputTag("dt1DRecHits")

# -----------------------------------------------------------------------


process.jobPath = cms.Path(process.reco + process.dtLocalRecoAnal + process.VisDTDigi * process.VisDTRecSegment4D * process.VisDTRecHit)
# process.jobPath = cms.Path(process.reco + process.dtLocalRecoAnal)

#process.jobPath = cms.Path(process.dtLocalRecoAnal)


#f = file('aNewconfigurationFile.cfg', 'w')
#f.write(process.dumpConfig())
#f.close()


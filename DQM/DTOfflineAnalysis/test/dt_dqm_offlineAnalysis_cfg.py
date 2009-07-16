import FWCore.ParameterSet.Config as cms

process = cms.Process("DTOffAna")

# the source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/820/84097095-0172-DE11-BD73-000423D944F8.root',
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/820/4A0A9AAE-ED71-DE11-9F95-001D09F27003.root',
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/820/3E308797-EE71-DE11-986A-001D09F253D4.root',
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/820/12BBDBFC-0272-DE11-B8DF-001D09F2AF96.root',
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/820/0621E5AE-ED71-DE11-9633-001D09F24498.root',
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/812/062964A0-E871-DE11-98BD-000423D94700.root',
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/765/FCC57794-A371-DE11-A624-000423D992A4.root',
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/765/FCB30018-C271-DE11-81CA-000423D951D4.root',
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/765/FC9A95A4-A571-DE11-8A0B-000423D944DC.root',
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/765/FC768B72-C471-DE11-9307-000423D990CC.root',
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/765/FC5B9DAF-B871-DE11-8FAF-001D09F254CE.root',
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/765/FC01DDF5-C371-DE11-B1EF-001D09F24FEC.root',
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/765/FA95271D-A771-DE11-B4FE-001D09F254CE.root',
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/765/FA55CCC6-AC71-DE11-8682-000423D9880C.root',
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/765/FA4E96FA-D871-DE11-B037-000423D99896.root',
    '/store/data/Commissioning09/Cosmics/RAW/v3/000/105/765/FA4962C4-AC71-DE11-871E-000423D99896.root'    ))


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
                                   connect = cms.string('sqlite_file:/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/COMM09/ttrig/ttrig_ResidCorr_102183.db'),
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


process.jobPath = cms.Path(process.reco + process.dtLocalRecoAnal)
#process.jobPath = cms.Path(process.dtLocalRecoAnal)


#f = file('aNewconfigurationFile.cfg', 'w')
#f.write(process.dumpConfig())
#f.close()


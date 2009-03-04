import FWCore.ParameterSet.Config as cms

process = cms.Process("DTOffAna")

# the source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/002ABA60-CDA4-DD11-9D53-001D09F248FD.root',
    '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/00559BCE-DAA4-DD11-A35B-000423D9517C.root',
    '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/00696BD3-74A4-DD11-AB50-001617DBD5B2.root',
    '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/00D1727B-BCA4-DD11-89C7-001D09F23A07.root',
    '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/00DFF5CC-E8A4-DD11-93ED-001D09F23E53.root',
    '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/00ED84F0-D7A4-DD11-912C-001D09F2462D.root',
    '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/0230E879-BAA4-DD11-AD5E-000423D98634.root',
    '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/023638D9-DCA4-DD11-8AE3-001D09F24FE7.root',
    '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/025B07B0-85A4-DD11-9828-000423D98634.root',
    '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/02FE6C69-C8A4-DD11-AB1E-001617C3B69C.root',
    '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/0401FDAC-86A4-DD11-9145-0019DB29C5FC.root',
    '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/049A3FFE-90A4-DD11-AA53-001617C3B76E.root',
    '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/04CC5535-D0A4-DD11-B7FB-000423D99BF2.root'
    ))


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
    )


process.load("DQM.DTOfflineAnalysis.dt_dqm_offlineAnalysis_common_cff")
process.load("DQM.DTOfflineAnalysis.dtLocalRecoAnalysis_cfi")
#process.dtOfflineOccupancy.rootFileName = "DTOfflineOccupancy_splash.root"

process.GlobalTag.globaltag = "CRAFT_ALL_V8::All"
process.dt1DRecHits.dtDigiLabel = 'dtunpacker'

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
                                                                                 limit = cms.untracked.int32(100000000))
                                                              )
                                    )


process.jobPath = cms.Path(process.reco + process.dtLocalRecoAnal + process.dtLocalRecoAnalT0Seg)
#process.jobPath = cms.Path(process.dtLocalRecoAnal)


#f = file('aNewconfigurationFile.cfg', 'w')
#f.write(process.dumpConfig())
#f.close()


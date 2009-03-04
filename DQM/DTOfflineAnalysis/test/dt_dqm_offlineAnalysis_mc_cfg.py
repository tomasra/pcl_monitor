import FWCore.ParameterSet.Config as cms

process = cms.Process("DTOffAna")

# the source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
    '/store/mc/Summer08/CosmicMCBOn10GeV/GEN-SIM-RAW/COSMMC_21X_v3/0010/024306F6-6691-DD11-B397-00304877A312.root',
    '/store/mc/Summer08/CosmicMCBOn10GeV/GEN-SIM-RAW/COSMMC_21X_v3/0010/04B27EBA-D290-DD11-B09C-003048553C30.root',
    '/store/mc/Summer08/CosmicMCBOn10GeV/GEN-SIM-RAW/COSMMC_21X_v3/0010/0A2D664B-D490-DD11-8333-003048322BF6.root',
    '/store/mc/Summer08/CosmicMCBOn10GeV/GEN-SIM-RAW/COSMMC_21X_v3/0010/14778A43-6D91-DD11-911C-003048770BAA.root',
    '/store/mc/Summer08/CosmicMCBOn10GeV/GEN-SIM-RAW/COSMMC_21X_v3/0010/2229B83F-D490-DD11-920C-003048322CA0.root',
    '/store/mc/Summer08/CosmicMCBOn10GeV/GEN-SIM-RAW/COSMMC_21X_v3/0010/22F8CF61-CB90-DD11-98DB-001A9243D630.root',
    '/store/mc/Summer08/CosmicMCBOn10GeV/GEN-SIM-RAW/COSMMC_21X_v3/0010/2A5E8344-E590-DD11-A3BA-003048553C30.root',
    '/store/mc/Summer08/CosmicMCBOn10GeV/GEN-SIM-RAW/COSMMC_21X_v3/0010/2C18E47E-D490-DD11-8A87-003048335548.root'
    ))


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
    )


process.load("DQM.DTOfflineAnalysis.dt_dqm_offlineAnalysis_common_cff")
process.load("DQM.DTOfflineAnalysis.dtLocalRecoAnalysis_cfi")
#process.dtOfflineOccupancy.rootFileName = "DTOfflineOccupancy_splash.root"

process.GlobalTag.globaltag = "COSMMC_21X_V1::All"
process.dt1DRecHits.dtDigiLabel = 'dtunpacker'
process.dtunpacker.inputLabel = 'rawDataCollector'
process.dtunpacker.fedbyType = False

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


import FWCore.ParameterSet.Config as cms

process = cms.Process("DTOffAna")

# the source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
    'file:/data/c/cerminar/data/CosmicMCBOn10GeV-GEN-SIM-RAW/34A263C4-0491-DD11-8B23-001A9227D359.root'
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


# f = file('configuratiodump_cfg.py', 'w')
# f.write(process.dumpPython())
# f.close()


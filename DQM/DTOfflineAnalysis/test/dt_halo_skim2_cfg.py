import FWCore.ParameterSet.Config as cms

process = cms.Process("Skim2")

# the source
process.source = cms.Source("PoolSource",
     fileNames = cms.untracked.vstring(
     'file:/data/c/cerminar/data/GlobalRun/Run62232_SkimHLT_L1_CSCMuonHalo_a.root',
     'file:/data/c/cerminar/data/GlobalRun/Run62232_SkimHLT_L1_CSCMuonHalo_b.root',
     )
                             )
#process.source.skipEvents = 500000

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(5000)
    )



process.load("DQM.DTOfflineAnalysis.dt_dqm_offlineAnalysis_common_cff")
process.dtRecoFilter.dtDigiLabel = "muonDTDigis"


process.bxFilter = cms.EDFilter("BxNumberFilter",
                                #inputLabel = cms.InputTag("source"),
                                goldenBXIds = cms.vint32(901,832),
                                range = cms.untracked.uint32(1),
                                debug = cms.untracked.uint32(1))


# message logger
process.MessageLogger = cms.Service("MessageLogger",
                                    destinations = cms.untracked.vstring('cout'),
                                    cout = cms.untracked.PSet(threshold = cms.untracked.string('INFO'))
                                    )



process.mySkim2 = cms.Path(process.dtRecoFilter)



process.out1 = cms.OutputModule("PoolOutputModule",
                                #compressionLevel = cms.untracked.int32(9),
                                fileName = cms.untracked.string('/data/c/cerminar/data/GlobalRun/Run62232_Skim2_small.root'),
                                SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring('mySkim2'))
                                )
 


process.output = cms.EndPath(process.out1)



# f = file('aNewconfigurationFile.cfg', 'w')
# f.write(process.dumpConfig())
# f.close()



import FWCore.ParameterSet.Config as cms

process = cms.Process("offAnalysis")

# the source
# process.source = cms.Source("PoolSource",
#     fileNames = cms.untracked.vstring(
#      '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/04FF0C7D-7280-DD11-8FCD-000423D98F98.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/082A4A06-4180-DD11-BE09-000423D6CAF2.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/08776190-6B80-DD11-8C59-0016177CA7A0.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/124E8F95-5280-DD11-8A56-001617C3B64C.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/18542160-6C80-DD11-B371-001617DBD332.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/1CBA5A5C-7280-DD11-87F7-000423D98DB4.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/2299233E-5B80-DD11-A5E4-000423D9939C.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/241A75D4-6D80-DD11-9FC3-001617E30D4A.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/28373AD8-6F80-DD11-BEF9-000423D6CA6E.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/388D7F9F-6B80-DD11-8C5C-001617DBD472.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/42572F1B-5880-DD11-9977-001617E30CE8.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/520371CD-7080-DD11-9E08-001617C3B5D8.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/5637E70A-6C80-DD11-B472-001617E30F58.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/5A9127C6-6280-DD11-BC1F-001617C3B6CC.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/62427D18-6B80-DD11-97E7-001617E30D06.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/66AC0B48-6280-DD11-9DB3-001617E30F56.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/680EB2BB-6B80-DD11-B19E-001617DBCF1E.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/684CC7E2-5A80-DD11-BF3C-001617C3B70E.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/6ACD28A5-6D80-DD11-BBE9-001617C3B73A.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/6ADC765C-7280-DD11-9109-000423D98DB4.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/721169E1-7280-DD11-B54C-000423D99F3E.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/74EB0F58-7480-DD11-883A-000423D6C8E6.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/7693CEA9-6E80-DD11-828C-001617E30D38.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/7C306875-5780-DD11-8931-001617C3B706.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/823C563E-6B80-DD11-9F1D-001617C3B66C.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/84A0B72F-6C80-DD11-824F-001617C3B5F4.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/889C3866-4B80-DD11-BDED-000423D6CA72.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/90CBDE71-6780-DD11-93C3-001617DBD556.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/90CE5B16-7080-DD11-8340-001617C3B6E8.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/96498165-4380-DD11-95CB-000423D6C8EE.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/A463FB01-7380-DD11-9223-000423D98868.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/AC0C4953-6E80-DD11-AE63-001617C3B654.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/B07E8E7D-5680-DD11-977A-000423D6B2D8.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/B262CB4B-5680-DD11-B703-0019DB29C5FC.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/B2EAE5B6-6180-DD11-9DD2-000423D986A8.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/B46177F3-6A80-DD11-B6E3-001617DF785A.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/B657B2D2-3F80-DD11-BFC9-001617DBD288.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/B66DB821-5780-DD11-9DF4-001617C3B6C6.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/B699F24F-6880-DD11-A012-000423D9853C.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/B8C3C462-7080-DD11-9AE5-000423D98804.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/C42EBFDB-4980-DD11-B255-000423D9870C.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/CC6BFD75-7280-DD11-8749-000423D999CA.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/CCAF3AA8-6980-DD11-B730-000423D6CA02.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/DA67A3A1-6480-DD11-90CF-000423D6B42C.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/DCC5076F-6980-DD11-96A1-001617C3B79A.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/DEE5E173-6880-DD11-BB84-000423D6CAF2.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/ECB14149-6380-DD11-9675-001617C3B778.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/F0DD6021-6E80-DD11-8DCC-001617DBD5AC.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/F0E35422-5A80-DD11-8F53-001617C3B76E.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/F2AAED26-6280-DD11-9A88-000423D6CA42.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/F2FF0824-4580-DD11-9DCB-001617C3B6E2.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/F8AE5F03-5F80-DD11-959F-001617C3B6DC.root',
#         '/store/data/BeamCommissioning08/BeamHalo/RECO/v1/000/062/232/FCF2DC79-6980-DD11-A007-001617E30D52.root'
#      )
#                             )

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
    'file:/data/c/cerminar/data/GlobalRun/Run62232_SkimHLT_L1_CSCMuonHalo_a.root',
    'file:/data/c/cerminar/data/GlobalRun/Run62232_SkimHLT_L1_CSCMuonHalo_a.root'
    )
                            )
    

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )

#process.load("DQM.DTOfflineAnalysis.source_cfi")
#process.source.skipEvents = 500000

process.load("DQM.DTOfflineAnalysis.dt_dqm_offlineAnalysis_common_cff")
process.load("DQM.DTOfflineAnalysis.dtOfflineOccupancy_cfi")
process.load("DQM.DTOfflineAnalysis.triggerPathFilter_cfi")
process.dtOfflineOccupancy.rootFileName = "DTOfflineOccupancy_halo.root"
process.dtOfflineOccupancy.dtDigiLabel = "muonDTDigis"
process.dtOfflineOccupancy.mode = "halo"

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




process.out1 = cms.OutputModule("PoolOutputModule",
                                #compressionLevel = cms.untracked.int32(9),
                                fileName = cms.untracked.string('/data/c/cerminar/data/GlobalRun/Run62232_SkimHLT_L1_CSCMuonHalo.root'),
                                SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring('dtHalo'))
                                )
 


#process.dtHalo = cms.Path(process.triggerFilter * process.bxFilter * process.dtOfflineOccupancy)
#process.output = cms.EndPath(process.out1)


process.dtHalo = cms.Path(process.dtOfflineOccupancy)




# f = file('aNewconfigurationFile.cfg', 'w')
# f.write(process.dumpConfig())
# f.close()



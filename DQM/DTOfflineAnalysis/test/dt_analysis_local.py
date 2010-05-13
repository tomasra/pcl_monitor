import FWCore.ParameterSet.Config as cms

process = cms.Process("DTOffAna3")

# the source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
                                'file:/data/c/cerminar/data/DtCalibrationGoodCollV9-100507-V03/good_coll.root'
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_10_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_11_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_12_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_13_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_14_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_15_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_16_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_17_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_19_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_1_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_20_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_21_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_22_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_24_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_25_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_26_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_27_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_28_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_29_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_31_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_32_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_33_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_35_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_38_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_39_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_3_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_40_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_41_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_47_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_48_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_49_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_4_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_50_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_51_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_52_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_53_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_54_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_55_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_56_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_57_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_58_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_59_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_5_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_60_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_61_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_62_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_63_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_64_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_65_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_66_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_67_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_68_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_69_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_6_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_70_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_71_2.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_72_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_73_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_74_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_7_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_8_1.root',
# '/store/caf/user/cerminar/MinimumBias/DtCalibrationGoodCollV9-100507-V03/af5da1d43807c3c24b74ecca32fc0226/good_coll_9_1.root'
                                ))

process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*", "drop L1GlobalTriggerObjectMapRecord_hltL1GtObjectMap__HLT")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )


process.load('Configuration/StandardSequences/MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration/StandardSequences/GeometryIdeal_cff')


process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "GR_R_35X_V8::All"

                                            
process.GlobalTag.toGet = cms.VPSet(
    cms.PSet(record = cms.string("DTTtrigRcd"),
             tag = cms.string("ttrig"),
             connect = cms.untracked.string("sqlite_file:ttrigStat1_V0.db")
             )
    )



process.load("Configuration/StandardSequences/RawToDigi_Data_cff")
process.load("Configuration/StandardSequences/Reconstruction_cff")
process.load('Configuration/EventContent/EventContent_cff')

process.FEVTEventContent.outputCommands.append('drop *_MEtoEDMConverter_*_*')

process.load('L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskAlgoTrigConfig_cff')
process.load('L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskTechTrigConfig_cff')
process.load('HLTrigger/HLTfilters/hltLevel1GTSeed_cfi')


process.dtNDigiFilter = cms.EDFilter("DTNDigiFilter",
    threshold = cms.untracked.int32(10),
    debug = cms.untracked.bool(False),
    dtDigiLabel = cms.InputTag("muonDTDigis"),
    granularity = cms.untracked.string('perChamber'),
    cutType = cms.untracked.string('moreThan')
)

process.load('DQM.DTOfflineAnalysis.dtLocalRecoAnalysis_cfi')
process.dtLocalRecoAnal.rootFileName = '/data/c/cerminar/data/DtCalibrationGoodCollV9-100507-V03_NewTableV0/DTLocalRecoAnalysisStd.root'

####################################################################################
##################################good collisions############################################

process.L1T1coll=process.hltLevel1GTSeed.clone()
process.L1T1coll.L1TechTriggerSeeding = cms.bool(True)
process.L1T1coll.L1SeedsLogicalExpression = cms.string('0 AND (40 OR 41) AND NOT (36 OR 37 OR 38 OR 39) AND NOT ((42 AND NOT 43) OR (43 AND NOT 42))')

#process.l1tcollpath = cms.Path(process.L1T1coll*process.muonDTDigis*process.dtlocalreco*process.dtNDigiFilter+process.dtLocalRecoAnal)

process.primaryVertexFilter = cms.EDFilter("VertexSelector",
   src = cms.InputTag("offlinePrimaryVertices"),
   cut = cms.string("!isFake && ndof > 4 && abs(z) <= 15 && position.Rho <= 2"), # tracksSize() > 3 for the older cut
   filter = cms.bool(True),   # otherwise it won't filter the events, just produce an empty vertex collection.
)


process.noscraping = cms.EDFilter("FilterOutScraping",
applyfilter = cms.untracked.bool(True),
debugOn = cms.untracked.bool(False),
numtrack = cms.untracked.uint32(10),
thresh = cms.untracked.double(0.25)
)

#process.goodvertex=cms.Path(process.primaryVertexFilter+process.noscraping*process.muonDTDigis*process.dtlocalreco*process.dtNDigiFilter+process.dtLocalRecoAnal)


process.collout = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('/data/c/cerminar/data/DtCalibrationGoodCollV9-100507-V03_NewTableV0/good_coll.root'),
    outputCommands = process.FEVTEventContent.outputCommands,
    dataset = cms.untracked.PSet(
    	      dataTier = cms.untracked.string('RAW-RECO'),
    	      filterName = cms.untracked.string('GOODCOLL')),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('goodvertex','l1tcollpath')
    )
)

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



process.recoonly = cms.Path(process.muonDTDigis*process.dtlocalreco+process.dtLocalRecoAnal) 

#process.outpath = cms.EndPath(process.collout)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
    )



# process.jobPath = cms.Path(process.reco + process.dtLocalRecoAnal)

#process.jobPath = cms.Path(process.dtLocalRecoAnal)


#f = file('aNewconfigurationFile.cfg', 'w')
#f.write(process.dumpConfig())
#f.close()


import FWCore.ParameterSet.Config as cms

process = cms.Process("DTOffAna")

# RelValPt100
# process.source = cms.Source("PoolSource",
#                             fileNames = cms.untracked.vstring( 
#   '/store/relval/CMSSW_3_8_4/RelValSingleMuPt100/GEN-SIM-RECO/MC_38Y_V12-v1/0024/C004CB9E-82C2-DF11-835C-0018F3D0965C.root',
#         '/store/relval/CMSSW_3_8_4/RelValSingleMuPt100/GEN-SIM-RECO/MC_38Y_V12-v1/0024/12514483-81C2-DF11-95F5-001A92971BDC.root'
#     ),
#                             secondaryFileNames = cms.untracked.vstring(
#   '/store/relval/CMSSW_3_8_4/RelValSingleMuPt100/GEN-SIM-DIGI-RAW-HLTDEBUG/MC_38Y_V12-v1/0024/6EA8F12B-96C2-DF11-B752-002618943970.root',
#         '/store/relval/CMSSW_3_8_4/RelValSingleMuPt100/GEN-SIM-DIGI-RAW-HLTDEBUG/MC_38Y_V12-v1/0024/3249E6FB-80C2-DF11-A648-0018F3D09670.root',
#         '/store/relval/CMSSW_3_8_4/RelValSingleMuPt100/GEN-SIM-DIGI-RAW-HLTDEBUG/MC_38Y_V12-v1/0024/1CB0C3FE-81C2-DF11-91F7-0018F3D096CA.root',
#         '/store/relval/CMSSW_3_8_4/RelValSingleMuPt100/GEN-SIM-DIGI-RAW-HLTDEBUG/MC_38Y_V12-v1/0024/083E2B82-81C2-DF11-91E0-0018F3D0969C.root'
#     )
# )

# RelValZMM
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring( 
    '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-RECO/START38_V12-v1/0025/AA80C1F7-9AC2-DF11-817E-00261894398B.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-RECO/START38_V12-v1/0024/BAADB103-80C2-DF11-9602-0026189437E8.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-RECO/START38_V12-v1/0024/929C50FE-83C2-DF11-8757-002618943935.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-RECO/START38_V12-v1/0024/5E7ED90D-7FC2-DF11-8FDF-001A928116C0.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-RECO/START38_V12-v1/0024/42595C94-7FC2-DF11-A952-003048678FE4.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-RECO/START38_V12-v1/0024/00ABC27B-86C2-DF11-A82D-003048678B16.root'
    ),
                            secondaryFileNames = cms.untracked.vstring(
 '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START38_V12-v1/0025/883FC8F4-9AC2-DF11-8FA0-003048D3C010.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START38_V12-v1/0024/F0D989FC-83C2-DF11-A58B-002618FDA279.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START38_V12-v1/0024/E8E2A87D-7EC2-DF11-B4DE-003048678F02.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START38_V12-v1/0024/D0404798-7FC2-DF11-BA73-0018F3D095F0.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START38_V12-v1/0024/CA661A04-80C2-DF11-9273-0018F3D095F2.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START38_V12-v1/0024/C649BDFF-84C2-DF11-B3CE-0018F3D0961E.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START38_V12-v1/0024/A0A502FC-85C2-DF11-9905-00304867901A.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START38_V12-v1/0024/A09D6F07-7FC2-DF11-B96D-002618943983.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START38_V12-v1/0024/947B2EFB-81C2-DF11-98AD-001A92810AE0.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START38_V12-v1/0024/8A06F203-80C2-DF11-BAD7-0018F3D09620.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START38_V12-v1/0024/7E82CD79-87C2-DF11-9C3F-002618943956.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START38_V12-v1/0024/6C132CFF-7EC2-DF11-91FB-0026189438D6.root',
        '/store/relval/CMSSW_3_8_4/RelValZMM/GEN-SIM-DIGI-RAW-HLTDEBUG/START38_V12-v1/0024/0EFE3080-80C2-DF11-B465-002618943935.root'
    )
)


process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*", "drop L1GlobalTriggerObjectMapRecord_hltL1GtObjectMap__HLT")


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.MixingNoPileUp_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("Configuration/StandardSequences/Reconstruction_cff")
process.load('Configuration.EventContent.EventContent_cff')

# message logger
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

#process.GlobalTag.globaltag = "MC_38Y_V12::All"
process.GlobalTag.globaltag = "START38_V12::All"



process.load("DQM.DTOfflineAnalysis.dtLocalRecoAnalysis_cfi")


process.GlobalTag.toGet = cms.VPSet(
#        cms.PSet(record = cms.string("DTTtrigRcd"),
#                 tag = cms.string("ttrig"),
#                 connect = cms.untracked.string("sqlite_file:ttrig_ZMM_vd1.db")),
      cms.PSet(record = cms.string("DTMtimeRcd"),
               tag = cms.string("vdrift"),
               connect = cms.untracked.string("sqlite_file:MC_vdrift_543_532_sigma_ZMM_sigma4_ns2_statByLayer.db"))
#    cms.PSet(record = cms.string("DTT0Rcd"),
#             tag = cms.string("t0"),
#             connect = cms.untracked.string("sqlite_file:../calib/MyTables/MC_T0_sigma5.db"))
)

### Non-standard DB alignment
#DTGeom16May_Design.db --> internal alignment nominale
#DTGeom16May_SL.db     --> superlayer corrections
#DTGeom16May_Layer.db  --> layer to layer corrections
#
# import CondCore.DBCommon.CondDBSetup_cfi
# process.muonAlignment = cms.ESSource("PoolDBESSource",
#                                      connect = cms.string("sqlite_file:DTGeom16May_SL.db"),

#                                      DBParameters = CondCore.DBCommon.CondDBSetup_cfi.CondDBSetup.DBParameters,
#                                      toGet = cms.VPSet(cms.PSet(record = cms.string("DTAlignmentRcd"),
#                                                                 tag =  cms.string("DTAlignmentRcd")),
#                                                        cms.PSet(record = cms.string("DTAlignmentErrorRcd"),
#                                                                 tag =  cms.string("DTAlignmentErrorRcd"))
#                                                        )
#                                      )
# process.es_prefer_muonAlignment = cms.ESPrefer("PoolDBESSource","muonAlignment")
### 


### No rereco
#process.jobPath = cms.Path(process.dt2DSegments+process.dtLocalRecoAnal)

### RERECO (keep digis)
#process.jobPath = cms.Path(process.muonDTDigis+process.dtlocalreco+process.dt2DSegments + process.muonreco + process.dtLocalRecoAnal)


### REDIGI + RERECO (necessary for 38X series)
process.RandomNumberGeneratorService.restoreStateLabel = cms.untracked.string('randomEngineStateProducer')
pDTdigi = cms.Sequence(cms.SequencePlaceholder("randomEngineStateProducer")*cms.SequencePlaceholder("mix")*process.simMuonDTDigis*process.trackingParticles)
process.jobPath = cms.Path(pDTdigi+process.dtpacker+process.rawDataCollector+process.muonDTDigis+process.dtlocalreco+process.dt2DSegments* process.muonreco*process.dtLocalRecoAnal)

process.dtLocalRecoAnal.rootFileName = 'DTLocalReco.root'


process.options = cms.untracked.PSet(
#    wantSummary = cms.untracked.bool(True)
    fileMode = cms.untracked.string('NOMERGE')
    )


# f = file('configuratiodump_cfg.py', 'w')
# f.write(process.dumpPython())
# f.close()


import FWCore.ParameterSet.Config as cms

process = cms.Process("DTOffAna")

# the source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
                                'root://castorcms//castor/cern.ch/cms/store/caf/user/cerminar/Commissioning/DtCalibrationGoodColl-MuonDPG_skim-v6_V3/abde1693b1e2a1fd51144c650705ec92/good_coll_10_2_6jh.root'
                                )
                            
#    duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*", "drop L1GlobalTriggerObjectMapRecord_hltL1GtObjectMap__HLT")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
    )


process.load("DQM.DTOfflineAnalysis.dtLocalRecoAnalysis_cfi")


process.load('Configuration/StandardSequences/MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration/StandardSequences/Geometry_cff')


process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "GR_R_38X_V13::All"

process.GlobalTag.toGet = cms.VPSet(
#    cms.PSet(record = cms.string("DTTtrigRcd"),
#             tag = cms.string("ttrig"),
#             connect = cms.untracked.string("sqlite_file:Data_v5.db"))
    cms.PSet(record = cms.string("DTMtimeRcd"),
             tag = cms.string("vdrift"),
             connect = cms.untracked.string("sqlite_file:vdrift_543_v5s1_statByLayer_sigma_a.db"))
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


process.load("Configuration/StandardSequences/RawToDigi_Data_cff")
process.load("Configuration/StandardSequences/Reconstruction_cff")
#process.load('Configuration/EventContent/EventContent_cff')



# message logger
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

from HLTrigger.HLTfilters.hltHighLevelDev_cfi import hltHighLevelDev
process.hltL1DoubleMuOpen_Tight  = hltHighLevelDev.clone(HLTPaths = ['HLT_L1DoubleMuOpen_Tight'],  HLTPathsPrescales = [1])
process.Filter  = cms.Sequence(process.hltL1DoubleMuOpen_Tight)

process.primaryVertexFilter = cms.EDFilter("VertexSelector",
   src = cms.InputTag("offlinePrimaryVertices"),
   cut = cms.string("!isFake && ndof > 4 && abs(z) <= 25 && position.Rho <= 2"), # tracksSize() > 3 for the older cut
   filter = cms.bool(True),   # otherwise it won't filter the events, just produce an empty vertex collection.
)

process.noscraping = cms.EDFilter("FilterOutScraping",
applyfilter = cms.untracked.bool(True),
debugOn = cms.untracked.bool(False),
numtrack = cms.untracked.uint32(10),
thresh = cms.untracked.double(0.25)
)


process.dtLocalRecoAnal.rootFileName = 'DTLocalReco.root'


process.jobPath = cms.Path(process.noscraping*process.primaryVertexFilter*process.muonDTDigis*process.dtlocalreco+process.dt2DSegments+process.muonreco+process.dtLocalRecoAnal)



process.options = cms.untracked.PSet(
#    wantSummary = cms.untracked.bool(True)
    fileMode = cms.untracked.string('NOMERGE')
    )


# f = file('configuratiodump_cfg.py', 'w')
# f.write(process.dumpPython())
# f.close()



#GLOBALTAG = "START53_V7G"
#GLOBALTAG = "MC_53_V7A"
#GLOBALTAG = "PRE_ST62_V8"

#GLOBALTAG = "FT_R_53_V21" 
#GLOBALTAG = "GR_P_V42"
GLOBALTAG = "FT_53_V21_AN3" #for 22Jan2013
#RUN=198049 # approx start of 2012C
#RUN=202305 # approx end of 2012C
#RUN=203894 # approx stary of 2012D
RUN=999999

###########

import FWCore.ParameterSet.Config as cms

process = cms.Process("DumpDBToFile")
process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.source = cms.Source("EmptySource",
    numberEventsInRun = cms.untracked.uint32(1),
    firstRun = cms.untracked.uint32(RUN)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)


process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = GLOBALTAG+"::All"


#process.GlobalTag.connect = "sqlite_file:/afs/cern.ch/user/c/cerminar/public/Alca/GlobalTag/GR_R_38X_V9.db"
#process.GlobalTag.globaltag = "GR_R_38X_V9::All"


# process.GlobalTag.toGet = cms.VPSet(
#     cms.PSet(record = cms.string("DTTtrigRcd"),
#              tag = cms.string("ttrig"),
#              connect = cms.untracked.string("sqlite_file:ttrig_paramDrift_v1.db")
#              )
#     )

# process.calibDB = cms.ESSource("PoolDBESSource",
#     process.CondDBSetup,
#     authenticationMethod = cms.untracked.uint32(0),
#     toGet = cms.VPSet(cms.PSet(
#         # VDrift
#         #record = cms.string("DTMtimeRcd"),
#         #tag = cms.string("DT_vDrift_CRAFT_V02_offline")
#         # TZero
#         #record = cms.string("DTT0Rcd" ),
#         #tag = cms.string("t0"),
#         # TTrig
#         record = cms.string('DTTtrigRcd'),
#         tag = cms.string('ttrig')
#     )),
#     connect = cms.string('frontier://FrontierPrep/CMS_COND_31X_All')
# )

process.dumpT0ToFile = cms.EDAnalyzer("DumpDBToFile",
    dbToDump = cms.untracked.string('TZeroDB'),
    dbLabel = cms.untracked.string(''),
    calibFileConfig = cms.untracked.PSet(
        nFields = cms.untracked.int32(8),
        calibConstGranularity = cms.untracked.string('byWire')
    ),
    outputFileName = cms.untracked.string(GLOBALTAG+"_"+str(RUN)+'_t0.txt')
)

process.dumpTTrigToFile = cms.EDAnalyzer("DumpDBToFile",
    dbToDump = cms.untracked.string('TTrigDB'),
    dbLabel = cms.untracked.string(''),
    calibFileConfig = cms.untracked.PSet(
        nFields = cms.untracked.int32(8),
        calibConstGranularity = cms.untracked.string('bySL')
    ),
    outputFileName = cms.untracked.string(GLOBALTAG+"_"+str(RUN)+'_ttrig.txt')
)


process.dumpVdToFile = cms.EDAnalyzer("DumpDBToFile",
    dbToDump = cms.untracked.string('VDriftDB'),
    dbLabel = cms.untracked.string(''),
    calibFileConfig = cms.untracked.PSet(
        nFields = cms.untracked.int32(8),
        calibConstGranularity = cms.untracked.string('bySL')
    ),
    outputFileName = cms.untracked.string(GLOBALTAG+"_"+str(RUN)+'_vdrift.txt')
)


process.p1 = cms.Path(process.dumpT0ToFile)
process.p2 = cms.Path(process.dumpTTrigToFile)
process.p3 = cms.Path(process.dumpVdToFile)



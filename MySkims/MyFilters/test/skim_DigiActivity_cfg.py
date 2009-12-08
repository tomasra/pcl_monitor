import FWCore.ParameterSet.Config as cms

process = cms.Process("DTSKIM1")

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.DigiToRaw_cff")
process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
process.load('Configuration.StandardSequences.VtxSmearedEarly10TeVCollision_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.GlobalTag.globaltag = 'GR09_E_V6::All'

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
'file:/data/c/cerminar/Skim/r123596_V01/Skim_V01_10.root',
'file:/data/c/cerminar/Skim/r123596_V01/Skim_V01_5.root',
'file:/data/c/cerminar/Skim/r123596_V01/Skim_V01_9.root',
'file:/data/c/cerminar/Skim/r123596_V01/Skim_V01_11.root',
'file:/data/c/cerminar/Skim/r123596_V01/Skim_V01_7.root',
'file:/data/c/cerminar/Skim/r123596_V01/Skim_V01_12.root',
'file:/data/c/cerminar/Skim/r123596_V01/Skim_V01_14.root',
'file:/data/c/cerminar/Skim/r123596_V01/Skim_V01_6.root',
'file:/data/c/cerminar/Skim/r123596_V01/Skim_V01_3.root',
'file:/data/c/cerminar/Skim/r123596_V01/Skim_V01_8.root',
'file:/data/c/cerminar/Skim/r123596_V01/Skim_V01_4.root',
'file:/data/c/cerminar/Skim/r123596_V01/Skim_V01_2.root',
)
)


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)


#process.load('FWCore.MessageService.MessageLogger_cfi')
#from FWCore.MessageLogger.MessageLogger_cfi import *
# message logger
# process.MessageLogger = cms.Service("MessageLogger",
#                                     destinations = cms.untracked.vstring('cout'),
#                                     cout = cms.untracked.PSet(threshold = cms.untracked.string('INFO'))
#                                     )


# message logger
process.MessageLogger = cms.Service("MessageLogger",
                                    debugModules = cms.untracked.vstring('*'),
                                    destinations = cms.untracked.vstring('cout'),
                                    categories = cms.untracked.vstring('FwkSummary'),
                                    cout = cms.untracked.PSet(threshold = cms.untracked.string('INFO'),
                                                              DEBUG = cms.untracked.PSet(
                                                                    limit = cms.untracked.int32(0)),
                                                              INFO = cms.untracked.PSet(
                                                                    limit = cms.untracked.int32(0)),
                                                              FwkSummary = cms.untracked.PSet(
                                                                    limit = cms.untracked.int32(-1))
                                                              )
                                    )




process.load("ISpy/Analyzers/ISpy_Producer_cff")

process.add_(
    cms.Service("ISpyService",
                outputFileName = cms.untracked.string('Skim_V01.ig'),
                online = cms.untracked.bool(False),
                debug = cms.untracked.bool(True)
    )
)

#-------------------------------------------------------------------------------------------
# filters

process.dtNDigiFilter = cms.EDFilter("DTNDigiFilter",
    threshold = cms.untracked.int32(10),
    debug = cms.untracked.bool(True),
    dtDigiLabel = cms.InputTag("muonDTDigis"),
    granularity = cms.untracked.string('perChamber'),
    cutType = cms.untracked.string('moreThan')
)

# filter on L1 trigger bits:
# select only events triggered by muon L1A
process.load("L1Trigger.Skimmer.l1Filter_cfi")
process.l1Filter.algorithms = cms.vstring('L1_SingleMuOpen', 'L1_SingleMu0', 'L1_SingleMu3', 'L1_SingleMu5', 'L1_SingleMu7', 'L1_SingleMu10', 'L1_SingleMu14', 'L1_SingleMu20', 'L1_DoubleMuOpen', 'L1_DoubleMu3')



process.hltL1sL1BPTX = cms.EDFilter("HLTLevel1GTSeed",
                                    L1UseL1TriggerObjectMaps = cms.bool(True),
                                    L1NrBxInEvent = cms.int32(3),
                                    L1TechTriggerSeeding  = cms.bool(True),
                                    L1UseAliasesForSeeding  = cms.bool(True),
                                    L1SeedsLogicalExpression = cms.string("0 OR 1 OR 2 OR 3"),
                                    L1GtReadoutRecordTag = cms.InputTag("gtDigis"),
                                    L1GtObjectMapTag = cms.InputTag("gtObjectMap"),
                                    L1CollectionsTag = cms.InputTag("l1extraParticles"),
                                    L1MuonCollectionTag = cms.InputTag("l1extraParticles")
                                    )

process.load('L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskTechTrigConfig_cff')

#process.load('HLTrigger/HLTfilters/hltLevel1GTSeed_cfi')
#process.hltLevel1GTSeed.L1TechTriggerSeeding = cms.bool(True)
#process.hltLevel1GTSeed.L1SeedsLogicalExpression = cms.string('32 OR 33 OR 34 OR 35 OR 36 OR 37 OR 38 OR 39 OR 40 OR 41 OR 42 OR 43')

process.hltL1sL1BSC = cms.EDFilter("HLTLevel1GTSeed",
    L1SeedsLogicalExpression = cms.string('32 OR 33 OR 34 OR 35 OR 36 OR 37 OR 38 OR 39 OR 40 OR 41 OR 42 OR 43'),
    L1MuonCollectionTag = cms.InputTag("l1extraParticles"),
    L1UseL1TriggerObjectMaps = cms.bool(True),
    L1UseAliasesForSeeding = cms.bool(True),
    L1GtReadoutRecordTag = cms.InputTag("gtDigis"),
    L1CollectionsTag = cms.InputTag("l1extraParticles"),
    L1NrBxInEvent = cms.int32(3),
    L1GtObjectMapTag = cms.InputTag("gtObjectMap"),
    L1TechTriggerSeeding = cms.bool(True)
)

process.dtHLTActivity = cms.EDFilter("HLTHighLevel",
    eventSetupPathsKey = cms.string(''),
    andOr = cms.bool(True),
    HLTPaths = cms.vstring('HLT_Activity_DT'),
    throw = cms.bool(False),
    TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")
)


process.largeSiStripClusterEvents = cms.EDFilter("LargeSiStripClusterEvents",
    absoluteThreshold = cms.untracked.int32(50),
    collectionName = cms.InputTag("siStripClusters"),
    moduleThreshold = cms.untracked.int32(1000)
)


#-------------------------------------------------------------------------------------------


process.load("DQM.DTOfflineAnalysis.muonAnalysis_cff")

# process.dtBPTX = cms.Path(process.hltL1sL1BPTX*
#                          process.muonDTDigis*
#                          process.dtNDigiFilter*
#                          process.largeSiStripClusterEvents*
#                          process.iSpy_sequence)

process.dtBSC = cms.Path(process.hltL1sL1BSC*
                         process.muonDTDigis*
                         process.largeSiStripClusterEvents*
                         process.dtNDigiFilter*
                         process.muonAnalysis*
                         process.iSpy_sequence)


process.dtHLTAct = cms.Path(process.dtHLTActivity*
                            process.muonDTDigis*
                            process.largeSiStripClusterEvents*
                            process.muonAnalysis*
                            process.iSpy_sequence)


# process.p3 = cms.Path(process.RawToDigi)
# process.p4 = cms.Path(process.reconstruction)

# process.schedule = cms.Schedule(process.p3,process.p4,process.iSpy)

process.out1 = cms.OutputModule("PoolOutputModule",
                                fileName = cms.untracked.string('Skim_V01.root'),
                                SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('dtBSC', 
                                                                                             'dtHLTAct')
                                                                  )
                                )
 


process.output = cms.EndPath(process.out1)


process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
    )

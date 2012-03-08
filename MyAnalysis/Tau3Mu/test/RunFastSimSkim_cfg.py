# Auto generated configuration file
# using: 
# Revision: 1.341 
# Source: /cvs/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: MinBias_TuneZ2_DsTau3Mu -s FASTSIM,HLT:GRun --geometry DB --datatier GEN-SIM-DIGI-RECO --conditions START44_V7::All -n 10000 --eventcontent AODSIM --pileup=HighLumiPileUp --filein pippo.root --no_exec
import FWCore.ParameterSet.Config as cms

process = cms.Process('SKIM')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('FastSimulation.Configuration.EventContent_cff')
process.load('FastSimulation.PileUpProducer.PileUpSimulator_HighLumiPileUp_cff')
process.load('FastSimulation.Configuration.Geometries_START_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('FastSimulation.Configuration.FamosSequences_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedParameters_cfi')
process.load('FastSimulation.Configuration.HLT_GRun_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(300)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
    fileNames = cms.untracked.vstring(
'file:/data1/Tau3Mu/52X/GEN/DsTau3Mu_GEN/DsTau3Mu_000.root',
'file:/data1/Tau3Mu/52X/GEN/DsTau3Mu_GEN/DsTau3Mu_001.root',
'file:/data1/Tau3Mu/52X/GEN/DsTau3Mu_GEN/DsTau3Mu_002.root',
)
)

process.options = cms.untracked.PSet(
	wantSummary = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.3 $'),
    annotation = cms.untracked.string('MinBias_TuneZ2_DsTau3Mu nevts:10000'),
    name = cms.untracked.string('PyReleaseValidation')
)

# Output definition

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    fileName = cms.untracked.string('/tmp/cerminar/MinBias_TuneZ2_DsTau3Mu_cff_py_GEN.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-RAW')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('HLT_Tau2Mu_RegPixTrack_v1')
    )
)


# Additional output definition

# Other statements
process.famosSimHits.SimulateCalorimetry = True
process.famosSimHits.SimulateTracking = True
process.simulation = cms.Sequence(process.simulationWithFamos)
process.HLTEndSequence = cms.Sequence(process.reconstructionWithFamos)
process.Realistic7TeV2011CollisionVtxSmearingParameters.type = cms.string("BetaFunc")
process.famosSimHits.VertexGenerator = process.Realistic7TeV2011CollisionVtxSmearingParameters
process.famosPileUp.VertexGenerator = process.Realistic7TeV2011CollisionVtxSmearingParameters
process.GlobalTag.globaltag = 'START52_V1::All'

# Path and EndPath definitions
process.genLevelAnalysis = cms.EDAnalyzer('GenLevelAnalysis')
process.load("MyAnalysis.Tau3Mu.triggerProdAnalysis_cfi")
process.reconstruction = cms.Path(process.reconstructionWithFamos)
process.AODSIMoutput_step = cms.EndPath(process.RAWSIMoutput)



# Schedule definition
process.schedule = cms.Schedule()
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.reconstruction,process.AODSIMoutput_step])


# process.TFileService = cms.Service("TFileService",
#                                    fileName = cms.string("file:/tmp/cerminar/GenLevelAnalysis.root"),
#                                    closeFileFast = cms.untracked.bool(True)
#                                    )

# L1 emulator: override L1 menu and change the seeding
import L1Trigger.Configuration.L1Trigger_custom
process = L1Trigger.Configuration.L1Trigger_custom.customiseL1Menu(process)
process.hltL1sL1DoubleMu0HighQ.L1SeedsLogicalExpression = 'L1_DoubleMu0er_HighQ'
#process.hltDimuonL1HQ2p1Filtered0.MaxEta = 3.0
# # message logger
# process.MessageLogger = cms.Service("MessageLogger",
#                                     debugModules = cms.untracked.vstring('*'),
#                                     destinations = cms.untracked.vstring('cout'),
#                                     categories = cms.untracked.vstring('HLTMuonDimuonL3Filter'),
#                                     cout = cms.untracked.PSet(threshold = cms.untracked.string('DEBUG'),
#                                                               noLineBreaks = cms.untracked.bool(False),
#                                                               DEBUG = cms.untracked.PSet(
#                                                                       limit = cms.untracked.int32(-1)),
#                                                               INFO = cms.untracked.PSet(
#                                                                       limit = cms.untracked.int32(0)),
#                                                               HLTMuonDimuonL3Filter = cms.untracked.PSet(limit = cms.untracked.int32(-1))
#                                                               )
#                                     )
                                                

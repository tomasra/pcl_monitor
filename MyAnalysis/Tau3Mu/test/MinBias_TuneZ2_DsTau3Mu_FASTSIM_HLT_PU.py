# Auto generated configuration file
# using: 
# Revision: 1.341 
# Source: /cvs/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: MinBias_TuneZ2_DsTau3Mu -s FASTSIM,HLT:GRun --geometry DB --datatier GEN-SIM-DIGI-RECO --conditions START44_V7::All -n 10000 --eventcontent AODSIM --pileup=HighLumiPileUp --filein pippo.root --no_exec
import FWCore.ParameterSet.Config as cms

process = cms.Process('HLT')

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
    input = cms.untracked.int32(200)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
    fileNames = cms.untracked.vstring(
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_000.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_001.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_002.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_003.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_004.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_005.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_006.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_007.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_008.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_009.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_010.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_011.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_012.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_014.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_015.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_016.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_017.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_018.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_019.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_020.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_021.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_022.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_023.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_024.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_025.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_026.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_027.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_028.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_029.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_030.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_031.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_032.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_033.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_034.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_035.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_036.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_037.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_038.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_039.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_040.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_041.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_042.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_043.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_044.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_045.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_046.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_047.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_048.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_050.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_051.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_052.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_053.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_057.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_058.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_060.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_061.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_062.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_063.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_064.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_065.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_066.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_067.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_068.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_069.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_070.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_071.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_072.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_073.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_074.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_075.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_076.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_077.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_078.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_079.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_080.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_081.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_082.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_083.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_084.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_085.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_086.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_088.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_089.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_090.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_091.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_093.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_094.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_095.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_096.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_097.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_098.root',
'file:/data1/Tau3Mu/FastSim/DsTau3Mu_GEN_v1/DsTau3Mu_099.root',
)
)

process.options = cms.untracked.PSet(
	wantSummary = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    annotation = cms.untracked.string('MinBias_TuneZ2_DsTau3Mu nevts:10000'),
    name = cms.untracked.string('PyReleaseValidation')
)

# Output definition

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    outputCommands = process.AODSIMEventContent.outputCommands,
    fileName = cms.untracked.string('file:/tmp/guiducci/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RECO')
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
process.GlobalTag.globaltag = 'START44_V7::All'

# Path and EndPath definitions
process.genLevelAnalysis = cms.EDAnalyzer('GenLevelAnalysis')
process.reconstruction = cms.Path(process.reconstructionWithFamos)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput+process.genLevelAnalysis)



# Schedule definition
process.schedule = cms.Schedule()
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.reconstruction,process.AODSIMoutput_step])


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("file:/tmp/guiducci/GenLevelAnalysis.root"),
                                   closeFileFast = cms.untracked.bool(True)
                                   )

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
                                                

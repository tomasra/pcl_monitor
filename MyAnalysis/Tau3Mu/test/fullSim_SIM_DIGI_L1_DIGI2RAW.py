# Auto generated configuration file
# using: 
# Revision: 1.366 
# Source: /local/reps/CMSSW.admin/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: fullSimRaw -s SIM,DIGI,L1,DIGI2RAW --filein pippo.root --conditions START52_V2A::All --no_exec --eventcontent GENRAW -n -1 --datatier GEN-SIM-RAW --geometry DB
import FWCore.ParameterSet.Config as cms

process = cms.Process('DIGI2RAW')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
    fileNames = cms.untracked.vstring('file:/data1/Tau3Mu/52X/GEN/SKIM/v4_DsTau3Mu-GEN/Skim_GEN_11.root')
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.366 $'),
    annotation = cms.untracked.string('fullSimRaw nevts:-1'),
    name = cms.untracked.string('PyReleaseValidation')
)

# Output definition

process.GENRAWoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.GENRAWEventContent.outputCommands,
    fileName = cms.untracked.string('fullSimRaw_SIM_DIGI_L1_DIGI2RAW.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-RAW')
    )
)

# Additional output definition

# Other statements
process.GlobalTag.globaltag = 'START52_V2A::All'

# Path and EndPath definitions
process.simulation_step = cms.Path(process.psim)
process.digitisation_step = cms.Path(process.pdigi)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.GENRAWoutput_step = cms.EndPath(process.GENRAWoutput)

# Schedule definition
process.schedule = cms.Schedule(process.simulation_step,process.digitisation_step,process.L1simulation_step,process.digi2raw_step,process.endjob_step,process.GENRAWoutput_step)


import L1Trigger.Configuration.L1Trigger_custom
process = L1Trigger.Configuration.L1Trigger_custom.customiseL1Menu(process)
#process.hltL1sL1DoubleMu0HighQ.L1SeedsLogicalExpression = 'L1_DoubleMu0er_HighQ'

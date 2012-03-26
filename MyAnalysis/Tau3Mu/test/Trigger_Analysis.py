
import FWCore.ParameterSet.Config as cms

process = cms.Process('TRIGANA')

# import of standard configurations
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
    fileNames = cms.untracked.vstring(
    "/store/caf/user/fiori/outputFULL_Tau3Mu.root"
    )
)

process.options = cms.untracked.PSet(
     #wantSummary = cms.untracked.bool( True )

)


# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RECOSIMEventContent.outputCommands,
    fileName = cms.untracked.string('TrigAna.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('')
    )
)

# Additional output definition

process.ana = cms.EDAnalyzer('TriggerProdAnalysis',

OutFileName=cms.string("/tmp/fiori/RecoFullsim_Tau3Mu_L2Skim.root"),

)


# Other statements
process.GlobalTag.globaltag = 'START52_V4A::All'# was V2

# Path and EndPath definitions
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("TriggerAnalysis.root"),
                                   closeFileFast = cms.untracked.bool(True)
                                   )

process.ana_step = cms.Path(process.ana)







# Auto generated configuration file
# using: 
# Revision: 1.366 
# Source: /local/reps/CMSSW.admin/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: -s RAW2DIGI,RECO --mc --conditions auto:startup --eventcontent RECOSIM -n 10 --no_exec --filein rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L3skim/ReRunHLT_0.root
import FWCore.ParameterSet.Config as cms

process = cms.Process('RECO')

# import of standard configurations
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
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
    "file:/tmp/fiori/outputFULL.root"
#    'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_0.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_1.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_10.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_11.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_12.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_13.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_14.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_15.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_16.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_17.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_19.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_2.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_20.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_21.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_22.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_23.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_24.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_3.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_5.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_6.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_7.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_8.root',
#'rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_L2skim_actualSkim/ReRunHLT_9.root'
    )
)

process.options = cms.untracked.PSet(
     wantSummary = cms.untracked.bool( True )

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.366 $'),
    annotation = cms.untracked.string('s nevts:10'),
    name = cms.untracked.string('PyReleaseValidation')
)

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RECOSIMEventContent.outputCommands,
    fileName = cms.untracked.string('recoAna.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('')
    )
)

# Additional output definition

process.ana = cms.EDAnalyzer('Tau3MuAnalysis',

OutFileName=cms.string("/tmp/fiori/RecoFullsim_Tau3Mu_L2Skim.root"),

Debug=cms.bool(False),

IsMC=cms.bool(True),     #Be sure you run on MC otherwise you get a crash!
isSignal=cms.bool(True), #If true the gen matching is done on Signal else on Norm. sample

OnlyOppositeChargeMuons=cms.bool(False), #False for tau->3mu, True for Ds->phi pi

DiMuMassMin= cms.double(0.2),
DiMuMassMax= cms.double(1.7),#1.8

DiMuLxyMin= cms.double(-100),
DiMuLxyMax= cms.double(500),
DiMuLxySigMin= cms.double(-100.),

DiMuVtxChi2Max= cms.double(200),
DiMuVprobMin=cms.double(0.),

GuessForTrackMass=cms.double(0.1057), #Guess for the mass of the track | 0.1396 pion | 0.1057 muon |

DiMuTrackMassMin= cms.double(1.6),
DiMuTrackMassMax= cms.double(2.0),

DiMuTrackLxyMin= cms.double(-100),
DiMuTrackLxyMax= cms.double(700),
DiMuTrackLxySigMin= cms.double(-100.), 

DiMuTrackVtxChi2Max= cms.double(200),
DiMuTrackVprobMin=cms.double(0),

Trackd0Max= cms.double(5000),
Trackd0SigMin= cms.double(-100.),

MuPTCut=cms.double(1.0),
TrackPTCut=cms.double(.5),

MaxDrForTrackCount=cms.double(0.5),#not a real cut, is only for plotting

HLT_paths = cms.vstring( # noting means passtrough
#"HLT_Dimuon0_Omega_Phi_v3",
"HLT_Tau2Mu_L2MuonCandidates",
"HLT_Tau2Mu_ItTrack_v1",
"HLT_Tau2Mu_L3MuonCandidates",
"HLT_Tau2Mu_MuMuVtx"
),

HLT_process = cms.string("HLTX")

)


# Other statements
process.GlobalTag.globaltag = 'START52_V4A::All'# was V2

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.reconstruction_step = cms.Path(process.reconstruction*process.ana)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.reconstruction_step,process.endjob_step)#,process.RECOSIMoutput_step)


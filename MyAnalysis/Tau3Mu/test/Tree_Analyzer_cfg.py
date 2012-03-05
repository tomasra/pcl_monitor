import FWCore.ParameterSet.Config as cms

process = cms.Process('GenLevel')

process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.GlobalTag.globaltag = 'START52_V2A::All'

# Source
process.source = cms.Source("PoolSource",
fileNames = cms.untracked.vstring(
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_000.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_001.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_002.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_003.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_004.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_005.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_006.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_007.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_008.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_009.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_010.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_011.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_012.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_013.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_014.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_015.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_016.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_017.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_018.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_019.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_020.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_021.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_022.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_023.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_024.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_025.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_026.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_027.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_028.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_029.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_030.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_031.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_032.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_033.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_034.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_035.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_036.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_037.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_038.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_039.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_040.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_041.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_042.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_043.root",
##"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_044.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_045.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_046.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_047.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_048.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_049.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_050.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_051.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_052.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_053.root",
#"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_054.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_055.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_056.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_057.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_058.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_059.root",
#"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_060.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_061.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_062.root",
##"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_063.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_064.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_065.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_066.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_067.root",
#"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_068.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_069.root",
#"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_070.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_071.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_072.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_073.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_074.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_075.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_076.root",
#"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_077.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_078.root",
#"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_079.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_080.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_081.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_082.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_083.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_084.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_085.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_086.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_087.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_088.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_089.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_090.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_091.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_092.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_093.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_094.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_095.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_096.root",
#"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_097.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_098.root",
"rfio:/castor/cern.ch/user/g/guiducci/Tau3Mu/52x/DsTau3Mu_FASTSIM/MinBias_TuneZ2_DsTau3Mu_FASTSIM_HLT_PU_099.root"
#
       
    )
)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(300))

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

process.ana = cms.EDAnalyzer('Tau3MuAnalysis',

OutFileName=cms.string("OUT_Tree_Azzo.root"),

Debug=cms.bool(False),

SaveOnlyGenMatchedVar=cms.bool(True),

OnlyOppositeChargeMuons=cms.bool(False), #False for tau->3mu, True for Ds->phi pi

DiMuMassMin= cms.double(0.0),
DiMuMassMax= cms.double(1.8),#1.8

DiMuLxyMin= cms.double(-10),
DiMuLxySigMin= cms.double(-10),

DiMuVtxChi2Max= cms.double(100),
DiMuVprobMin=cms.double(0.00),

GuessForTrackMass=cms.double(0.1057), #Guess for the mass of the track | 0.1396 pion | 0.1057 muon |

DiMuTrackMassMin= cms.double(1.6),
DiMuTrackMassMax= cms.double(2.3),

DiMuTrackLxyMin= cms.double(-10), #for now not used
DiMuTrackLxySigMin= cms.double(-10), #for now not used

DiMuTrackVtxChi2Max= cms.double(100),
DiMuTrackVprobMin=cms.double(0.0),

Trackd0Max= cms.double(100),
Trackd0SigMin= cms.double(-10),

MuPTCut=cms.double(1.0),
TrackPTCut=cms.double(0.5),

MaxDrForTrackCount=cms.double(0.5),

HLT_paths = cms.vstring( # noting means passtrough
#"HLT_Dimuon0_Omega_Phi_v3",
#"HLT_Dimuon0_Omega_Phi_v4"
#"HLT_Tau2Mu_RegPixTrack_v1"
),

HLT_process = cms.string("HLT")

)


process.analysisPath = cms.Path(process.ana)

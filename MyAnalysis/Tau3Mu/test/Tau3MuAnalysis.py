import FWCore.ParameterSet.Config as cms

process = cms.Process('GenLevel')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.Services_cff')
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.GlobalTag.globaltag ="START52_V11::All"
#"START52_V11::All"
#'GR_P_V39::All'
process.MessageLogger = cms.Service("MessageLogger",
     cout = cms.untracked.PSet(
         threshold = cms.untracked.string('WARNING')
     ),
     destinations = cms.untracked.vstring('cout')
)

# Source
process.source = cms.Source("PoolSource",
fileNames = cms.untracked.vstring(
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_10_1_If0.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_10_1_N8t.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_10_1_oAu.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_11_1_GYM.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_12_1_1pH.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_13_1_4A7.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_14_1_p6N.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_15_1_8KK.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_16_1_wen.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_17_1_3eP.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_18_1_R5r.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_19_1_88c.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_1_1_1tl.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_1_1_JEN.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_1_1_Pfb.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_1_1_jDk.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_20_1_BQM.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_21_1_PXv.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_22_1_Em3.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_23_1_kEV.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_24_1_xXy.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_25_1_vzK.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_26_1_yfv.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_27_1_LUg.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_28_1_jSg.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_29_1_NRk.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_2_1_cTO.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_2_1_mDQ.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_2_1_yrK.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_30_1_lEM.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_3_1_TbI.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_3_1_fkX.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_4_1_Y5X.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_4_1_sA3.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_5_1_8Kc.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_5_1_lzv.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_5_1_nbS.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_6_1_Fqs.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_6_1_Y80.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_6_1_agm.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_7_1_43M.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_7_1_iQM.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_7_1_kSf.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_8_1_H9U.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_8_1_jbD.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_8_1_tf6.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_9_1_kpZ.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_9_1_sGe.root",
#"/store/caf/user/guiducci/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/MinBias_TuneZ2_DsPhiTo2MuPhi_v1/91497683f71fb3fd1629db65b303c81d/MinBias_TuneZ2_DsPhiTo2MuPhi_2Mu_cff_py_GEN_FASTSIM_HLT_PU_9_1_wC3.root"
"/store/caf/user/fiori/Tau3Mu_RECO.root"
#
)
)


#process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange('190645:10-190645:110')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

process.ana = cms.EDAnalyzer('Tau3MuAnalysis_V2',

OutFileName=cms.string("OUT_DATA.root"),

Debug=cms.bool(False),

IsMC=cms.bool(True),     #Be sure you run on MC otherwise you get a crash!

isSignal=cms.bool(True), #If true the gen matching is done on Signal else on Norm. sample
isBackground=cms.bool(False),

DiMuMassMin= cms.double(0.6),  # 
DiMuMassMax= cms.double(1.7),#

DiMuLxyMin= cms.double(-100),
DiMuLxyMax= cms.double(500),
DiMuLxySigMin= cms.double(1.),

DiMuVtxChi2Max= cms.double(20),
DiMuVprobMin=cms.double(0.1),

DiMuCosPointMin=cms.double(0.5),
DiMuTrackCosPointMin=cms.double(0.98),

GuessForTrackMass=cms.double(0.1), #Guess for the mass of the track | 0.1396 pion | 0.1057 muon |

DiMuTrackMassMin= cms.double(1.7),
DiMuTrackMassMax= cms.double(2.0),

DiMuTrackLxyMin= cms.double(-100),
DiMuTrackLxyMax= cms.double(700),
DiMuTrackLxySigMin= cms.double(1.), 

DiMuTrackVtxChi2Max= cms.double(20),
DiMuTrackVprobMin=cms.double(0.1),

MuPTCut=cms.double(1.0),
TrackPTCut=cms.double(.5),

HLT_paths = cms.vstring( # noting means passtrough
"HLT_Tau2Mu_ItTrack"
),

HLT_process = cms.string("HLTX")

)

process.analysisPath = cms.Path(process.ana)

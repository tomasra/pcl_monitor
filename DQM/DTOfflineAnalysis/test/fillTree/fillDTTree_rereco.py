import FWCore.ParameterSet.Config as cms

######################################################################

isMC = True              #True for MC

reReco = True            #re-reconstruct segments; if true:
skipDeltaSuppr = True    #skip DRR
ALIGNMENT = ""           #alignment DB to use
doAngleCorr = False      #apply angle correction (experimental)

######################################################################
import os
print 'Working in: ', os.environ['CMSSW_BASE']

process = cms.Process("DTOffAna")

# the source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#---
#    process.GlobalTag.globaltag = "START53_V7G::All"
#                                 '/store/relval/CMSSW_5_3_6-START53_V14/RelValZMM/GEN-SIM-RECO/v2/00000/08C1D822-F629-E211-A6B1-003048679188.root',
#                                 '/store/relval/CMSSW_5_3_6-START53_V14/RelValZMM/GEN-SIM-RECO/v2/00000/76156813-F529-E211-917B-003048678FA6.root'
#---
#                                 '/store/relval/CMSSW_6_2_0_pre6_patch1/RelValZMM/GEN-SIM-RECO/PRE_ST62_V6-v1/00000/1A1EDFF1-D5BE-E211-AE75-003048FFCB9E.root',
#                                 '/store/relval/CMSSW_6_2_0_pre6_patch1/RelValZMM/GEN-SIM-RECO/PRE_ST62_V6-v1/00000/3E430421-D9BE-E211-B2EB-0026189438A2.root'
#--
                                
    )                        
#    duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

################### Set input samples

#execfile("files_ZMu-22Jan2013-v1.py")                                    # Data
#execfile("files_DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball.py")    # Z MC
execfile("files_RelValZMM5312.py")                                       # Z RelVal, 5X
#execfile("files_RelValZMM700p4.py")                                      # Z RelVal, 7X

# Override GT set in flies above to use IDEAL MC
#    process.GlobalTag.globaltag = "MC_53_V7A::All"  # IDEAL MC

###################

process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*", "drop L1GlobalTriggerObjectMapRecord_hltL1GtObjectMap__HLT", "drop l1extra*_*_*_*")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )


process.load("DQM.DTOfflineAnalysis.dtLocalRecoAnalysis_cfi")


process.load('Configuration/StandardSequences/MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration/Geometry/GeometryIdeal_cff')


#if CALIBRATION != "" :
#process.GlobalTag.toGet = cms.VPSet(
#    cms.PSet(record = cms.string("DTTtrigRcd"),
#             tag = cms.string("ttrig"),
#             connect = cms.untracked.string("sqlite_file:Data_v5.db"))
#    cms.PSet(record = cms.string("DTMtimeRcd"),
#             tag = cms.string("vdrift"),
#             connect = cms.untracked.string("sqlite_file:vdrift_543_v5s1_statByLayer_sigma_a.db"))
#)

### Non-standard DB alignment
#DTGeom16May_Design.db --> internal alignment nominale
#DTGeom16May_SL.db     --> superlayer corrections
#DTGeom16May_Layer.db  --> layer to layer corrections
#

if ALIGNMENT != "" :
    import CondCore.DBCommon.CondDBSetup_cfi
    process.muonAlignment = cms.ESSource("PoolDBESSource",
                                      connect = cms.string("sqlite_file:"+ALIGNMENT),

                                      DBParameters = CondCore.DBCommon.CondDBSetup_cfi.CondDBSetup.DBParameters,
                                      toGet = cms.VPSet(cms.PSet(record = cms.string("DTAlignmentRcd"),
                                                                 tag =  cms.string("DTAlignmentRcd")),
                                                        cms.PSet(record = cms.string("DTAlignmentErrorRcd"),
                                                                 tag =  cms.string("DTAlignmentErrorRcd"))
                                                        )
                                      )
    process.es_prefer_muonAlignment = cms.ESPrefer("PoolDBESSource","muonAlignment")
### 


process.load("Configuration/StandardSequences/RawToDigi_Data_cff")
process.load("Configuration/StandardSequences/Reconstruction_cff")
#process.load('Configuration/EventContent/EventContent_cff')



# message logger
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
#suppress message: "Failed to get  TEV refits, fall back to sigma switch."
process.MessageLogger.suppressWarning= cms.untracked.vstring('muons1stStep')

process.goodPrimaryVertices = cms.EDFilter("VertexSelector",
  src = cms.InputTag("offlinePrimaryVertices"),
  cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2"),
  filter = cms.bool(True),
)

if (skipDeltaSuppr) :
    process.dt4DSegments.Reco4DAlgoConfig.perform_delta_rejecting = False;
    process.dt4DSegments.Reco4DAlgoConfig.Reco2DAlgoConfig.perform_delta_rejecting = False;

if (doAngleCorr) :
    process.dt4DSegments.Reco4DAlgoConfig.recAlgoConfig.doAngleCorr = True;
    process.dt4DSegments.Reco4DAlgoConfig.Reco2DAlgoConfig.doAngleCorr = True; # FIXME: hit recomputation @step2 is not activated!


process.dtLocalRecoAnal.rootFileName = 'DTLocalReco.root'

if (reReco) :
    ### redigi, from RAW
#    process.jobPath = cms.Path(process.goodPrimaryVertices*process.muonDTDigis*process.dtlocalreco+process.dt2DSegments+process.muonreco+process.dtLocalRecoAnal)
    ### re-reconstruct segments from rechits
    process.jobPath = cms.Path(process.goodPrimaryVertices*process.dt4DSegments+process.muonreco+process.dtLocalRecoAnal)
else :
    process.jobPath = cms.Path(process.goodPrimaryVertices*process.dtLocalRecoAnal)

if (False) :
    process.load("DQMServices.Core.DQMStore_cfg")
    process.load("DQMServices.Components.DQMEnvironment_cfi")
    process.dqmSaver.convention = 'Offline'
    # FIXME: correct this
    process.dqmSaver.workflow = '/Cosmics/CMSSW_2_2_X-Testing/RECO'      

    process.load("Validation.DTRecHits.DTRecHitQualityAll_cfi")
    process.load("Validation.DTRecHits.DTRecHitClients_cfi")
##process.rechivalidation.doStep2 = False
# process.rechivalidation.recHitLabel = 'hltDt1DRecHits'
# process.rechivalidation.segment4DLabel = 'hltDt4DSegments'
# process.seg2dsuperphivalidation.segment4DLabel = 'hltDt4DSegments'
# process.seg4dvalidation.segment4DLabel = 'hltDt4DSegments'

    process.validation = cms.Sequence(process.dtLocalRecoValidation_no2D)
    process.clients = cms.Sequence(process.dtLocalRecoValidationClients)
    process.p = cms.Path(process.validation + process.dqmSaver)


#     process.jobPath.insert(process.jobPath.index(process.dtLocalRecoAnal),
#                            process.dtLocalRecoValidation_no2D+
#                            process.dtLocalRecoValidationClients+
#                            process.dqmSaver
#                            )
#     print process.jobPath

process.options = cms.untracked.PSet(
#    wantSummary = cms.untracked.bool(True)
    fileMode = cms.untracked.string('NOMERGE')
    )

# process.out = cms.OutputModule(
#     "PoolOutputModule",
#     fileName = cms.untracked.string('test.root'),
#     outputCommands =  cms.untracked.vstring(
#             'keep *',
#         )
#     #SelectEvents = cms.untracked.PSet(
#     #SelectEvents = cms.vstring('path')
#     #)
#     )
# process.outp = cms.EndPath(process.out)


# f = file('configuratiodump_cfg.py', 'w')
# f.write(process.dumpPython())
# f.close()

if (not isMC) :
    execfile("json_2012.py")


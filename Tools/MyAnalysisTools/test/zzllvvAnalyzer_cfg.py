import FWCore.ParameterSet.Config as cms

process = cms.Process("HtoZZto2l2nu")

from CMGTools.HtoZZ2l2nu.localPatTuples_cff import *
process.source = cms.Source("PoolSource",
#                            fileNames = getLocalSourceFor('GluGluToHToZZTo2L2NuM400'),
                            inputCommands = cms.untracked.vstring('keep *',
                                                                  'drop *_MEtoEDMConverter_*_*'),
                            fileNames = cms.untracked.vstring('/store/cmst3/user/cerminar/ZZllvv_sel3/DYJetsToLL_PU2010/patTuple_99_1_mox.root')
                            )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.load('CMGTools.HtoZZ2l2nu.NormalizationCounter_cfi')
process.load('CMGTools.HtoZZ2l2nu.CleanEventProducer_cfi')
process.load('CMGTools.HtoZZ2l2nu.CleanEventFilter_cfi')
process.load('CMGTools.HtoZZ2l2nu.CleanEventAnalyzer_cfi')


from CMGTools.HtoZZ2l2nu.StandardSelections_cfi import *
process.zzllvvAnalyzer = cms.EDAnalyzer("ZZllvvAnalyzer",
                                        fileName = cms.untracked.string('ZZllvvAnalyzer.root'),
                                        source = cms.untracked.InputTag("cleanEvent"),
                                        zmmInput = cms.untracked.InputTag("zMMCand"),
                                        debug = cms.untracked.bool(False)
                                        #Generator = BaseGeneratorSelection.clone(),
                                        Vertices = BaseVertexSelection.clone(),
                                        #Muons = BaseMuonsSelection.clone(),
                                        #Electrons = BaseElectronsSelection.clone(),
                                        #Dileptons = BaseDileptonSelection.clone(),
                                        #Jets = BaseJetSelection.clone(),
                                        #MET = BaseMetSelection.clone()
                                        )





process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('/tmp/evHyp.root'),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      'keep *_MEtoEDMConverter_*_*',
                                                                      'keep edmMergeableCounter_*_*_*',#FIXME: useful?
                                                                      'keep *_prunedGen_*_*',
                                                                      'keep *_genEventScale_*_*',
                                                                      'keep GenRunInfoProduct_*_*_*',
                                                                      'keep *_genMetTrue_*_*',
                                                                      'keep *_selectedPat*_*_*',
                                                                      'keep patMETs_*_*_*',
                                                                      'keep double*_*_rho_*',
                                                                      #'keep *_tcMet_*_*',
                                                                      'keep *_pfMet_*_*',
                                                                      'keep *_cleanEvent_*_*'),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') )
                               )
process.p = cms.Path(process.loadNormalizationCounters*process.cleanEvent*process.cleanEventFilter*process.zzllvvAnalyzer)
process.e = cms.EndPath(process.saveNormalizationCounters*process.out)


# message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 500
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    SkipEvent = cms.untracked.vstring('ProductNotFound')
    )



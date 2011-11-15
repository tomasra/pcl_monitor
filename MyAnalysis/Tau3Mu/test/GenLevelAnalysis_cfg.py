import FWCore.ParameterSet.Config as cms

process = cms.Process('GenLevel')


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("GenLevelAnalysis.root"),
                                   closeFileFast = cms.untracked.bool(True)
                                   )

# Source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(#'file:/afs/cern.ch/user/g/guiducci/scratch0/tau3mu/GENsamples/MinBias_TuneZ2_7TeV_pythia6_DsTau3Mu_GEN_1.root'
"file:/afs/cern.ch/user/g/guiducci/scratch0/tau3mu/GENsamples/MinBias_TuneZ2_Ds-Tau-3Mu.root")
                            )
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))



process.genLevelAnalysis = cms.EDAnalyzer('GenLevelAnalysis')

process.analysisPath = cms.Path(process.genLevelAnalysis)

import FWCore.ParameterSet.Config as cms

#---------------------------------------------

#---------------------------------------------

process = cms.Process("ANALYSIS")

process.source = cms.Source("PoolSource",
                            #firstRun = cms.untracked.uint32(10)
                            )


process.source.fileNames = cms.untracked.vstring(
        '/store/cmst3/user/cerminar/Analysis/ZZllvv_v01/sel0/ZJetsPU/cmgTuple_0.root'
)


process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(-1)
)



process.zzllvvAnalyzer = cms.EDAnalyzer("ZZllvvAnalyzer")


#output file for histograms etc
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("histograms.root"))


process.analysisSequence = cms.Sequence(process.zzllvvAnalyzer)

process.p = cms.Path(process.analysisSequence)
#process.MessageLogger.cerr.FwkReport.reportEvery = 100

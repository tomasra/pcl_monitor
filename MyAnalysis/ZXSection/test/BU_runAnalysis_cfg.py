import FWCore.ParameterSet.Config as cms

runProcess = cms.PSet(
    input = cms.string("/data/Analysis/42x/DYJetsToLL.root"),
    outdir = cms.string("./"),
    useFitter=cms.bool(False),
    isMC = cms.bool(True),
    evStart = cms.int32(0),
    evEnd = cms.int32(10000),
    dirName = cms.string("evAnalyzer/data"),
    jobfile = cms.string("./test/xsec_42X.txt"),
    )

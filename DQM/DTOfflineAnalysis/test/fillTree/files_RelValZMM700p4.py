#/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-HLT8E33_PU_S10_START53_V7I-v1/GEN-SIM-RECO

process.GlobalTag.globaltag = "PRE_ST62_V8::All" #used for 7X as well

readFiles = cms.untracked.vstring()

process.source.fileNames = readFiles

readFiles.extend( [
        '/store/relval/CMSSW_7_0_0_pre4/RelValZMM/GEN-SIM-RECO/PRE_ST62_V8-v1/00000/086DEE6A-1325-E311-BEB2-003048FFD752.root',
        '/store/relval/CMSSW_7_0_0_pre4/RelValZMM/GEN-SIM-RECO/PRE_ST62_V8-v1/00000/A8B465D7-1025-E311-B656-003048D3C010.root'
    ] );


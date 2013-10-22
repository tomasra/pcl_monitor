#/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-HLT8E33_PU_S10_START53_V7I-v1/GEN-SIM-RECO

process.GlobalTag.globaltag = "START53_LV2::All" # for 5312

readFiles = cms.untracked.vstring()

process.source.fileNames = readFiles

readFiles.extend( [
       '/store/relval/CMSSW_5_3_12_patch2/RelValZMM/GEN-SIM-RECO/START53_LV2-v1/00000/28D552C4-A82B-E311-952C-002590596486.root',
       '/store/relval/CMSSW_5_3_12_patch2/RelValZMM/GEN-SIM-RECO/START53_LV2-v1/00000/EA8973F4-A92B-E311-A0A6-00261894396D.root'
    ] );


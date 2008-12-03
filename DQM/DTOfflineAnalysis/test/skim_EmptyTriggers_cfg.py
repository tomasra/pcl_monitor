import FWCore.ParameterSet.Config as cms

process = cms.Process("SkimEmptyTriggers")

# the source
process.source = cms.Source("NewEventStreamFileReader",
     fileNames = cms.untracked.vstring(
    'file:GlobalCRAFT1.00071280.0001.A.storageManager.00.0000.dat'
     )
                             )
#process.source.skipEvents = 500000

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
    )



process.load("DQM.DTOfflineAnalysis.dt_dqm_offlineAnalysis_common_cff")

#process.load("DQM.DTOfflineAnalysis.bxDistanceFilter_cfi")
#process.bxDistanceFilter.debug = True

import EventFilter.L1GlobalTriggerRawToDigi.l1GtUnpack_cfi
process.gtDigis = EventFilter.L1GlobalTriggerRawToDigi.l1GtUnpack_cfi.l1GtUnpack.clone()
process.gtDigis.DaqGtInputTag = 'source'


process.load("DQM.DTOfflineAnalysis.triggerSourceFilter_cfi")
process.load("DQM.DTOfflineAnalysis.dtNDigiFilter_cfi")


# message logger
process.MessageLogger = cms.Service("MessageLogger",
                                    destinations = cms.untracked.vstring('cout'),
                                    cout = cms.untracked.PSet(threshold = cms.untracked.string('WARNING'))
                                    )



#process.mySkimBxDistance = cms.Path(process.bxDistanceFilter)

#process.mySkimEmtyTriggers = cms.Path(process.gtDigis * process.triggerSourceFilter * process.dtunpacker + process.dtNDigiFilter)

process.mySkimEmtyTriggers = cms.Path(process.dtunpacker + process.dtNDigiFilter)


process.out1 = cms.OutputModule("PoolOutputModule",
                                #compressionLevel = cms.untracked.int32(9),
                                fileName = cms.untracked.string('SkimEmptyTriggers.root'),
                                SelectEvents = cms.untracked.PSet(
                                       SelectEvents = cms.vstring('mySkimEmtyTriggers'))
                                )
 


process.output = cms.EndPath(process.out1)



# f = file('aNewconfigurationFile.cfg', 'w')
# f.write(process.dumpConfig())
# f.close()



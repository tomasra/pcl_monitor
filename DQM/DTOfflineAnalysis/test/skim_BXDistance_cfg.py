import FWCore.ParameterSet.Config as cms

process = cms.Process("SkimBXDistance")

# the source
process.source = cms.Source("PoolSource",
     fileNames = cms.untracked.vstring(
    '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/00559BCE-DAA4-DD11-A35B-000423D9517C.root'
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

import EventFilter.L1GlobalTriggerRawToDigi.l1GtEvmUnpack_cfi
process.gtEvmDigis = EventFilter.L1GlobalTriggerRawToDigi.l1GtEvmUnpack_cfi.l1GtEvmUnpack.clone()

process.load("DQM.DTOfflineAnalysis.eventListProducer_cfi")
process.load("DQM.DTOfflineAnalysis.l1GmtTriggerSource_cfi")


# message logger
process.MessageLogger = cms.Service("MessageLogger",
                                    destinations = cms.untracked.vstring('cout'),
                                    cout = cms.untracked.PSet(threshold = cms.untracked.string('WARNING'))
                                    )



#process.mySkimBxDistance = cms.Path(process.bxDistanceFilter)

process.mySkimBxDistance = cms.Path(process.gtDigis+ process.eventListProducer + process.l1GmtTriggerSource)


process.out1 = cms.OutputModule("PoolOutputModule",
                                #compressionLevel = cms.untracked.int32(9),
                                fileName = cms.untracked.string('run67818_SkimBxDistance_2.root'),
                                SelectEvents = cms.untracked.PSet(
                                       SelectEvents = cms.vstring('mySkimBxDistance'))
                                )
 


process.output = cms.EndPath(process.out1)




# f = file('aNewconfigurationFile.cfg', 'w')
# f.write(process.dumpConfig())
# f.close()



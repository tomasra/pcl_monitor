import FWCore.ParameterSet.Config as cms

process = cms.Process("SkimBXDistanceStep2")

# the source
process.source = cms.Source("PoolSource",
     fileNames = cms.untracked.vstring(
        'file:/tmp/cerminar/run67818_SkimBxDistance_2.root'
    )
                            )
#process.source.skipEvents = 500000

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )



process.load("DQM.DTOfflineAnalysis.dt_dqm_offlineAnalysis_common_cff")

#process.load("DQM.DTOfflineAnalysis.bxDistanceFilter_cfi")
#process.bxDistanceFilter.debug = True

import EventFilter.L1GlobalTriggerRawToDigi.l1GtUnpack_cfi
process.gtDigis = EventFilter.L1GlobalTriggerRawToDigi.l1GtUnpack_cfi.l1GtUnpack.clone()
process.gtDigis.DaqGtInputTag = 'source'

import EventFilter.L1GlobalTriggerRawToDigi.l1GtEvmUnpack_cfi
process.gtEvmDigis = EventFilter.L1GlobalTriggerRawToDigi.l1GtEvmUnpack_cfi.l1GtEvmUnpack.clone()





# message logger
process.MessageLogger = cms.Service("MessageLogger",
                                    destinations = cms.untracked.vstring('cout'),
                                    cout = cms.untracked.PSet(threshold = cms.untracked.string('WARNING'))
                                    )



process.load("DQM.DTOfflineAnalysis.l1GmtTriggerSource_cfi")
process.load("DQM.DTOfflineAnalysis.bxDistanceFilter_cfi")
process.bxDistanceFilter.listInstance = "All"

process.mySkimBxDistance = cms.Path(process.gtDigis+ process.bxDistanceFilter * process.l1GmtTriggerSource)


process.out1 = cms.OutputModule("PoolOutputModule",
                                #compressionLevel = cms.untracked.int32(9),
                                fileName = cms.untracked.string('/tmp/cerminar/run67818_SkimBxDistance_Step2_Test.root'),
                                SelectEvents = cms.untracked.PSet(
                                       SelectEvents = cms.vstring('mySkimBxDistance')),
                                outputCommands = cms.untracked.vstring('keep *',
                                                                       'drop SimpleEventCollection_event*_*_*')

                                )
 


process.output = cms.EndPath(process.out1)



# f = file('aNewconfigurationFile.cfg', 'w')
# f.write(process.dumpConfig())
# f.close()


process.options = cms.untracked.PSet(
    fileMode = cms.untracked.string('NOMERGE')
    )


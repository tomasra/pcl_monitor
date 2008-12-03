#
# cfg file to run L1GmtTriggerSource
#

import FWCore.ParameterSet.Config as cms

# process
process = cms.Process("TEST")

# number of events to be processed and source file
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(50000)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/002ABA60-CDA4-DD11-9D53-001D09F248FD.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/00559BCE-DAA4-DD11-A35B-000423D9517C.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/00696BD3-74A4-DD11-AB50-001617DBD5B2.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/00D1727B-BCA4-DD11-89C7-001D09F23A07.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/00DFF5CC-E8A4-DD11-93ED-001D09F23E53.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/00ED84F0-D7A4-DD11-912C-001D09F2462D.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/0230E879-BAA4-DD11-AD5E-000423D98634.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/023638D9-DCA4-DD11-8AE3-001D09F24FE7.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/025B07B0-85A4-DD11-9828-000423D98634.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/02FE6C69-C8A4-DD11-AB1E-001617C3B69C.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/0401FDAC-86A4-DD11-9145-0019DB29C5FC.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/049A3FFE-90A4-DD11-AA53-001617C3B76E.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/04CC5535-D0A4-DD11-B7FB-000423D99BF2.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/04F122C1-C0A4-DD11-BFE8-000423D6B5C4.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/04F1258B-B7A4-DD11-91D9-0019B9F72BAA.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/0656E92A-B6A4-DD11-84F4-001D09F24664.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/068A1D69-E7A4-DD11-A7D3-001D09F253FC.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/06E085C6-80A4-DD11-8A85-000423D6B5C4.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/08956446-DEA4-DD11-9894-000423D99F3E.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/08AC780E-B4A4-DD11-9DBE-001D09F254CE.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/0A267B7F-88A4-DD11-8322-000423D996B4.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/0A527211-79A4-DD11-828C-000423D9517C.root',
        '/store/data/Commissioning08/Cosmics/RAW/v1/000/067/818/0AEE483E-DEA4-DD11-9044-001D09F28C1E.root'
                                      )
)
import EventFilter.L1GlobalTriggerRawToDigi.l1GtUnpack_cfi
process.gtDigis = EventFilter.L1GlobalTriggerRawToDigi.l1GtUnpack_cfi.l1GtUnpack.clone()
process.gtDigis.DaqGtInputTag = 'source'

import EventFilter.L1GlobalTriggerRawToDigi.l1GtEvmUnpack_cfi
process.gtEvmDigis = EventFilter.L1GlobalTriggerRawToDigi.l1GtEvmUnpack_cfi.l1GtEvmUnpack.clone()

process.l1GmtTriggerSource = cms.EDAnalyzer("L1GmtTriggerSource",
                                            inputLabel = cms.InputTag("source"),             
                                            GMTInputTag = cms.InputTag("gtDigis")
)

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "CRAFT_V2P::All"

# message logger
process.MessageLogger = cms.Service("MessageLogger",
                                    debugModules = cms.untracked.vstring('*'),
                                    destinations = cms.untracked.vstring('cout'),
                                    categories = cms.untracked.vstring('DTNoiseAnalysisTest'), 
                                    cout = cms.untracked.PSet(threshold = cms.untracked.string('DEBUG'),
                                                              noLineBreaks = cms.untracked.bool(False),
                                                              DEBUG = cms.untracked.PSet(
                                                                      limit = cms.untracked.int32(0)),
                                                              INFO = cms.untracked.PSet(
                                                                      limit = cms.untracked.int32(0)),
                                                              DTNoiseAnalysisTest = cms.untracked.PSet(
                                                                                 limit = cms.untracked.int32(100000000))
                                                              )
                                    )




# path to be run
process.p = cms.Path(process.gtDigis+ process.l1GmtTriggerSource)



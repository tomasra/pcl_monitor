import FWCore.ParameterSet.Config as cms

process = cms.Process("DTFEDAnal")

# the source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
 '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/FC08ADEA-EF83-DE11-8F24-000423D998BA.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/EE944D03-F583-DE11-914A-001D09F24691.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/D604AFAC-0084-DE11-AF62-0019B9F72BAA.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/B8B9A2EC-0384-DE11-8E1C-001D09F2305C.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/B2F37E1E-FE83-DE11-BE40-000423D985B0.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/B255FF1E-FD83-DE11-9D08-000423D98A44.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/B22FC6E6-0784-DE11-85B9-001D09F248F8.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/A65C7829-FC83-DE11-ABEC-000423D944FC.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/A634DC08-FF83-DE11-9563-000423D60FF6.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/A0248F57-FA83-DE11-8F00-000423D986A8.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/8C320D96-F883-DE11-BC12-0019B9F730D2.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/5830A9C2-F283-DE11-9067-000423D98BE8.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/4028D2AC-0484-DE11-A06E-001D09F241D2.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/381BCA2A-EF83-DE11-A214-000423D98868.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/208C6664-ED83-DE11-A2E5-001D09F2523A.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/146EEBE2-F083-DE11-9E76-001D09F2441B.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/10E146C7-F183-DE11-B130-001D09F295FB.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/08F41A6D-0384-DE11-A813-000423D99A8E.root',
        '/store/data/CRAFT09/Cosmics/RAW/v1/000/110/323/001B74E6-0784-DE11-AD12-0019B9F6C674.root'
      ))


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
    )


process.load("DQM.DTOfflineAnalysis.fedSizeAnalyzer_cfi")


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
                                                                                 limit = cms.untracked.int32(-1))
                                                              )
                                    )


process.jobPath = cms.Path(process.fedSizeAnalyzer)
#process.jobPath = cms.Path(process.dtLocalRecoAnal)


#f = file('aNewconfigurationFile.cfg', 'w')
#f.write(process.dumpConfig())
#f.close()


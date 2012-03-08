import FWCore.ParameterSet.Config as cms

genLevelTriggerEff = cms.EDAnalyzer("GenLevelTriggerEff",
                                    genParticles = cms.untracked.InputTag("genParticles"),
                                    triggerResults = cms.untracked.InputTag("TriggerResults"),
                                    triggerName1 = cms.untracked.string("HLT_Tau2Mu_RegPixTrack_v1"),
                                    triggerName2 = cms.untracked.string("HLT_Tau2Mu_RegPixTrack_Tight_v1"),
                                    triggerName3 = cms.untracked.string("HLT_Tau2Mu_ItTrack_v1")
                                    )

import FWCore.ParameterSet.Config as cms

source = cms.Source("EmptySource")


generator = cms.EDFilter("Pythia6GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(7000.0),
    crossSection = cms.untracked.double(71260000000.0),
    maxEventsToPrint = cms.untracked.int32(0),
   
    PythiaParameters = cms.PSet(
        pythiaUESettings = cms.vstring('MSTU(21)=1     ! Check on possible errors during program execution', 
            'MSTJ(22)=2     ! Decay those unstable particles', 
            'PARJ(71)=10 .  ! for which ctau  10 mm', 
            'MSTP(33)=0     ! no K factors in hard cross sections', 
            'MSTP(2)=1      ! which order running alphaS', 
            'MSTP(51)=10042 ! structure function chosen (external PDF CTEQ6L1)', 
            'MSTP(52)=2     ! work with LHAPDF', 
            'PARP(82)=1.832 ! pt cutoff for multiparton interactions', 
            'PARP(89)=1800. ! sqrts for which PARP82 is set', 
            'PARP(90)=0.275 ! Multiple interactions: rescaling power', 
            'MSTP(95)=6     ! CR (color reconnection parameters)', 
            'PARP(77)=1.016 ! CR', 
            'PARP(78)=0.538 ! CR', 
            'PARP(80)=0.1   ! Prob. colored parton from BBR', 
            'PARP(83)=0.356 ! Multiple interactions: matter distribution parameter', 
            'PARP(84)=0.651 ! Multiple interactions: matter distribution parameter', 
            'PARP(62)=1.025 ! ISR cutoff', 
            'MSTP(91)=1     ! Gaussian primordial kT', 
            'PARP(93)=10.0  ! primordial kT-max', 
            'MSTP(81)=21    ! multiple parton interactions 1 is Pythia default', 
            'MSTP(82)=4     ! Defines the multi-parton model'),
        processParameters = cms.vstring('MSEL=1         ! User defined processes', # or put 0 and use next lines for indiv processes 
         #   'MSUB(11)=1     ! Min bias process', 
         #   'MSUB(12)=1     ! Min bias process', 
         #   'MSUB(13)=1     ! Min bias process', 
         #   'MSUB(28)=1     ! Min bias process', 
         #   'MSUB(53)=1     ! Min bias process', 
         #   'MSUB(68)=1     ! Min bias process', 
         #   'MSUB(92)=1     ! Min bias process, single diffractive', 
         #   'MSUB(93)=1     ! Min bias process, single diffractive', 
         #   'MSUB(94)=1     ! Min bias process, double diffractive', 
         #   'MSUB(95)=1     ! Min bias process'
	 #,# D_s decays
       'MDME(818,1)=1    ! D_s+ -> tau nutau',
       'MDME(819,1)=0    ! ',
       'MDME(820,1)=0    ! ',
       'MDME(821,1)=0    ! D_s+ -> phi e nu',
       'MDME(822,1)=0    ! ',
       'MDME(823,1)=0    ! ',
       'MDME(824,1)=0    ! ',
       'MDME(825,1)=0    ! ',
       'MDME(826,1)=0    ! D_s+ -> phi mu nu',
       'MDME(827,1)=0    ! ',
       'MDME(828,1)=0    ! ',
       'MDME(829,1)=0    ! ',
       'MDME(830,1)=0    ! ',
       'MDME(831,1)=0    ! D_s+ -> phi pi',
       'MDME(832,1)=0    ! ',
       'MDME(833,1)=0    ! ',
       'MDME(834,1)=0    ! D_s+ -> phi ro',
       'MDME(835,1)=0    ! ',
       'MDME(836,1)=0    ! ',
       'MDME(837,1)=0    ! ',
       'MDME(838,1)=0    ! ',
       'MDME(839,1)=0    ! ',
       'MDME(840,1)=0    ! ',
       'MDME(841,1)=0    ! ',
       'MDME(842,1)=0    ! ',
       'MDME(843,1)=0    ! ',
       'MDME(844,1)=0    ! ',
       'MDME(845,1)=0    ! ',
       'MDME(846,1)=0    ! ',
       'MDME(847,1)=0    ! D_s+ ->phi K',
       'MDME(848,1)=0    ! ',
       'MDME(849,1)=0    ! ',
       'MDME(850,1)=0    ! '
					),
        parameterSets = cms.vstring('pythiaUESettings', 
            'processParameters')
    ),
				 
				     ExternalDecays = cms.PSet(
	EvtGen = cms.untracked.PSet(
	  operates_on_particles = cms.vint32(431,15), # 15=only tau
	  use_default_decay = cms.untracked.bool(False),
	  decay_table = cms.FileInPath('GeneratorInterface/ExternalDecays/data/DECAY_NOLONGLIFE.DEC'),
	  particle_property_file = cms.FileInPath('GeneratorInterface/ExternalDecays/data/evt.pdl'),
	  # user_decay_file = cms.FileInPath('GeneratorInterface/ExternalDecays/data/Ds_tau_mumumu.dec'),
	  user_decay_file = cms.FileInPath('MyAnalysis/Tau3Mu/data/Ds_tau_mumumu.dec'),
	  list_forced_decays = cms.vstring('Mytau+','Mytau-','MyD_s+','MyD_s-')
	  ),
	parameterSets = cms.vstring('EvtGen')
	),

)

# filter to select events with a Ds
DsFilter = cms.EDFilter("PythiaFilter",
       Status = cms.untracked.int32(2),
       MaxEta = cms.untracked.double(3),
       MinEta = cms.untracked.double(-3),
       MinPt = cms.untracked.double(5),
       ParticleID = cms.untracked.int32(431)  #D_s 
   )

# ask 3 muons in the acceptance
muonParticlesInAcc = cms.EDFilter("GenParticleSelector",
				  filter = cms.bool(False),
				  src = cms.InputTag("genParticles"),
				  cut = cms.string('pt > 1. && abs(pdgId) == 13 && abs(eta) < 2.4'),
				  stableOnly = cms.bool(True)
				  )


threeMuonFilter = cms.EDFilter("CandViewCountFilter",
			       src = cms.InputTag("muonParticlesInAcc"),
			       minNumber = cms.uint32(3))


ProductionFilterSequence = cms.Sequence(process.generator * process.DsFilter * (muonParticlesInAcc + threeMuonFilter))

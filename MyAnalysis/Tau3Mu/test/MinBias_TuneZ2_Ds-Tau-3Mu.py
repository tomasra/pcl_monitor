# Auto generated configuration file
# using: 
# Revision: 1.303.2.7 
# Source: /cvs_server/repositories/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: MinBias_TuneZ2_7TeV_pythia6_cff.py -s GEN --geometry DB --datatier GEN-SIM-RAW --conditions MC_42_V15B --eventcontent RAWSIM --no_exec
import FWCore.ParameterSet.Config as cms

process = cms.Process('GEN')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic7TeV2011Collision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10000)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.3 $'),
    annotation = cms.untracked.string('MinBias_TuneZ2_7TeV_pythia6_cff.py nevts:1'),
    name = cms.untracked.string('PyReleaseValidation')
)

# Output definition

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    fileName = cms.untracked.string('MinBias_TuneZ2_Ds-Tau-3Mu.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-RAW')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

# Other statements
process.GlobalTag.globaltag = 'START42_V15B::All'

#customized generator settings:
# - load custom decay for tau to 3mu (phase space) and force to this decay
# - modify pythia cards for Ds decay to force Ds->Tau

process.generator = cms.EDFilter("Pythia6GeneratorFilter",
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
      				),
        parameterSets = cms.vstring('pythiaUESettings', 
            'processParameters')
    ),
				 
				     ExternalDecays = cms.PSet(
	EvtGen = cms.untracked.PSet(
	  operates_on_particles = cms.vint32(0), # 0=all
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
process.Dfilter = cms.EDFilter("PythiaFilter",
       Status = cms.untracked.int32(2),
       MaxEta = cms.untracked.double(3),
       MinEta = cms.untracked.double(-3),
       MinPt = cms.untracked.double(5),
       ParticleID = cms.untracked.int32(431)  #D_s 
   )

# ask 3 muons in the acceptance: filter needed!!!!!!!!!!!!

# ask 3 muons in the acceptance
process.muonParticlesInAcc = cms.EDFilter("GenParticleSelector",
				  filter = cms.bool(False),
				  src = cms.InputTag("genParticles"),
				  cut = cms.string('pt > 1. && abs(pdgId) == 13 && abs(eta) < 2.4'),
				  stableOnly = cms.bool(True)
				  )


process.threeMuonFilter = cms.EDFilter("CandViewCountFilter",
			       src = cms.InputTag("muonParticlesInAcc"),
			       minNumber = cms.uint32(3))

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
    )


process.ProductionFilterSequence = cms.Sequence(process.generator)

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen*process.Dfilter*process.muonParticlesInAcc*process.threeMuonFilter)  # put filter for muon acceptance here!
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step,process.RAWSIMoutput_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq 

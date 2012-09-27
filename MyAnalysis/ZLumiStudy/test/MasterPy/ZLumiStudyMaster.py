import FWCore.ParameterSet.Config as cms
process = cms.Process("TEST")

### ----------------------------------------------------------------------
### Flags that need to be setted
### ----------------------------------------------------------------------

try:
    IsMC
except NameError:
    IsMC = True


try:
    LEPTON_SETUP
except NameError:
    LEPTON_SETUP = 2012 # define the set of effective areas, rho corrections, etc.


try:
    SAMPLE_TYPE
except NameError:
    SAMPLE_TYPE = LEPTON_SETUP


#use "Prompt2012", "Summer12" for 2012 data
try:
    ELECORRTYPE
except NameError:
    ELECORRTYPE = "None"
    

# Setup for V4 PAT on 44X samples:
# patElectrons: selectedPatElectrons 
# patMuons: selectedPatMuons, requires module PATPFMuonEmbedder to attach userFloat('isPFMuon')
#           (the collection selectedPatMuonsAK5 also exists; it contains only muons which are isPFMuon())

# For V5 PAT on 42X samples:
# patElectrons: patElectronsWithTrigger  
# patMuons: patMuonsWithTrigger (built from recoMuons; userFloat('isPFMuon') is already attached)

# For V5 PAT on 52X samples:
# Same collection names. In 52X, patMuons have the method isPFMuon().

try:
  PATVERSION
except NameError:
  PATVERSION = "V5"


### ----------------------------------------------------------------------
### Set the GT
### ----------------------------------------------------------------------
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
if IsMC: 
  #process.GlobalTag.globaltag = 'GR_P_V14::All'
  #process.GlobalTag.globaltag = 'GR_R_39X_V5::All'
  #process.GlobalTag.globaltag = 'START311_V2::All'
  #process.GlobalTag.globaltag = 'START42_V12::All'
  #process.GlobalTag.globaltag = 'START42_V12::All'
  #2012 Analysis: First Step Fall11 42X MC 
  process.GlobalTag.globaltag = 'START44_V12::All'
else: 
  process.GlobalTag.globaltag = 'GR_P_V41_AN2::All' # For Jan16rereco, 42X 


### ----------------------------------------------------------------------
### Standard stuff
### ----------------------------------------------------------------------
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


### ----------------------------------------------------------------------
### Source
### ----------------------------------------------------------------------
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      '/store/cmst3/user/cmgtools/CMG/GluGluToHToZZTo4L_M-130_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM/V5/PAT_CMG_V5_2_0/patTuple_1.root'
    )
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)


### ----------------------------------------------------------------------
### Trigger bit Requests 
### ----------------------------------------------------------------------
import HLTrigger.HLTfilters.hltHighLevel_cfi 

process.hltFilterDiMu  = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltFilterDiMu.TriggerResultsTag  = cms.InputTag("TriggerResults","","HLT")
process.hltFilterDiMu.throw  = cms.bool(False) #FIXME: beware of this!

if (LEPTON_SETUP == 2011):
   if (IsMC):
       process.hltFilterDiMu.HLTPaths = ["HLT_Mu17_Mu8_v*"] # to run on MC 2011    
   else :
       process.hltFilterDiMu.HLTPaths = ["HLT_DoubleMu7_v*", "HLT_Mu13_Mu8_v*", "HLT_Mu17_Mu8_v*"] # to run on data 2011 NB: Emulation is needed

elif (LEPTON_SETUP == 2012):
  #process.hltFilterDiMu.HLTPaths = ["HLT_Mu17_Mu8_v*", "HLT_Mu17_TkMu8_v*"] # to run on data 2012 Data/MC No Emulation needed
  process.hltFilterDiMu.HLTPaths = ["HLT_Mu17_Mu8_v*"] # to run on data 2012 Data/MC No Emulation needed

process.triggerDiMu   = cms.Path(process.hltFilterDiMu)


### ----------------------------------------------------------------------
### MC Filters and tools
### ----------------------------------------------------------------------

process.heavyflavorfilter = cms.EDFilter('HeavyFlavorFilter2',
#                                 src= cms.InputTag("genParticles"), # genParticles available only in PAT
                                 src= cms.InputTag("genParticlesPruned"),
                                 status2 = cms.bool(True),
                                 status3 = cms.bool(True),
                                 hDaughterVeto = cms.bool(True),
                                 zDaughterVeto = cms.bool(False),
                                 ptcut=cms.double(0)
                                 )


process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   src = cms.InputTag("genParticlesPruned"),
                                   printP4 = cms.untracked.bool(False),
                                   printPtEtaPhi = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(False),
                                   printStatus = cms.untracked.bool(True),
                                   printIndex = cms.untracked.bool(False) )


process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
                                                   patElectronsWithTrigger = cms.PSet(
                                                       initialSeed = cms.untracked.uint32(1),
                                                       engineName = cms.untracked.string('TRandom3')
                                                       ),
                                                   )



### ----------------------------------------------------------------------
### ----------------------------------------------------------------------
### Loose lepton selection + cleaning + embeddding of user data
### ----------------------------------------------------------------------
### ----------------------------------------------------------------------

#GOODLEPTON = "userFloat('ID') && userFloat('SIP')<4 && userFloat('combRelIsoPF')<0.4" # Lepton passing ID, SIP, ISO
GOODLEPTON = "userFloat('ID') && userFloat('SIP')<4" # Lepton passing ID, SIP [ISO is asked AFTER FSR!!!]

#&& userFloat('combRelIsoPF')<0.4


process.bareSoftMuons = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("(isGlobalMuon || (isTrackerMuon && numberOfMatches>0)) &&" +
                     "pt>5 && abs(eta)<2.4")
)



# MC matching. As the genParticles are no more available in cmg, we re-match with genParticlesPruned.
process.muonMatch = cms.EDProducer("MCMatcher", # cut on deltaR, deltaPt/Pt; pick best by deltaR
                                   src     = cms.InputTag("softMuons"), # RECO objects to match  
                                   matched = cms.InputTag("genParticlesPruned"),   # mc-truth particle collection
                                   mcPdgId     = cms.vint32(13), # one or more PDG ID (13 = muon); absolute values (see below)
                                   checkCharge = cms.bool(True), # True = require RECO and MC objects to have the same charge
                                   mcStatus = cms.vint32(1),     # PYTHIA status code (1 = stable, 2 = shower, 3 = hard scattering)
                                   maxDeltaR = cms.double(0.5),  # Minimum deltaR for the match
                                   maxDPtRel = cms.double(0.5),  # Minimum deltaPt/Pt for the match
                                   resolveAmbiguities = cms.bool(True),     # Forbid two RECO objects to match to the same GEN object
                                   resolveByMatchQuality = cms.bool(False), # False = just match input in order; True = pick lowest deltaR pair first
                                   )

process.softMuons = cms.EDProducer("MuProperties",
    src = cms.InputTag("bareSoftMuons"),
    sampleType = cms.int32(SAMPLE_TYPE),                     
    setup = cms.int32(LEPTON_SETUP), # define the set of effective areas, rho corrections, etc.
#    cut = cms.string("userFloat('SIP')<100"),
    cut = cms.string("userFloat('dxy')<0.5 && userFloat('dz')<1."),
    flags = cms.PSet(
        ID = cms.string("userFloat('isPFMuon')" ), # PF ID
        isGood = cms.string(GOODLEPTON),
        isPFISO = cms.string("userFloat('combRelIsoPF')<0.4")
    )
)



### ----------------------------------------------------------------------
### ----------------------------------------------------------------------
### BUILD CANDIDATES 
### ----------------------------------------------------------------------
### ----------------------------------------------------------------------



### ----------------------------------------------------------------------
### Dileptons: combine/merge leptons into intermediate (bare) collections;
###            Embed additional user variables into final collections
### ----------------------------------------------------------------------

TWOGOODLEPTONS = ("userFloat('d0.isGood') && userFloat('d1.isGood')") # Z made of 2 isGood leptons
#ZISO           = ("userFloat('d0.combRelIsoPFFSRCorr')<0.4 && userFloat('d1.combRelIsoPFFSRCorr')<0.4") #ISO after FSR
ZISO           = ("userFloat('d0.isPFISO') && userFloat('d1.isPFISO')") #ISO after FSR

ZLEPTONSEL     = TWOGOODLEPTONS + "&&" + ZISO


BESTZ_AMONG = ( ZLEPTONSEL ) # "Best Z" chosen among those with 2 leptons with ID, SIP, ISO

Z1PRESEL    = (ZLEPTONSEL + " && mass > 40 && mass < 120") # FIXME



# mu+mu-
process.bareMMCand = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string('softMuons@+ softMuons@-'),
#    decay = cms.string('appendPhotons:muons@+ appendPhotons:muons@-'),
    cut = cms.string('mass > 0'), # protect against ghosts
    checkCharge = cms.bool(True)
)
process.MMCand = cms.EDProducer("ZCandidateProperties",
    src = cms.InputTag("bareMMCand"),
    sampleType = cms.int32(SAMPLE_TYPE),                     
    setup = cms.int32(LEPTON_SETUP), # define the set of effective areas, rho corrections, etc.
    bestZAmong = cms.string(BESTZ_AMONG),
    flags = cms.PSet(
        GoodLeptons = cms.string(ZLEPTONSEL),
        ZPresel = cms.string(Z1PRESEL),
                                    )
    )

 

### ----------------------------------------------------------------------
### Paths
### ----------------------------------------------------------------------

# Prepare lepton collections
process.Leptons = cms.Path(
       process.bareSoftMuons     + process.softMuons  
  )

# if ELECORRTYPE != "None" :
#     process.Leptons.insert( 0, process.patElectronsWithTrigger )


# Build 4-lepton candidates
process.Candidates = cms.Path(
       process.bareMMCand         + process.MMCand  
  )


### Skim, triggers and MC filters (Only store filter result, no filter is applied)

### 2011 HZZ Skim
#process.afterSkimCounter = cms.EDProducer("EventCountProducer")
#process.load("ZZAnalysis.AnalysisStep.HZZSkim_cfg")
#process.skim = cms.Path(process.skim2011 + process.afterSkimCounter) # the 2011 skim

### 2012 skim.
#FIXME this is the version from /afs/cern.ch/user/p/psilva/public/HZZSkim/PDWG_HZZSkim_cff.py
#      which is buggy!!
#process.load("ZZAnalysis.AnalysisStep.PDWG_HZZSkim_cff") 
#SkimPaths = cms.vstring('HZZ4ePath', 'HZZ2e2mPath', 'HZZ2m2ePath', 'HZZ4mPath', 'HZZem2ePath', 'HZZem2mPath')

# Reimplementation by Giovanni
#process.load("ZZAnalysis.AnalysisStep.Skim2012_cfg")
#process.SkimSequence = cms.Sequence(process.HZZSkim2012)
#process.Skim = cms.Path(process.SkimSequence)
#SkimPaths = cms.vstring('Skim')

SkimPaths = cms.vstring()

# process.HF = cms.Path(process.heavyflavorfilter)

# FIXME total kin filter?




import FWCore.ParameterSet.Config as cms

### USAGE:
###    cmsRun fitTrigger_Z.py <scenario>
### scenarios:
###   - data_all:    will fit tnpJPsi_Data.root with bins suitable for the current data
###   - datalike_mc: will fit tnpJPsi_{JPsiMuMu,ppMuX}_Spring10_0.117pb.root MC but
###                  with same config as data

import sys
args = sys.argv[1:]
if (sys.argv[0] == "cmsRun"): args =sys.argv[2:]
scenario = "data_all"
if len(args) > 0: scenario = args[0]
print "Will run scenario ", scenario 

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.TnP_Trigger = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    NumCPU = cms.uint32(1),
    SaveWorkspace = cms.bool(False),

    InputFileNames = cms.vstring('/data1/ZLumiStudy/TagAndProbe/TPV0/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_9_1_1Iu_sorted_lumi.root',
'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_82_2_eSg_sorted_lumi.root',
'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_84_2_jrg_sorted_lumi.root',
'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_85_2_Yoi_sorted_lumi.root',
'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_86_2_spN_sorted_lumi.root',
'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_87_1_7Nl_sorted_lumi.root',
'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_88_1_ll4_sorted_lumi.root',
'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_89_1_RMZ_sorted_lumi.root',
'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_8_1_NYr_sorted_lumi.root',
'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_90_1_Wym_sorted_lumi.root',
'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_91_1_ZsV_sorted_lumi.root',
'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_92_1_F88_sorted_lumi.root',
'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_93_1_oox_sorted_lumi.root',
'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_94_1_pKE_sorted_lumi.root',
                                 ),
    InputTreeName = cms.string("fitter_tree"),
    InputDirectoryName = cms.string("tpTree"),
    OutputFileName = cms.string("TnP_Z_Trigger_%s.root" % scenario),

    Variables = cms.PSet(
        mass = cms.vstring("Tag-Probe Mass", "70", "110", "GeV/c^{2}"),
        pt     = cms.vstring("Probe p_{T}", "0", "1000", "GeV/c"),
        eta    = cms.vstring("Probe |#eta|", "-2.5", "2.5", ""),
        abseta = cms.vstring("Probe |#eta|", "0", "2.5", ""),
        SIP = cms.vstring("Probe SIP", "0", "1000", ""),
        bxInstLumi = cms.vstring("Inst. Lumi. by BX","0","7", "1/ub"),
        tag_pt = cms.vstring("Tag p_{T}", "2.6", "1000", "GeV/c"),
        combRelIso = cms.vstring("Iso", "0", "6", ""),
    ),

    Categories = cms.PSet(
        Calo = cms.vstring("POG_Glb",  "dummy[pass=1,fail=0]"),
        Glb  = cms.vstring("POG_Glb",  "dummy[pass=1,fail=0]"),
        VBTF = cms.vstring("VBTFLike", "dummy[pass=1,fail=0]"),
        Isol = cms.vstring("MC true",  "dummy[pass=1,fail=0]"),
        DoubleMu17Mu8_Mu17  = cms.vstring("DoubleMu17Mu8_Mu17",  "dummy[pass=1,fail=0]"),
    ),

    PDFs = cms.PSet(
        gaussPlusExpo = cms.vstring(
            "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])",
            "Exponential::backgroundPass(mass, lp[0,-5,5])",
            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        voigtPlusExpo = cms.vstring(
            "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])",
            "Exponential::backgroundPass(mass, lp[0,-5,5])",
            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusExpo = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,2,10])",
            "SUM::signal(vFrac[0.8,0,1]*signal1, signal2)",
            "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])",
            "Exponential::backgroundFail(mass, lf[-0.9,-1,0.1])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
    ),
    #Cuts = cms.PSet(),
    Efficiencies = cms.PSet(), # will be filled later
)


# === SETTINGS
# ==================================================================================================
# Here I define the different categories (or BINS) for wich I want to compute the efficiency
triggerName = "DoubleMu17Mu8_Mu17"
minPtCut = 20.
instLumiBins = cms.vdouble()


BARREL = cms.PSet(
    pt = cms.vdouble(minPtCut, 100),
    abseta = cms.vdouble( 0, 1.2)
    )

ALL2P1 = cms.PSet(
    pt = cms.vdouble(minPtCut, 100),
    abseta = cms.vdouble( 0, 2.1)
    )

ALL2P4 = cms.PSet(
    pt = cms.vdouble(minPtCut, 100),
    abseta = cms.vdouble( 0, 2.4)
    )

# cuts used in ZlumiTreeReader
SURVIVE_WITHOUT_ISO = cms.PSet(
    pt = cms.vdouble(minPtCut, 100),
    SIP = cms.vdouble(0, 0.4),
    )
SURVIVE_WITH_ISO = cms.PSet(
    pt = cms.vdouble(minPtCut, 100),
    SIP = cms.vdouble(0, 0.4),
    combRelIso = cms.vdouble(0, 0.4),
    )
SURVIVE_ETA_WITHOUT_ISO = cms.PSet(
    pt = cms.vdouble(minPtCut, 100),
    SIP = cms.vdouble(0, 0.4),
    abseta = cms.vdouble(0, 1.2),
    )
SURVIVE_ETA_WITH_ISO = cms.PSet(
    pt = cms.vdouble(minPtCut, 100),
    SIP = cms.vdouble(0, 0.4),
    abseta = cms.vdouble(0, 1.2),
    combRelIso = cms.vdouble(0, 0.4),
    )


PT_BINS_ALL2P1 = ALL2P1.clone(pt = cms.vdouble(15, 25, 35, 100))
ETA_BINS_ALL2P1 = ALL2P1.clone(abseta = cms.vdouble(0, 1.2, 2.1))
# lumi bins between 1 and 5 (16 bins)
LUMI_BINS_BARREL = BARREL.clone(bxInstLumi = cms.vdouble(1.0, 1.25, 1.5, 1.75, 2., 2.25, 2.5, 2.75, 3., 3.25, 3.5, 3.75, 4., 4.25, 4.5, 4.75, 5))
RUNS = "run == 194315"
#process.TnP_Trigger.Cuts = cms.PSet(
#    run194315 = cms.vstring("runSel", "run", "194315")
#    )
# FIXME: add the run selections to match what is used in the analysis
# FIXME: get the complete list of InputFileNames directly out of the directory
#==== END SETTINGS

if scenario == "data_all":
    process.TnP_Trigger.binsForMassPlots = cms.uint32(20)

if scenario == "datalike_mc":
    process.TnP_Trigger.InputFileNames = [ "tnpZ_MC.root", ]


ALLBINS = [
#    ("all2p1", ALL2P1),
    ("barr_lumi", LUMI_BINS_BARREL),
]



for (T,M) in [ ("DoubleMu17Mu8_Mu17","Track"),("DoubleMu17Mu8_Mu17","OurMuonID")]:
        print "--------------"
        print "Trigger: " + T
        print "From: " + M

        for BN,BV in ALLBINS:
            print "   Bin Name: " + BN
            print "   Bins: " + str(BV)
            BINNEDVARS = BV.clone()
            if M == 'OurMuonID':
                # here we should reimplement exactly our Muon ID
                setattr(BINNEDVARS, "VBTF", cms.vstring("pass"))
            # orig: if M == "VBTF_Isol":
            elif M == "VBTF_Isol":
                setattr(BINNEDVARS, "VBTF", cms.vstring("pass"))
                setattr(BINNEDVARS, "Isol", cms.vstring("pass"))
            elif M != "Track": 
                setattr(BINNEDVARS, M, cms.vstring("pass"))
            setattr(process.TnP_Trigger.Efficiencies, M+"_To_"+T+"_"+BN, cms.PSet(
                    EfficiencyCategoryAndState = cms.vstring(T,"pass"),
                    UnbinnedVariables = cms.vstring("mass"),
                    BinnedVariables = BINNEDVARS,
                    BinToPDFmap = cms.vstring("vpvPlusExpo")
                ))
# for  X,B in ALLBINS:
#     setattr(process.TnP_Trigger.Efficiencies, "Track_To_VBTF_Mu9_"+X, cms.PSet(
#         EfficiencyCategoryAndState = cms.vstring("VBTF","pass","Mu9","pass"),
#         UnbinnedVariables = cms.vstring("mass"),
#         BinnedVariables = B,
#         BinToPDFmap = cms.vstring("gaussPlusExpo")
#     ))
#     setattr(process.TnP_Trigger.Efficiencies, "Track_To_VBTF_Isol_Mu9_"+X, cms.PSet(
#         EfficiencyCategoryAndState = cms.vstring("VBTF","pass","Isol","pass","Mu9","pass"),
#         UnbinnedVariables = cms.vstring("mass"),
#         BinnedVariables = B,
#         BinToPDFmap = cms.vstring("gaussPlusExpo")
#     ))


process.p = cms.Path(
    process.TnP_Trigger
)

f = file('fitTrigger_byLumi_dump.py', 'w')
f.write(process.dumpPython())
f.close()


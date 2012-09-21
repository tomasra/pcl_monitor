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

run_files = "Run2012B"
print "Will use files for ", run_files

outputName = run_files + "_TnP_Z_Trigger" + scenario + ".root"


process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.TnP_Trigger = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    NumCPU = cms.uint32(1),
    SaveWorkspace = cms.bool(False),

    InputFileNames = cms.vstring(),

#    InputFileNames = cms.vstring('/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_9_1_1Iu_sorted_lumi.root',
#'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_82_2_eSg_sorted_lumi.root',
#'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_84_2_jrg_sorted_lumi.root',
#'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_85_2_Yoi_sorted_lumi.root',
#'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_86_2_spN_sorted_lumi.root',
#'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_87_1_7Nl_sorted_lumi.root',
#'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_88_1_ll4_sorted_lumi.root',
#'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_89_1_RMZ_sorted_lumi.root',
#'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_8_1_NYr_sorted_lumi.root',
#'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_90_1_Wym_sorted_lumi.root',
#'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_91_1_ZsV_sorted_lumi.root',
#'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_92_1_F88_sorted_lumi.root',
#'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_93_1_oox_sorted_lumi.root',
#'/data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1_lumi/tnpZ_Data_94_1_pKE_sorted_lumi.root',
#                                 ),
    InputTreeName = cms.string("fitter_tree"),
    InputDirectoryName = cms.string("tpTree"),
    OutputFileName = cms.string(outputName),

    Variables = cms.PSet(
        mass = cms.vstring("Tag-Probe Mass", "70", "110", "GeV/c^{2}"),
        pt     = cms.vstring("Probe p_{T}", "0", "1000", "GeV/c"),
        eta    = cms.vstring("Probe |#eta|", "-2.5", "2.5", ""),
        abseta = cms.vstring("Probe |#eta|", "0", "2.5", ""),
        SIP = cms.vstring("Probe SIP", "0", "1000", ""),
        bxInstLumi = cms.vstring("Inst. Lumi. by BX","0","7", "1/ub"),
        tag_pt = cms.vstring("Tag p_{T}", "2.6", "1000", "GeV/c"),
        combRelIso = cms.vstring("Iso", "0", "6", ""),
        dxyPVdzmin = cms.vstring("dxyPVdzmin", "0", "10","cm"),
        dzPV = cms.vstring("dzPV", "0", "10", "cm"),
    ),

    Categories = cms.PSet(
        Calo = cms.vstring("POG_Glb",  "dummy[pass=1,fail=0]"),
        Glb  = cms.vstring("POG_Glb",  "dummy[pass=1,fail=0]"),
        VBTF = cms.vstring("VBTFLike", "dummy[pass=1,fail=0]"),
        Isol = cms.vstring("MC true",  "dummy[pass=1,fail=0]"),
        DoubleMu17Mu8_Mu17  = cms.vstring("DoubleMu17Mu8_Mu17",  "dummy[pass=1,fail=0]"),
        DoubleMu17Mu8_Mu8  = cms.vstring("DoubleMu17Mu8_Mu8",  "dummy[pass=1,fail=0]"),
        GlbOrTMwMatch = cms.vstring("GlbOrTMwMatch", "dummy[pass=1,fail=0]"),
        PF = cms.vstring("PF", "dummy[pass=1,fail=0]"),
    ),

    Cuts = cms.PSet(
        eta0P8 = cms.vstring("abseta < 0.8", "abseta", "0.8"),
        eta1P2 = cms.vstring("abseta < 1.2", "abseta", "1.2"),
        eta2P4 = cms.vstring("abseta < 2.4", "abseta", "2.4"),
        pt20 = cms.vstring("pt > 20", "pt", "20"),
        dxyPV0P5 = cms.vstring("dxy (from PV) < 0.5", "dxyPVdzmin", "0.5"),
        dz1 = cms.vstring("dz < 1", "dzPV", "1"),
        SIP3 = cms.vstring("SIP < 3", "SIP", "3"),
        combRelIso0P4 = cms.vstring("Isolation < 0.4", "combRelIso", "0.4",)
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


# load file for root-files
files = []
read_file = open(run_files + ".txt", "r")

# change nth_lines or lines_to_use
lines_to_use = 1
nth_line = 3

for ln, line in enumerate(read_file):
    if ln%nth_line == lines_to_use:
        lineparts = line.split('\n')
        if lineparts[0] != "":
            files.append(lineparts[0])
read_file.close()

for i in range(len(files)):
    print files[i]

process.TnP_Trigger.InputFileNames += files

# === SETTINGS
# ==================================================================================================
# Here I define the different categories (or BINS) for wich I want to compute the efficiency
triggerName = "DoubleMu17Mu8_Mu17"
minPtCut = 20.
instLumiBins = cms.vdouble()


BARREL = cms.PSet(
    pt = cms.vdouble(minPtCut, 200),
    abseta = cms.vdouble( 0, 1.2)
    )


ALL0P8 = cms.PSet(
    pt = cms.vdouble(minPtCut, 200),
    abseta = cms.vdouble(0, 0.8)
    )
ALL1P2 = cms.PSet(
    pt = cms.vdouble(minPtCut, 200),
    abseta = cms.vdouble( 0, 1.2)
    )
ALL2P4 = cms.PSet(
    pt = cms.vdouble(minPtCut, 200),
    abseta = cms.vdouble( 0, 2.4)
    )

ALL0P8_ISO = cms.PSet(
    pt = cms.vdouble(minPtCut, 200),
    abseta = cms.vdouble(0, 0.8),
    combRelIso = cms.vdouble(0, 0.4)
    )
ALL1P2_ISO = cms.PSet(
    pt = cms.vdouble(minPtCut, 200),
    abseta = cms.vdouble(0, 1.2),
    combRelIso = cms.vdouble(0, 0.4)
    )
ALL2P4_ISO = cms.PSet(
    pt = cms.vdouble(minPtCut, 200),
    abseta = cms.vdouble(0, 2.4),
    combRelIso = cms.vdouble(0, 0.4)
    )

LUMI_ETA0P8 = ALL0P8.clone(bxInstLumi = cms.vdouble([1+0.25*x for x in range(0,17)]))
LUMI_ETA1P2 = ALL1P2.clone(bxInstLumi = cms.vdouble([1+0.25*x for x in range(0,17)]))
LUMI_ETA2P4 = ALL2P4.clone(bxInstLumi = cms.vdouble([1+0.25*x for x in range(0,17)]))
LUMI_ETA0P8_ISO = ALL0P8_ISO.clone(bxInstLumi = cms.vdouble([1+0.25*x for x in range(0,17)]))
LUMI_ETA1P2_ISO = ALL1P2_ISO.clone(bxInstLumi = cms.vdouble([1+0.25*x for x in range(0,17)]))
LUMI_ETA2P4_ISO = ALL2P4_ISO.clone(bxInstLumi = cms.vdouble([1+0.25*x for x in range(0,17)]))
 


#PT_BINS_ALL2P1 = ALL2P1.clone(pt = cms.vdouble(15, 25, 35, 100))
#ETA_BINS_ALL2P1 = ALL2P1.clone(abseta = cms.vdouble(0, 1.2, 2.1))
# lumi bins between 1 and 5 (16 bins)
LUMI_BINS_BARREL = BARREL.clone(bxInstLumi = cms.vdouble([1+0.25*x for x in range(0,17)]))
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



#for (T,M) in [ ("DoubleMu17Mu8_Mu17","Track"),("DoubleMu17Mu8_Mu17","OurMuonID")]:
#        print "--------------"
#        print "Trigger: " + T
#        print "From: " + M
#
#        for BN,BV in ALLBINS:
#            print "   Bin Name: " + BN
#            print "   Bins: " + str(BV)
#            BINNEDVARS = BV.clone()
#            if M == 'OurMuonID':
#                # here we should reimplement exactly our Muon ID
#                setattr(BINNEDVARS, "VBTF", cms.vstring("pass"))
#            # orig: if M == "VBTF_Isol":
#            elif M == "VBTF_Isol":
#                setattr(BINNEDVARS, "VBTF", cms.vstring("pass"))
#                setattr(BINNEDVARS, "Isol", cms.vstring("pass"))
#            elif M != "Track": 
#                setattr(BINNEDVARS, M, cms.vstring("pass"))
#
#            setattr(process.TnP_Trigger.Efficiencies, M+"_To_"+T+"_"+BN, cms.PSet(
#                    EfficiencyCategoryAndState = cms.vstring(T,"pass"),
#                    UnbinnedVariables = cms.vstring("mass"),
#                    BinnedVariables = BINNEDVARS,
#                    BinToPDFmap = cms.vstring("vpvPlusExpo")
#                ))

def GetOurMuonId(trigger, extraCuts):
    result = cms.vstring(trigger, 'pass',
                "GlbOrTMwMatch", "pass",
                #"VBTF", "pass",
                "pt20", "above",
                "dxyPV0P5", "below",
                "dz1", "below",
                "PF", "pass",
                "SIP3", "below"
            )
    result += extraCuts
    return result  

noSteps = False

process.TnP_Trigger.binnedFit = cms.bool(True)
process.TnP_Trigger.binsForFit = cms.uint32(50) 

if noSteps:
    for (T,M) in [ ("DoubleMu17Mu8_Mu17","Track"),("DoubleMu17Mu8_Mu17","OurMuonID"),("DoubleMu17Mu8_Mu8","Track"),("DoubleMu17Mu8_Mu8","OurMuonID")]:
        print "--------------"
        print "Trigger: " + T
        print "From: " + M

        if M == 'OurMuonID':
            setattr(process.TnP_Trigger.Efficiencies, M + "_and_" + T + "_lumi_Eta2P4_for_" + run_files, cms.PSet(
                EfficiencyCategoryAndState = GetOurMuonId(T, ["eta2P4", "below"]),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = LUMI_ETA2P4,
                BinToPDFmap = cms.vstring("vpvPlusExpo")
                ))
        
            setattr(process.TnP_Trigger.Efficiencies, M + "_and_" + T + "_lumi_Eta1P2_for_" + run_files, cms.PSet(
                EfficiencyCategoryAndState = GetOurMuonId(T, ["eta1P2", "below"]),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = LUMI_ETA1P2,
                BinToPDFmap = cms.vstring("vpvPlusExpo")
                ))

            setattr(process.TnP_Trigger.Efficiencies, M + "_and_" + T + "_lumi_Eta0P8_for_" + run_files, cms.PSet(
                EfficiencyCategoryAndState = GetOurMuonId(T, ["eta0P8", "below"]),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = LUMI_ETA0P8,
                BinToPDFmap = cms.vstring("vpvPlusExpo")
                ))

            setattr(process.TnP_Trigger.Efficiencies, M + "_and_" + T + "_lumi_Eta2P4_Iso_for_" + run_files, cms.PSet(
                EfficiencyCategoryAndState = GetOurMuonId(T, ["eta2P4", "below", "combRelIso0P4", "below"]),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = LUMI_ETA2P4_ISO,
                BinToPDFmap = cms.vstring("vpvPlusExpo")
                ))
        
            setattr(process.TnP_Trigger.Efficiencies, M + "_and_" + T + "_lumi_Eta1P2_Iso_for_" + run_files, cms.PSet(
                EfficiencyCategoryAndState = GetOurMuonId(T, ["eta1P2", "below", "combRelIso0P4", "below"]),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = LUMI_ETA1P2_ISO,
                BinToPDFmap = cms.vstring("vpvPlusExpo")
                ))

            setattr(process.TnP_Trigger.Efficiencies, M + "_and_" + T + "_lumi_Eta0P8_Iso_for_" + run_files, cms.PSet(
                EfficiencyCategoryAndState = GetOurMuonId(T, ["eta0P8", "below", "combRelIso0P4", "below"]),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = LUMI_ETA0P8_ISO,
                BinToPDFmap = cms.vstring("vpvPlusExpo")
                ))

        elif M == "Track":
            setattr(process.TnP_Trigger.Efficiencies, M + "_and_" + T + "_lumi_for_" + run_files, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(T, "pass", "pt20", "above"),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = cms.PSet(
                    pt = cms.vdouble(minPtCut, 100),
                    bxInstLumi = cms.vdouble([1+0.25*x for x in range(0,17)])
                    ),
                BinToPDFmap = cms.vstring("vpvPlusExpo")
                ))

            # check eff vs pt (using no cuts)
            setattr(process.TnP_Trigger.Efficiencies, M + "_and_" + T + "_Pt_for_" + run_files, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(T, "pass"),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = cms.PSet(
                    pt = cms.vdouble(15, 25, 35, 100),
                    bxInstLumi = cms.vdouble([1+0.25*x for x in range(0,17)])
                    ),
                BinToPDFmap = cms.vstring("vpvPlusExpo")
                ))

else:
    T = "DoubleMu17Mu8_Mu17"
    print "in steps"
    print "Trigger", T

    setattr(process.TnP_Trigger.Efficiencies, "eta0P8_" + run_files, cms.PSet(
    EfficiencyCategoryAndState = cms.vstring("eta0P8", "below"),
    UnbinnedVariables = cms.vstring("mass"),
    BinnedVariables = LUMI_ETA0P8,
    BinToPDFmap = cms.vstring("vpvPlusExpo")
    ))

    setattr(process.TnP_Trigger.Efficiencies, "eta0P8_" + T + "_" + run_files, cms.PSet(
    EfficiencyCategoryAndState = cms.vstring("eta0P8", "below", T, "pass"),
    UnbinnedVariables = cms.vstring("mass"),
    BinnedVariables = LUMI_ETA0P8,
    BinToPDFmap = cms.vstring("vpvPlusExpo")
    ))

    setattr(process.TnP_Trigger.Efficiencies, "eta0P8_" + T + "_GlbMuon_" + run_files, cms.PSet(
    EfficiencyCategoryAndState = cms.vstring("eta0P8", "below", T, "pass", "GlbOrTMwMatch", "pass"),
    UnbinnedVariables = cms.vstring("mass"),
    BinnedVariables = LUMI_ETA0P8,
    BinToPDFmap = cms.vstring("vpvPlusExpo")
    ))

    setattr(process.TnP_Trigger.Efficiencies, "eta0P8_" + T + "_GlbMuon_PF_" + run_files, cms.PSet(
    EfficiencyCategoryAndState = cms.vstring("eta0P8", "below", T, "pass", "GlbOrTMwMatch", "pass", "PF", "pass"),
    UnbinnedVariables = cms.vstring("mass"),
    BinnedVariables = LUMI_ETA0P8,
    BinToPDFmap = cms.vstring("vpvPlusExpo")
    ))

    setattr(process.TnP_Trigger.Efficiencies, "eta0P8_" + T + "_GlbMuon_PF_dxy_" + run_files, cms.PSet(
    EfficiencyCategoryAndState = cms.vstring("eta0P8", "below", T, "pass", "GlbOrTMwMatch", "pass", "PF", "pass", "dxyPV0P5", "below"),
    UnbinnedVariables = cms.vstring("mass"),
    BinnedVariables = LUMI_ETA0P8,
    BinToPDFmap = cms.vstring("vpvPlusExpo")
    ))

    setattr(process.TnP_Trigger.Efficiencies, "eta0P8_" + T + "_GlbMuon_PF_dxy_dz_" + run_files, cms.PSet(
    EfficiencyCategoryAndState = cms.vstring("eta0P8", "below", T, "pass", "GlbOrTMwMatch", "pass", "PF", "pass", "dxyPV0P5", "below", "dz1", "below"),
    UnbinnedVariables = cms.vstring("mass"),
    BinnedVariables = LUMI_ETA0P8,
    BinToPDFmap = cms.vstring("vpvPlusExpo")
    ))

    setattr(process.TnP_Trigger.Efficiencies, "eta0P8_" + T + "_GlbMuon_PF_dxy_dz_SIP_" + run_files, cms.PSet(
    EfficiencyCategoryAndState = cms.vstring("eta0P8", "below", T, "pass", "GlbOrTMwMatch", "pass", "PF", "pass", "dxyPV0P5", "below", "dz1", "below", "SIP3", "below"),
    UnbinnedVariables = cms.vstring("mass"),
    BinnedVariables = LUMI_ETA0P8,
    BinToPDFmap = cms.vstring("vpvPlusExpo")
    ))

    setattr(process.TnP_Trigger.Efficiencies, "eta0P8_" + T + "_GlbMuon_PF_dxy_dz_SIP_pt_" + run_files, cms.PSet(
    EfficiencyCategoryAndState = cms.vstring("eta0P8", "below", T, "pass", "GlbOrTMwMatch", "pass", "PF", "pass", "dxyPV0P5", "below", "dz1", "below", "SIP3", "below", "pt20", "above"),
    UnbinnedVariables = cms.vstring("mass"),
    BinnedVariables = LUMI_ETA0P8,
    BinToPDFmap = cms.vstring("vpvPlusExpo")
    ))

    setattr(process.TnP_Trigger.Efficiencies, "eta0P8_" + T + "_GlbMuon_PF_dxy_dz_SIP_pt_iso_" + run_files, cms.PSet(
    EfficiencyCategoryAndState = cms.vstring("eta0P8", "below", T, "pass", "GlbOrTMwMatch", "pass", "PF", "pass", "dxyPV0P5", "below", "dz1", "below", "SIP3", "below", "pt20", "above", "combRelIso0P4", "below"),
    UnbinnedVariables = cms.vstring("mass"),
    BinnedVariables = LUMI_ETA0P8_ISO,
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


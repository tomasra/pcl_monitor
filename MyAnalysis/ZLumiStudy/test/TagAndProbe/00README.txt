##############################################################################
### Documentation of the procedure used to run the T&P code.

### 0. Documentation:

https://twiki.cern.ch/twiki/bin/view/CMS/MuonTagAndProbe
https://twiki.cern.ch/twiki/bin/view/CMS/TagAndProbeForHIG

### 1.Generation of the T&P trees

I setup a 52X area following the instructions in:
 
https://twiki.cern.ch/twiki/bin/view/CMS/TagAndProbeForHIG

recipe 4a:
cmsrel CMSSW_5_2_4_patch4 
cd CMSSW_5_2_4_patch4/src
cmsenv
cvs co -r V04-04-00 PhysicsTools/TagAndProbe
cvs co -r V02-00-03 MuonAnalysis/MuonAssociators
cvs co -r V08-00-06 MuonAnalysis/TagAndProbe
cvs co -r V06-04-34 DataFormats/PatCandidates 
scramv1 b
cd MuonAnalysis/TagAndProbe/test/zmumu/



On the top of this I modified the follwing thisngs:

- Add BX info to the tree:
Files
PhysicsTools/TagAndProbe/interface/BaseTreeFiller.h
PhysicsTools/TagAndProbe/src/BaseTreeFiller.cc:

The output of 
cvs diff -u8p PhysicsTools/TagAndProbe/interface/BaseTreeFiller.h
is saved in:
BaseTreeFiller_h.patch

The output of
cvs diff -u8p PhysicsTools/TagAndProbe/src/BaseTreeFiller.cc
is saved in:
BaseTreeFiller_cc.patch

- Add the exact ID implemented in the analysis trees to the T&P flags
 
cvs diff -u8p MuonAnalysis/TagAndProbe/python/common_variables_cff.py
is saved in:
common_variables_cff.patch

- the crab cfg used for running the job is in the directory 
Data2012_TPV0

The output has been saved in:
/store/caf/user/cerminar/ZLumiStudy/TPV0/

- I check for duplicates using 
UserCodecerminar/Tools/MyCondTools/scripts/checkOutputDir.py


### 2. Adding the inst lumi information to the trees
- the trees need to be sorted for better performance
To generate the input file list:
python buildinputlist.py -n TPV0_SingleMu_Run2012B-PromptReco-v1.h /store/caf/user/cerminar/ZLumiStudy/TPV0/Data_SingleMu_Run2012B-PromptReco-v1/ 

python buildinputlist.py -n TPV0_SingleMu_Run2012A-PromptReco-v1.h /store/caf/user/cerminar/ZLumiStudy/TPV0/Data_SingleMu_Run2012A-PromptReco-v1/ 

to actually sort the trees:

.x sortTPTrees.r

NOTE you have to setup input and output parameters editing the 2 lines:
  gROOT->Macro("TPV0_SingleMu_Run2012B-PromptReco-v1.h");
  outDir = TString("/data1/ZLumiStudy/TagAndProbe/TPV0/Test1/");

in the file to point at the correct input list and outputDir



- the lumi inst information for the BX needs to be added to the tree
.x addLumiInfoToTPTrees.r+

NOTE: for some reason needs to be run 2 times after each compilation....

Also in this case you need to generate the list of files using
python buildinputlist.py -s local -n TPV0_SingleMu_Run2012B-PromptReco-v1_sorted.h /data1/ZLumiStudy/TagProbe/SingleMu_Run2012B-PromptReco-v1/

python buildinputlist.py -s local -n TPV0_SingleMu_Run2012A-PromptReco-v1_sorted.h /data1/ZLumiStudy/TagProbe/SingleMu_Run2012A-PromptReco-v1/


and than you need to set it in the script:
  gROOT->Macro("TPV0_SingleMu_Run2012B-PromptReco-v1.h");
  outDir = TString("/data1/ZLumiStudy/TagAndProbe/TPV0/SingleMu_Run2012B-PromptReco-v1_lumi/");

At the moment the files sit on lxcms136
- file sorted per run # /data1/ZLumiStudy/TagAndProbe/TPV0/SingleMu_Run2012B-PromptReco-v1/
- file with lumi info by BX
/data1/ZLumiStudy/TagAndProbe/TPV0/SingleMu_Run2012B-PromptReco-v1_lumi/

I only produced the _lumi.root for Run2012B, Daniela can you try to reproduce the for Run2012A?


The last set of trees is the one to be used to fit the efficiencies

### 3. Fitting the efficiencies

Note: 
to run this you just need:
cvs co -r V04-04-00 PhysicsTools/TagAndProbe
cvs co -r V08-03-15 PhysicsTools/Utilities

The best documnenbtation for this step is:

https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideTagProbeFitTreeAnalyzer?redirectedfrom=CMS.SWGuideTagProbeFitTreeAnalyzer


- Tag muon definition:


process.tagMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("pt > 15 && isPFMuon && numberOfMatchedStations > 1 && muonID(\'GlobalMuonPromptTight\') && abs(dB) < 0.2 && track.hitPattern.trackerLayersWithMeasurement > 5 && track.hitPattern.numberOfValidPixelHits > 0 && !triggerObjectMatchesByCollection(\'hltL3MuonCandidates\').empty()")
)


- the fit of the trigger efficiency is:
cmsRun fitTrigger_byLumi.py

To edit the selections please have a look at the section "SETTINGS"

In particular check the binning of the lumi
and the minPtCut should that should match what is used in your analysis

BinToPDFmap controls the pdf which is used


Note for convenience it also produces a dump.py of the py each time it is
run so that you can read it easily

Note also the selection of the Tag muon needs to be checked looking at
the results that we get for the failing probes.


- fit of the ID efficiency:

* How to translate the ID defintion in the Tag and probe flags:

The variables in the tree are all defined in:
http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/MuonAnalysis/TagAndProbe/python/common_variables_cff.py?revision=1.40&view=markup

Here I list those that you need to use to implement the MuonID the we
are using:


global-muon || (tracker-muon && # matches > 0) -> corresponds to the
'GlbOrTMwMatch' Category

pt>5GeV -> actually use the threshold on the variable "pt" that you
use in the analyis

|eta|<2.4 or |eta| < 1.2 for the barrel only bin -> 'abseta" variable

dxy (from PV) < 0.5 cm -> corresponds to 'dxyPVdzmin'
dz < 1 cm -> corresponds to 'dzPV'

In the tree we save the following flags for further selection:

ID = PF muon (PF = particle flow) ID -> Corresponds to the 'PF' category
SIP = 3D significance dell'Impact Parameter -> require SIP < 0.4 ->
use the 'SIP' variable

The variable defining the lumiByBx is: bxInstLumi


Forget about the isolation for the moment....

To actually run the fit:
cmsRun fitMuonID_lumi.py


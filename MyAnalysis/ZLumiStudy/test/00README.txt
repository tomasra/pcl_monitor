-*-outline -*-

Thi file contains the instructions about how to run the lumi study
using the Z to study the BX by BX lumi behavior


* Setup


The 533 setup for the HZZ4l infrastructure is described in:

http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/CJLST/ZZAnalysis/README.txt?revision=1.15&view=markup

apart from the tag;
cvs co -d ZZAnalysis/AnalysisStep -r namapane120926_PostICHEP UserCode/CJLST/ZZAnalysis/AnalysisStep

Note: youmight want to add 
cvs co -d CMGTools/Production UserCode/CMG/CMGTools/Production
to get the discovery tools needed for the CMG stuff.


on the top you need to checkout our analysis package

cvs co -d MyAnalysis/ZLumiStudy -r UserCode/cerminar/MyAnalysis/ZLumiStudy


* Running the ntuple production

The main cfg is 

MyAnalysis/ZLumiStudy/test/analysis_cfg.py
This is imported by the various 

analysis_DATA_2012_cfg.py

which actually set the parameters for MC/data...
(at the moment only 1 exists but we might need 1 for each sample)


* CMG Ntuples


** Releases CMG Tools:

https://twiki.cern.ch/twiki/bin/viewauth/CMS/CMGToolsReleasesExperimental#Colin_533_V5_7_0

** Samples:
https://twiki.cern.ch/twiki/bin/view/CMS/CmgSamplesSeptember12

They are in 
/eos/cms/store/cmst3/user/cmgtools/CMG


You can use also the CMG discovery tool:
getInfo.py -s "SELECT distinct(dataset_id), file_owner, path_name,
dataset_fraction FROM dataset_details WHERE path_name LIKE '%V5_4_0'"

(you need 
cvs co -d CMGTools/Production UserCode/CMG/CMGTools/Production   
)

where the release refers to the CMG tool rlease as in:
https://twiki.cern.ch/twiki/bin/view/CMS/CMGToolsReleasesExperimental

* submitting the Jobs on the CMGTuples on the batch system

You need to checkout:
cvs co -d Tools/MyAnalysisTools UserCode/cerminar/Tools/MyAnalysisTools

Then you can submit using the cfg in
MyAnalysis/ZLumiStudy/test/prod/submission.cfg
(the syntax is straightforward)

To create the configuration files:
submission.py --file submission.cfg --create

NOTE: this can take a while....

To submit the jobs:
submission.py --file submission.cfg --submit

To check the status
submission.py --file submission.cfg --status

This should return back for each job:
1. the tree file
2. the JSON file of the input cmgTuples
3. the and of the inputJson file and the JSON_FILE provided for
filtering

* getting the lumi from lumi-calc

cvs co  -r V04-01-06 RecoLuminosity/LumiDB


configure the lumiMonitor using the file
/MyAnalysis/ZLumiStudy/test/prod/53X_v0/lumi.cfg

To actually run:

lumiMonitor.py --read-lumi

reads the input JSON files (output of ht eproduction step), splits
them by run (storing the individual json files) and uses the run by
run json to get the BXbyBX lumi in csv files

The version of lumiCalc and of the DB is stored for each run in the file:
lumiCalcVersion.log


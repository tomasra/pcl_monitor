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

where the release refers to the CMG tool rlease as in:
https://twiki.cern.ch/twiki/bin/view/CMS/CMGToolsReleasesExperimental


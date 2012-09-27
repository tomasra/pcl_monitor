-*-outline -*-

Thi file contains the instructions about how to run the lumi study
using the Z to study the BX by BX lumi behavior


* Setup


The 533 setup for the HZZ4l infrastructure is described in:

http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/CJLST/ZZAnalysis/README.txt?revision=1.15&view=markup

apart from the tag;
cvs co -d ZZAnalysis/AnalysisStep -r namapane120926_PostICHEP UserCode/CJLST/ZZAnalysis/AnalysisStep



on the top you need to checkout our analysis package

cvs co -d MyAnalysis/ZLumiStudy -r UserCode/cerminar/MyAnalysis/ZLumiStudy


* Running the ntuple production

The main cfg is 

MyAnalysis/ZLumiStudy/test/analysis_cfg.py
This is imported by the various 

analysis_DATA_2012_cfg.py

which actually set the parameters for MC/data...
(at the moment only 1 exists)





** customize the GT to run on



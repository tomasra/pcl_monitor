#include "ZMuMuConfigHelper.h"
#include "ZMuMuConfigHelper.h"
#include <ZZAnalysis/AnalysisStep/interface/bitops.h>

using namespace std;
using namespace edm;

ZMuMuConfigHelper::ZMuMuConfigHelper(const ParameterSet& pset) :
  isMC_(pset.getUntrackedParameter<bool>("isMC")),
  theSetup(pset.getParameter<int>("setup")),
  theSampleType(pset.getParameter<int>("sampleType")),
  PD(pset.getParameter<std::string>("PD")),
  skimPaths(pset.getParameter<std::vector<std::string> >("skimPaths")),
  MCFilter(pset.getParameter<std::string>("MCFilterPath"))
  
{
  string channel = pset.getUntrackedParameter<string>("channel");
  theChannel = finalState(channel);
  
  // Check for inconsistent configurations
  if ((theSampleType != 2011 && theSampleType != 2012) ||
      ((theSampleType != theSetup) && (!isMC_ || theSampleType!=2011))) {
    cout << "ERROR: ZMuMuConfigHelper: inconsistent setup" << theSampleType << " " << theSetup << " " <<isMC_ << endl;
    abort();
  }
  
  
  if ((isMC_&&PD!="") || (!isMC_ && (PD!="DoubleEle" && PD!="DoubleMu" && PD!="MuEG"))) {
    cout << "ERROR: ZMuMuConfigHelper: isMC: " << isMC_ << " PD: " << PD << endl;
    abort();
  }    

  if (!isMC_&&MCFilter!="") {
    cout << "ERROR: ZMuMuConfigHelper: MCFilter= " << MCFilter << " when isMC=0" 
	 << endl;
    abort();
  }    
  
}

void
ZMuMuConfigHelper::eventInit(const edm::Event & event) {
  // Initialize trigger results table
  if (event.id()==cachedEvtId) return;
  if (event.getByLabel(InputTag("TriggerResults"), triggerResults)) { // Use ("TriggerResults","","HLT") for the original HLT bits
    triggerNames = &(event.triggerNames(*triggerResults));
  } else {
    cout << "ERROR: failed to get TriggerResults" << endl;
  }
  cachedEvtId = event.id();
}

bool 
ZMuMuConfigHelper::passMCFilter(const edm::Event & event){
  if (MCFilter=="") return true;
  return passFilter(event, MCFilter);
}

bool 
ZMuMuConfigHelper::passSkim(const edm::Event & event, short& trigworld){
  bool evtPassSkim = false;
  if (skimPaths.size()==0) {
    evtPassSkim=true;
  } else {
    for (vector<string>::const_iterator name = skimPaths.begin(); name!= skimPaths.end(); ++name) {
      if (passFilter(event, *name)) {
	evtPassSkim = true; 
	break;
      }
    }
  }
  if (evtPassSkim) set_bit(trigworld,7);
  return evtPassSkim;
}

bool 
ZMuMuConfigHelper::passTrigger(const edm::Event & event, short& trigworld){
  bool evtPassTrigger = false;
  bool passDiMu  = passFilter(event, "triggerDiMu");
  
  if (passDiMu) evtPassTrigger = true;
  if (evtPassTrigger) set_bit(trigworld,0);
  if (passDiMu) set_bit(trigworld,1);
  
  return evtPassTrigger;
}

bool
ZMuMuConfigHelper::passFilter(const edm::Event & event, const string& filterPath) {
  eventInit(event);

  unsigned i =  triggerNames->triggerIndex(filterPath);
  if (i== triggerNames->size()){
    cout << "ERROR: ZMuMuConfigHelper::isTriggerBit: path does not exist! " << filterPath << endl;
    abort();
  }
  return triggerResults->accept(i);
}





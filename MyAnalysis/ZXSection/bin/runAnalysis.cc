#include <iostream>
#include <boost/shared_ptr.hpp>

#include "MyAnalysis/ZXSection/interface/ZSummaryHandler.h"
#include "MyAnalysis/ZXSection/interface/ZPhysicsEvent.h"

#include "Math/LorentzVector.h"
#include "Math/VectorUtil.h"


#include "CondFormats/JetMETObjects/interface/JetResolution.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "FWCore/PythonParameterSet/interface/MakeParameterSets.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TSystem.h"
#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TProfile.h"
#include "TNtuple.h"
#include "TLorentzVector.h"

using namespace std;


//Computes the Delta phi: the result is between 0 and pi 
double computeDeltaPhi(double phi1, double phi2) { 
  double deltaPhi = phi1 - phi2; 
  while(deltaPhi >= TMath::Pi()) deltaPhi -= 2*TMath::Pi(); 
  while(deltaPhi < -TMath::Pi()) deltaPhi += 2*TMath::Pi(); 
  return fabs(deltaPhi); 
} 
//



int main(int argc, char* argv[])
{
 // load framework libraries
  gSystem->Load( "libFWCoreFWLite" );
  AutoLibraryLoader::enable();

  //check arguments
  if ( argc < 2 ) {
    std::cout << "Usage : " << argv[0] << " parameters_cfg.py" << std::endl;
    return 0;
  }
  
  // ============================================================================
  // configure
  const edm::ParameterSet &runProcess = edm::readPSetsFrom(argv[1])->getParameter<edm::ParameterSet>("runProcess");
  TString url=runProcess.getParameter<std::string>("input");
  TString outdir=runProcess.getParameter<std::string>("outdir");
  bool isMC = runProcess.getParameter<bool>("isMC");
  //bool useFitter = runProcess.getParameter<bool>("useFitter");

  int evStart=runProcess.getParameter<int>("evStart");
  int evEnd=runProcess.getParameter<int>("evEnd");
  TString dirname = runProcess.getParameter<std::string>("dirName");



  // ============================================================================
  // create the output file
  TString outUrl( outdir );
  gSystem->Exec("mkdir -p " + outUrl);
  outUrl += "/";
  outUrl += gSystem->BaseName(url);

  TFile *ofile=TFile::Open(outUrl, "recreate");



  // ============================================================================
  // open the input file and get events tree
  cout << "[runAnalysis] Open file: " << url << endl;
  TFile *file = TFile::Open(url);
  if(file==0) return -1;
  if(file->IsZombie()) return -1;
  ZSummaryHandler evSummaryHandler;
  
  if( !evSummaryHandler.attachToTree( (TTree *)file->Get(dirname) ) ) {
    file->Close();
    return -1;
  }

  //check event range
  float rescaleFactor( evEnd>0 ?  float(evSummaryHandler.getEntries())/float(evEnd-evStart) : -1 );
  if(evEnd<0 || evEnd>evSummaryHandler.getEntries() ) evEnd=evSummaryHandler.getEntries();
  if(evStart > evEnd ) {
    file->Close();
    return -1;
  }

  // ============================================================================
  // run event loop
  for( int iev=evStart; iev<evEnd; iev++) {
    if(iev%1000==0) {
      cout << "[" << int(100*float(iev-evStart)/float(evEnd)) << "/100 ]" << endl;
    }
    
    // get the event
    evSummaryHandler.getEntry(iev);
    ZZ2l2nuSummary_t &ev=evSummaryHandler.getEvent();
    PhysicsEvent_t phys=getPhysicsEventFrom(ev);
    
    // get the event wwight
    float weight = ev.weight;
    if(!isMC) weight=1;


    //z kinematics
//     double dphill=deltaPhi(phys.leptons[0].phi(),phys.leptons[1].phi());
    LorentzVector zll=phys.leptons[0]+phys.leptons[1];

    cout << "Pt1: " <<  phys.leptons[0].pt() << endl;
  }
  
  
  
  //MC normalization (to 1/pb)
  float cnorm=1.0;
  if(isMC) {
    TString tag=gSystem->BaseName(url);
    tag.ReplaceAll(".root","");
    TH1F *cutflowH = (TH1F *) file->Get("evAnalyzer/"+tag+"/cutflow");
    if(cutflowH) {
      cnorm=cutflowH->GetBinContent(1);
    } else {
      cout << "[runAnalysis] no cut flow histo found" << endl;
    }
      if(rescaleFactor>0) cnorm /= rescaleFactor;
  }

  //all done with the events file
  file->Close();
  cout << outUrl << " " << cnorm << endl;
  ofile->cd();
  ofile->Close();
}  

#ifndef HistoZ_H
#define HistoZ_H


#include "TH1F.h"
#include "TH2F.h"


#include <iostream>
using namespace std; 

class HistoZ {
public:

  
  HistoZ(std::string name) : theName(name) {
    hMass = new TH1F(theName+"_hMass","Mass [GeV]",100,60,120);
    hMass->Sumw2();
  }


  HistoZ() : theName("") {
    hMass = 0;
  }


  HistoZ(std::string name, std::string dir, TFile *file) : theName(name) {
    if(dir != "") {
      dir = dir + "/";
    }

    hMass = (TH1F *) file->Get(TString(dir) + theName+"_hMass");
  }


 /* HistoZ * Clone(std::string name) {
    HistoZ *ret = new HistoZ();
    ret->theName = name;

    if(hMass != 0) hPhi->Clone((ret->theName+"_hMass").Data());

    return ret;
  }



  void Add(const HistoZ* histSet) {
    if(hMass != 0) hPhi->Add(histSet->hMass);
  }
*/


  void Scale(double scaleFact) {
    if(hMass != 0) hMass->Scale(scaleFact);
  }


  void Write() {
    //if(hMass != 0) 
      hMass->Write();
  }
  
  void Fill(double mass, double weight) {
    hMass->Fill(mass, weight);
  }

  /// Destructor
  virtual ~HistoZ() {}

  // Operations
  TString theName;

  TH1F *hMass;

};


#endif

#if !defined(__CINT) || defined(__MAKECINT__)

#include "TH1F.h"
#include "TH2F.h"

#include "TStyle.h"
#include "TString.h"
#include "TFile.h"
#include "TROOT.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include "TGraphErrors.h"
#include "TCanvas.h"

//#include "macros.C"
#include "root_lib/LumiFileReaderByBX.h"

// #include "HistoAlat.h"
#include <iostream>
#include <string>
#include <vector>
#endif

using namespace std;

bool debug = false;


//172822

bool doLumiCalc1 = true;
bool doLumiCalc2 = false;

bool doPromptV6 = false;

bool doSingleMu = false;

int nRunsMax = 10;


void plotLumi() {
  LumiFileReaderByBX lumiMap("/data/fguatier/JsonPipe/");
  //  LumiFileReaderByBX lumiMap2("/data/fguatier/JsonPipe2/");
  LumiFileReaderByBX lumiMap2("/data/LumiCalc/CMSSW_4_2_8/src/");

  int run = 172949;
  int maxLS = 800;
  int maxBX = 3426;

  TH1F *hBxLumi1 = new TH1F("hBxLumi1", "Integrated Lumi per BX", maxBX, 0, maxBX );
  TH1F *hBxLumi2 = new TH1F("hBxLumi2", "Integrated Lumi per BX", maxBX, 0, maxBX );
  

  lumiMap.checkCache(run);
  lumiMap.readFileForRun(run);
  lumiMap2.readFileForRun(run);


  


  for(int ls = 1; ls != maxLS; ++ls) { // loop over LS
    for(int bx = 1; bx != maxBX; ++bx) {// loop over BX
      RunLumiBXIndex runAndLumiAndBx(run, ls, bx);
      double instLumi = lumiMap.getAvgInstLumi(runAndLumiAndBx);
      double instLumi2 = lumiMap2.getAvgInstLumi(runAndLumiAndBx);
      
      if(instLumi != -1) hBxLumi1->Fill(bx, instLumi);
      if(instLumi2 != -1) hBxLumi2->Fill(bx, instLumi2);
    }
  }



  TCanvas *c1 = new TCanvas("cBxLumi1","cBxLumi1");
  hBxLumi1->Draw();

  TCanvas *c2 = new TCanvas("cBxLumi2","cBxLumi2");
  hBxLumi2->Draw();

  TCanvas *c3 = new TCanvas("cRatio1Over2","cRatio1Over2");
  TH1F *hRatio = (TH1F *) hBxLumi1->Clone("hRatio");
  hRatio->Divide(hBxLumi2);
  hRatio->Draw();


}

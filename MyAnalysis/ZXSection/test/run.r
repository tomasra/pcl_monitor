#if !defined(__CINT) || defined(__MAKECINT__)

#include "TH1F.h"
#include "TStyle.h"
#include "TString.h"
#include "TFile.h"
#include "TROOT.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include "TGraphErrors.h"

//#include "macros.C"
#include "root_lib/LumiFileReader.h"

// #include "HistoAlat.h"
#include <iostream>
#include <string>
#include <vector>
#endif

using namespace std;

bool debug = false;
double massMin = 91.-15.;
double massMax = 91.+15.;


//172822

void run() {
  LumiFileReader lumiMap;
  lumiMap.readFile("/data/Analysis/LumiDB/Lumi1-May10.csvt");
  lumiMap.readFile("/data/Analysis/LumiDB/Lumi2-PromptV4.csvt");
  lumiMap.readFile("/data/Analysis/LumiDB/Lumi3-Aug5.csvt");
//   lumiMap.readFile("/data/Analysis/LumiDB/Lumi4-PromptV6.csvt");

//   lumiMap.readFile("/data/Analysis/LumiDB/Lumi1d-v2-May10.csvt");
//   lumiMap.readFile("/data/Analysis/LumiDB/Lumi2d-v2-PromptV4.csvt");
//   lumiMap.readFile("/data/Analysis/LumiDB/Lumi3d-v2-Aug5.csvt");
// //   lumiMap.readFile("/data/Analysis/LumiDB/Lumi4d-v2-PromptV6.csvt");


  
  cout << lumiMap.getRecIntegralInLumiBin(378.301, 578.38).first << endl;
  cout << lumiMap.getRecIntegralInLumiBin(578.38, 675.509).first << endl;
  cout << lumiMap.getRecIntegralInLumiBin(675.509, 734.303 ).first << endl;
  cout << lumiMap.getRecIntegralInLumiBin(734.303 ,789.625).first << endl;

  cout << "Total rec. lumi: " << lumiMap.getRecIntegral(RunLumiIndex(1,1),RunLumiIndex(300000,1)) << endl;

  vector<TString> fileNames;
  fileNames.push_back("/data/Analysis/42X_110823/DoubleMuMay10ReReco.root");
  fileNames.push_back("/data/Analysis/42X_110823/DoubleMuPromptRecov4.root");
  fileNames.push_back("/data/Analysis/42X_110823/DoubleMu05AugReReco.root");
  fileNames.push_back("/data/Analysis/42X_110823/SingleMu05AugReReco.root");
  fileNames.push_back("/data/Analysis/42X_110823/SingleMuPromptRecov4.root");
  fileNames.push_back("/data/Analysis/42X_110823/SingleMuMay10ReReco.root");

//    fileNames.push_back("/data/Analysis/42X_110823/SingleMuPromptRecov6_172620_173244.root");

//    fileNames.push_back("/data/Analysis/42X_110823/DoubleMuPromptRecov6_172620_173244.root");

  int run = -1;
  int ls = -1;
  float p1x, p1y, p1z, e1;
  float p2x, p2y, p2z, e2;

  
  TFile *outFile = new TFile("outFile.root","recreate");

  TH1F *hEventPerLumi = new TH1F("hEventPerLumi", "# events; avg. inst. lumi. [Hz/um]", 20, 200, 2000);

  for(vector<TString>::const_iterator file = fileNames.begin();
      file != fileNames.end(); ++file) {
    TFile* rFile = new TFile((*file).Data());
    TTree *tree = (TTree*) rFile->Get("evAnalyzer/data"); 

    tree->SetBranchAddress("run", &run);
    tree->SetBranchAddress("lumi", &ls);
    tree->SetBranchAddress("l1_px", &p1x);
    tree->SetBranchAddress("l1_py", &p1y);
    tree->SetBranchAddress("l1_pz", &p1z);
    tree->SetBranchAddress("l1_en", &e1);
    tree->SetBranchAddress("l2_px", &p2x);
    tree->SetBranchAddress("l2_py", &p2y);
    tree->SetBranchAddress("l2_pz", &p2z);
    tree->SetBranchAddress("l2_en", &e2);
    

    for(int entry = 0; entry != tree->GetEntries(); ++entry) {
      tree->GetEntry(entry);
      if(debug)    cout << run << ":" << ls << endl;

//       if(run != 163817) continue; 

      RunLumiIndex runAndLumi(run, ls);
      double instLumi = lumiMap.getAvgInstLumi(runAndLumi);
      if(instLumi < 0.1) {
	cout << run << ":" << ls << "    inst lumi: " << instLumi << " Hz/ub" << endl;
      }
      if(debug)      cout << "    inst lumi: " << instLumi << " Hz/ub" << endl;

      TLorentzVector lept1(p1x, p1y, p1z, e1);
      if(debug)      cout << lept1.Px() << " " <<  lept1.Py() << " " << lept1.Pz() << " " << lept1.E() << endl;
      TLorentzVector lept2(p2x, p2y, p2z, e2);
      if(debug)      cout << lept2.Px() << " " <<  lept2.Py() << " " << lept2.Pz() << " " << lept2.E() << endl;
      
      TLorentzVector zBoson = lept1 + lept2;
      double mass = zBoson.M();
      if(debug)      cout << "    mass: " << mass << endl;

      if(mass >= massMin && mass <= massMax) { //cut on Z mass
	hEventPerLumi->Fill(instLumi);
      }

      
    }

  }
  
  TH1F *hRecLumiInteg = new TH1F("hRecLumiInteg", "rec. lumi. integ.; rec. lumi. integ. [1/ub]", hEventPerLumi->GetNbinsX(), 200, 2000);

  double avgInstLumi[hEventPerLumi->GetNbinsX()];
  double xsec[hEventPerLumi->GetNbinsX()];
  double xsecErr[hEventPerLumi->GetNbinsX()];
  double avgInstLumiErr[hEventPerLumi->GetNbinsX()];


  // fill the recorded lumi for each bin
  for(int bin = 1; bin <= hEventPerLumi->GetNbinsX(); ++bin) {

    double lowEdge = hEventPerLumi->GetBinLowEdge(bin);
    double width = hEventPerLumi->GetBinWidth(bin);
    double upEdge = lowEdge + width;
    pair<double, double> integAndMean = lumiMap.getRecIntegralInLumiBin(lowEdge, upEdge);
    double recLumiInteg = integAndMean.first;
    avgInstLumi[bin-1] = integAndMean.second;
    xsec[bin-1] = hEventPerLumi->GetBinContent(bin)/recLumiInteg;
    xsecErr[bin-1] = sqrt( hEventPerLumi->GetBinContent(bin)) / recLumiInteg;
    avgInstLumiErr[bin-1] = 0;
    cout << "bin: " << bin << " from: " << lowEdge << " to: " << upEdge << " lumi: " << integAndMean.first
	 << " mean inst lumi: " <<  integAndMean.second << endl;
    hRecLumiInteg->SetBinContent(bin, recLumiInteg);
    hRecLumiInteg->SetBinError(bin, recLumiInteg*0.045);
    
  }

  TH1F *hSigma = (TH1F *) hEventPerLumi->Clone("hSigma");
  
  hSigma->Divide(hRecLumiInteg);
  hSigma->SetTitle("effective sigma (ub) vs avg. inst. lumi; avg. inst. lumi [Hz/ub]");
  TGraphErrors *gSigma  = new TGraphErrors(hEventPerLumi->GetNbinsX(), avgInstLumi, xsec, 0, xsecErr);
  gSigma->SetName("gSigma");
  gSigma->SetTitle("effective sigma (ub) vs avg. inst. lumi; avg. inst. lumi [Hz/ub]");

  outFile->cd();
  hEventPerLumi->Write();
  hRecLumiInteg->Write();
  gSigma->Write();
  hSigma->Write();
  outFile->Close();


}

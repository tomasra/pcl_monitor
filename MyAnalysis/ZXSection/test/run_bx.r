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

//#include "macros.C"
#include "root_lib/LumiFileReaderByBX.h"

// #include "HistoAlat.h"
#include <iostream>
#include <string>
#include <vector>

#include "TStopwatch.h"

#endif

using namespace std;

bool debug = false;
double massMin = 91.-15.;
double massMax = 91.+15.;


//172822

bool doLumiCalc1 = true;
bool doLumiCalc2 = false;

bool doPromptV6 = true;

bool doSingleMu = false;

int nRunsMax = 1000;


float binMin = 0.2; //Hz/ub
float binMax = 2.0; //Hz/ub
int nBins = 20;


void run_bx() {

  TStopwatch watch;

  TString lumiDir = "";

  if(doLumiCalc1) {
    lumiDir = "/data/fguatier/JsonPipe/";
  } else if() {
    lumiDir = "/data/fguatier/JsonPipe2/";
  }


  LumiFileReaderByBX lumiMap();
//   if(doLumiCalc1) {
//     lumiMap.readFile("/data/Analysis/LumiDB/Lumi1-May10.csvt");
//     lumiMap.readFile("/data/Analysis/LumiDB/Lumi2-PromptV4.csvt");
//     lumiMap.readFile("/data/Analysis/LumiDB/Lumi3-Aug5.csvt");
//     if(doPromptV6) lumiMap.readFile("/data/Analysis/LumiDB/Lumi4-PromptV6.csvt");
//   } else {
//     lumiMap.readFile("/data/Analysis/LumiDB/Lumi1d-v2-May10.csvt");
//     lumiMap.readFile("/data/Analysis/LumiDB/Lumi2d-v2-PromptV4.csvt");
//     lumiMap.readFile("/data/Analysis/LumiDB/Lumi3d-v2-Aug5.csvt");
//     if(doPromptV6) lumiMap.readFile("/data/Analysis/LumiDB/Lumi4d-v2-PromptV6.csvt");
//   }
  



  
//   cout << lumiMap.getRecIntegralInLumiBin(378.301, 578.38).first << endl;
//   cout << lumiMap.getRecIntegralInLumiBin(578.38, 675.509).first << endl;
//   cout << lumiMap.getRecIntegralInLumiBin(675.509, 734.303 ).first << endl;
//   cout << lumiMap.getRecIntegralInLumiBin(734.303 ,789.625).first << endl;

//   cout << "Total rec. lumi: " << lumiMap.getRecIntegral(RunLumiIndex(1,1),RunLumiIndex(300000,1)) << endl;

  int nRunCounter = 0;


  vector<TString> fileNames;
  fileNames.push_back("/data/Analysis/42X_BX_v0/DoubleMu-May10ReReco_sorted.root");
  fileNames.push_back("/data/Analysis/42X_BX_v0/DoubleMu-PromptReco-v4_sorted.root");
  fileNames.push_back("/data/Analysis/42X_BX_v0/DoubleMu-05Aug2011_sorted.root");
  if(doPromptV6) fileNames.push_back("/data/Analysis/42X_BX_v0/DoubleMu-PromptReco-v6_sorted.root");
  if(doSingleMu) {
    fileNames.push_back("/data/Analysis/42X_BX_v0/SingleMu-05Aug2011_sorted.root");
    fileNames.push_back("/data/Analysis/42X_BX_v0/SingleMu-PromptReco-v4_sorted.root");
    fileNames.push_back("/data/Analysis/42X_BX_v0/SingleMu-May10ReReco_sorted.root");
    if(doPromptV6) fileNames.push_back("/data/Analysis/42X_BX_v0/SingleMu-PromptReco-v6_sorted.root");

  }
  
  // the variables from the tree
  int run = -1;
  int ls = -1;
  int bx = -1;
  float p1x, p1y, p1z, e1;
  float p2x, p2y, p2z, e2;

  // define the output file
  TString outFileName = "outFile_";
  if(doLumiCalc1) {
    outFileName += "lc1.root";
  } else {
    outFileName += "lc2.root";
  }
  TFile *outFile = new TFile(outFileName.Data(),"recreate");


  // book the histograms
  TH1F *hEventPerLumi = new TH1F("hEventPerLumi", "# events; avg. inst. lumi. [Hz/um]; # events",
				 nBins, binMin, binMax);
  TH1F *hRecLumiInteg = new TH1F("hRecLumiInteg", "rec. lumi. integ.; avg. inst. lumi. [Hz/ub]; int lumi [1/ub]",
				 nBins, binMin, binMax);


  TH2F *hZMassVsLumi = new TH2F("hZMassVsLumi", "# events; avg. inst. lumi. [Hz/ub]", 20, 0.2, 2, 80, 50, 130);


  
  for(vector<TString>::const_iterator file = fileNames.begin();
      file != fileNames.end(); ++file) { // loop over the files
    // open the tree
    TFile* rFile = new TFile((*file).Data());
    TTree *tree = (TTree*) rFile->Get("data"); 

    tree->SetBranchAddress("run", &run);
    tree->SetBranchAddress("lumi", &ls);
    tree->SetBranchAddress("bx", &bx);
    tree->SetBranchAddress("l1_px", &p1x);
    tree->SetBranchAddress("l1_py", &p1y);
    tree->SetBranchAddress("l1_pz", &p1z);
    tree->SetBranchAddress("l1_en", &e1);
    tree->SetBranchAddress("l2_px", &p2x);
    tree->SetBranchAddress("l2_py", &p2y);
    tree->SetBranchAddress("l2_pz", &p2z);
    tree->SetBranchAddress("l2_en", &e2);
    

    int nEntriesMax = tree->GetEntries();
    watch.Start();    
    
    // loop over all the entries
    for(int entry = 0; entry != nEntriesMax; ++entry) {
      tree->GetEntry(entry);
      if(run > 172802) break;
      if(entry %1000 == 0) cout << "processing entry #: " << entry << endl;
      if(debug)    cout << run << ":" << ls << endl;
      if(lumiMap.checkCache(run)) nRunCounter++;
      if(nRunCounter> nRunsMax) break;

      if(lumiMap.checkCache(run) && entry != 0) { // this run was not already cached
	cout << "read a new file and fill the bins for the previous one!" << endl;
	TH1F *histo = lumiMap.getRecLumiBins(nBins, binMin, binMax);
	hRecLumiInteg->Add(histo);
      }

      // flush the previous run from the cache and read a new one
      lumiMap.readFileForRun(run);
      //       if(run  > 163339) break;

      // BX identifier
      RunLumiBXIndex runAndLumiAndBx(run, ls, bx);
      
      // get the inst. lumi for this event
      double instLumi = lumiMap.getAvgInstLumi(runAndLumiAndBx);
      //       if(instLumi < 0.1) {
      // 	cout << run << ":" << ls << ":" << bx
      // << "    inst lumi: " << instLumi << " Hz/ub" << endl;
      //       }
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
	hZMassVsLumi->Fill(instLumi, mass);
      }

      
    }
    watch.Stop();
    cout << watch.CpuTime() << endl;
    watch.Print("u");

  }
  TH1F *histo = lumiMap.getRecLumiBins(nBins, binMin, binMax);
  hRecLumiInteg->Add(histo);


//   double avgInstLumi[hEventPerLumi->GetNbinsX()];
//   double xsec[hEventPerLumi->GetNbinsX()];
//   double xsecErr[hEventPerLumi->GetNbinsX()];
//   double avgInstLumiErr[hEventPerLumi->GetNbinsX()];


//   // fill the recorded lumi for each bin
//   for(int bin = 1; bin <= hEventPerLumi->GetNbinsX(); ++bin) {

//     double lowEdge = hEventPerLumi->GetBinLowEdge(bin);
//     double width = hEventPerLumi->GetBinWidth(bin);
//     double upEdge = lowEdge + width;
//     pair<double, double> integAndMean = lumiMap.getRecIntegralInLumiBin(lowEdge, upEdge);
    
//     double recLumiInteg = integAndMean.first;
//     avgInstLumi[bin-1] = integAndMean.second;
//     xsec[bin-1] = hEventPerLumi->GetBinContent(bin)/recLumiInteg;
//     xsecErr[bin-1] = sqrt( hEventPerLumi->GetBinContent(bin)) / recLumiInteg;
//     avgInstLumiErr[bin-1] = 0;
//     cout << "bin: " << bin << " from: " << lowEdge << " to: " << upEdge << " lumi: " << integAndMean.first
// 	 << " mean inst lumi: " <<  integAndMean.second << endl;
//     hRecLumiInteg->SetBinContent(bin, recLumiInteg);
//     hRecLumiInteg->SetBinError(bin, recLumiInteg*0.045);
    
//   }

  TH1F *hSigma = (TH1F *) hEventPerLumi->Clone("hSigma");
  
  hSigma->Divide(hRecLumiInteg);
  hSigma->SetTitle("effective sigma (ub) vs avg. inst. lumi; avg. inst. lumi [Hz/ub]");
//   TGraphErrors *gSigma  = new TGraphErrors(hEventPerLumi->GetNbinsX(), avgInstLumi, xsec, 0, xsecErr);
//   gSigma->SetName("gSigma");
//   gSigma->SetTitle("effective sigma (ub) vs avg. inst. lumi; avg. inst. lumi [Hz/ub]");

  outFile->cd();
  hEventPerLumi->Write();
  hRecLumiInteg->Write();
//   gSigma->Write();
  hSigma->Write();
  hZMassVsLumi->Write();
  outFile->Close();

  cout << watch.CpuTime() << endl;
}

#define fitResSlope_cxx

#include "fitResSlope.h"

#include <TH2.h>
#include <TF1.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TGraphErrors.h>

#include <fstream>
#include <vector>
#include <string>
#include <iostream>
#include <sstream>

using namespace::std;

fitResSlope::fitResSlope(TTree *tree)
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("residualFits_hqPhiV.root");
      if (!f) {
         f = new TFile("residualFits_hqPhiV.root");
      }
      tree = (TTree*)gDirectory->Get("res_tree");

   }
   Init(tree);

   for(int wheel=0;wheel<5;wheel++){
     for(int sector=0;sector<14;sector++){
       for(int station=0;station<4;station++){
	 for(int sl=0;sl<3;sl++){
	   ttrigCorr[wheel][sector][station][sl] = 0.;
	 }
       }
     }
   }

}

fitResSlope::~fitResSlope()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t fitResSlope::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t fitResSlope::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (!fChain->InheritsFrom(TChain::Class()))  return centry;
   TChain *chain = (TChain*)fChain;
   if (chain->GetTreeNumber() != fCurrent) {
      fCurrent = chain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void fitResSlope::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("ttrig", &ttrig, &b_ttrig);
   fChain->SetBranchAddress("wheel", &wheel, &b_theWheel);
   fChain->SetBranchAddress("station", &station, &b_theStation);
   fChain->SetBranchAddress("sector", &sector, &b_theSector);
   fChain->SetBranchAddress("sl", &sl, &b_theSL);
   fChain->SetBranchAddress("res_mean", &res_mean, &b_res_mean);
   fChain->SetBranchAddress("res_mean_err", &res_mean_err, &b_res_mean_err);
   fChain->SetBranchAddress("res_sigma1", &res_sigma1, &b_res_sigma1);
   fChain->SetBranchAddress("res_sigma2", &res_sigma2, &b_res_sigma2);
   fChain->SetBranchAddress("t0seg", &t0seg, &b_t0seg);
   fChain->SetBranchAddress("chi2", &chi2, &b_chi2);
   Notify();
}

Bool_t fitResSlope::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void fitResSlope::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t fitResSlope::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}

void fitResSlope::Loop()
{
  if (fChain == 0) return;

  gROOT->SetStyle("Plain");
  gStyle->SetOptFit(0111);
  gStyle->SetMarkerStyle(20);
  gStyle->SetMarkerSize(0.7);

  Long64_t nentries = fChain->GetEntriesFast();

  //indexes are wheel,sector,station,SL,ttrig
  Double_t Ares_mean[5][14][4][3][5];
  Double_t Ares_mean_err[5][14][4][3][5];

  Double_t t0res_mean[5][14][4][3][5];

  Double_t deltaTtrig[5] = {-4.,-2.,0.,2.,4.};

  TCanvas c1;
  TCanvas c2;

  Int_t count = 0;

  Long64_t nbytes = 0, nb = 0;
  for (Long64_t jentry=0; jentry<nentries;jentry++) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;
    // if (Cut(ientry) < 0) continue;

    int tmp_ttrig;
    if(ttrig == -2) tmp_ttrig = 0;
    else if(ttrig == -1) tmp_ttrig = 1;
    else if(ttrig ==  0) tmp_ttrig = 2;
    else if(ttrig ==  1) tmp_ttrig = 3;
    else if(ttrig ==  2) tmp_ttrig = 4;

    //cout << "w " << wheel << " sec " << sector << " station " << " sl " << endl;

    Ares_mean[wheel+2][sector-1][station-1][sl-1][tmp_ttrig] = res_mean;
    Ares_mean_err[wheel+2][sector-1][station-1][sl-1][tmp_ttrig] = res_mean_err;

    t0res_mean[wheel+2][sector-1][station-1][sl-1][tmp_ttrig] = t0seg;

    //cout << "resmean" << Ares_mean[wheel+2][sector-1][station-1][sl-1][tmp_ttrig]  << endl;

  }

  TH2F *hCorr = new TH2F("hCorr","DTtrig from t0 vs DTrig from res (ns)", 60, -15, 15, 60, -15, 15); 
  TH1F *hPar1_phi = new TH1F("hPar1_phi", "VDrift from fit (cm/ns)", 500, 0.001, 0.006); 
  TH2F *hPar1VsSect_phi = new TH2F("hPar1VsSect_phi", "VDrift from fit (cm/ns) vs sector", 12,1,13,50, 0.0035, 0.0055); 
  TH2F *hPar1VsWheel_phi = new TH2F("hPar1VsWheel_phi", "VDrift from fit (cm/ns) vs wheel", 5,-2,3,50, 0.0035, 0.0055); 
  TH2F *hPar1VsStat_phi = new TH2F("hPar1VsStat_phi", "VDrift from fit (cm/ns) vs station", 4,1,5,50, 0.0035, 0.0055); 
  TH2F *hPar1VsChi2_phi = new TH2F("hPar1VsChi2_phi", "VDrift from fit (cm/ns) vs chi2", 50,0,10,50, 0.0035, 0.0055); 

  TH1F *hPar1_theta = new TH1F("hPar1_theta", "VDrift from fit (cm/ns)", 500, 0.001, 0.006); 

  ofstream fout("failed_sl.txt");

  for(Int_t mywheel = -2; mywheel<=2; mywheel++){
    for(Int_t mysector = 1; mysector<=12; mysector++){
      for(Int_t mystation = 1; mystation<=4; mystation++){
	for(Int_t mySL = 1; mySL<=3; mySL++){
	  // FIXME: skip SL theta for the moment
	  if(mySL == 2) continue;
	  //if(count == 10) break;

	  vector<Double_t> mymean;
	  vector<Double_t> mymean_err;
	  vector<Double_t> x_mean;
	  vector<Double_t> x_err;

	  vector<Double_t> myt0;
	  vector<Double_t> myt0_err;
	  vector<Double_t> x_t0;
	  vector<Double_t> x_err_t0;

	  int count_valid_points(0);

	  for(Int_t myttrig = 0; myttrig < 5; myttrig++){

	    if(Ares_mean_err[mywheel+2][mysector-1][mystation-1][mySL-1][myttrig] > 0.2) continue;

	    mymean.push_back(Ares_mean[mywheel+2][mysector-1][mystation-1][mySL-1][myttrig]);
	    mymean_err.push_back(Ares_mean_err[mywheel+2][mysector-1][mystation-1][mySL-1][myttrig]);
	    x_err.push_back(0.);
	    x_mean.push_back(deltaTtrig[myttrig]);

	    myt0.push_back(t0res_mean[mywheel+2][mysector-1][mystation-1][mySL-1][myttrig]);
	    myt0_err.push_back(0.5);
	    x_err_t0.push_back(0.);
	    x_t0.push_back(deltaTtrig[myttrig]);

	    count_valid_points++;
	  }

	  //cout << " res mean " << t0res_mean[mywheel+2][mysector-1][mystation-1][mySL-1][2] << endl;

	  if(count_valid_points < 2){
	    fout << mywheel << " " << mysector << " " << mystation << " " << mySL << endl;
	    continue;
	  }

	  TGraphErrors mygr(mymean.size(),&x_mean[0],&mymean[0],&x_err[0],&mymean_err[0]);
	  mygr.Fit("pol1");
	  TF1 * mygrFit = mygr.GetFunction("pol1");
	  double par0res = mygrFit->GetParameter("p0");
	  double par1res = mygrFit->GetParameter("p1");
	  double ttrigCorrRes  = 99999;
	  if(par1res != 0) ttrigCorrRes = -par0res/par1res;

	  ttrigCorr[mywheel+2][mysector-1][mystation-1][mySL-1] = par1res;

          string stringName1;
          stringstream theStream1;
          theStream1 <<  "Wh" << mywheel << "_Sect" << mysector << "_St"<< mystation << "_SL" << mySL;
          theStream1 >> stringName1;

	  mygr.SetTitle(stringName1.c_str());

	  c1.cd();
	  mygr.Draw("AP");

	  if(count == 0) c1.SaveAs("resplots.ps(");
	  else c1.SaveAs("resplots.ps");

	  TGraphErrors mygrt0(myt0.size(),&x_t0[0],&myt0[0],&x_err_t0[0],&myt0_err[0]);
	  mygrt0.Fit("pol1");

	  TF1 * mygrt0Fit = mygrt0.GetFunction("pol1");
	  double par0t0 = mygrt0Fit->GetParameter("p0");
	  double par1t0 = mygrt0Fit->GetParameter("p1");
	  double ttrigCorrT0    = 99999;
	  if(par1t0 != 0) ttrigCorrT0 = -par0t0/par1t0;

	  if(mySL != 2) {
	    hCorr->Fill(ttrigCorrRes, ttrigCorrT0);
	    hPar1_phi->Fill(-par1res);
	    hPar1VsSect_phi->Fill(mysector,-par1res);
	    hPar1VsWheel_phi->Fill(mywheel,-par1res);
	    hPar1VsStat_phi->Fill(mystation,-par1res);
	    hPar1VsChi2_phi->Fill(mygrFit->GetChisquare(), -par1res);
	    cout << " VDrift: " << par1res << endl;

	  } else {
	    hPar1_theta->Fill(-par1res);
	  }
	  mygrt0.SetTitle(stringName1.c_str());

	  c2.cd();
	  mygrt0.Draw("AP");

	  if(count == 0) c2.SaveAs("t0plots.ps(");
	  else c2.SaveAs("t0plots.ps");

	  count++;
	}
      }
    }
  }

  c1.cd();
  c1.SetGrid(1,1);
  hCorr->Draw("box");
  c1.SaveAs("resplots.ps");

  c1.cd();
  hPar1_phi->Draw();
  c1.SaveAs("resplots.ps");

  c1.cd();
  hPar1_theta->Draw();
  c1.SaveAs("resplots.ps");

  c1.cd();
  hPar1VsSect_phi->Draw("box");
  c1.SaveAs("resplots.ps");

  c1.cd();
  hPar1VsWheel_phi->Draw("box");
  c1.SaveAs("resplots.ps");

  c1.cd();
  hPar1VsStat_phi->Draw("box");
  c1.SaveAs("resplots.ps");

  c1.cd();
  hPar1VsChi2_phi->Draw("box");

  c1.SaveAs("resplots.ps)");
  c2.SaveAs("t0plots.ps)");
  
  return;
}

void fitResSlope::DumpCorrection(const char *filename)
{
  ifstream fin;
  fin.open(filename);
  if (!fin){
    cout << "Error opening file " << filename << endl;
    assert(0);
  }

  ofstream fout("outDB.txt");

  int tmp_wheel = 0;
  int tmp_sector = 0;
  int tmp_station = 0;
  int tmp_SL = 0;
  double tmp_ttrig = 0.;
  double tmp_t0 = 0.;
  double tmp_kfact = 0.;
  int tmp_a = 0;
  int tmp_b = 0;
  int tmp_c = 0;
  int tmp_d = 0;

  while(!fin.eof()){

    fin >> tmp_wheel >> tmp_sector >> tmp_station >> tmp_SL  >> tmp_a >> tmp_b >>
      tmp_ttrig >> tmp_t0 >> tmp_kfact >> tmp_c >> tmp_d;

    fout << " " << tmp_wheel << " " << tmp_sector << " " << tmp_station << " " <<
      tmp_SL << " " << tmp_a << " " << tmp_b << " " << tmp_ttrig << " " << tmp_t0 <<
      " " << tmp_kfact << " " << tmp_c << " " << tmp_d << " " <<
      ttrigCorr[tmp_wheel+2][tmp_sector-1][tmp_station-1][tmp_SL-1] << endl;
  }

  fin.close();
  fout.close();

  return;
}

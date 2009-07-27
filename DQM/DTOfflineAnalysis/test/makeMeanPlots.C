#define makeMeanPlots_cxx
#include "makeMeanPlots.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

void makeMeanPlots::Loop()
{
  //   In a ROOT session, you can do:
  //      Root > .L makeMeanPlots.C
  //      Root > makeMeanPlots t
  //      Root > t.GetEntry(12); // Fill t data members with entry number 12
  //      Root > t.Show();       // Show values of entry 12
  //      Root > t.Show(16);     // Read and show values of entry 16
  //      Root > t.Loop();       // Loop on all entries
  //

  //     This is the loop skeleton where:
  //    jentry is the global entry number in the chain
  //    ientry is the entry number in the current Tree
  //  Note that the argument to GetEntry must be:
  //    jentry for TChain::GetEntry
  //    ientry for TTree::GetEntry and TBranch::GetEntry
  //
  //       To read only selected branches, Insert statements like:
  // METHOD1:
  //    fChain->SetBranchStatus("*",0);  // disable all branches
  //    fChain->SetBranchStatus("branchname",1);  // activate branchname
  // METHOD2: replace line
  //    fChain->GetEntry(jentry);       //read all branches
  //by  b_branchname->GetEntry(ientry); //read only this branch
 
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

	  vector <Double_t> mymean;
	  vector <Double_t> mymean_err;
	  vector <Double_t> x_mean;
	  vector <Double_t> x_err;

	  vector <Double_t> myt0;
	  vector <Double_t> myt0_err;
	  vector <Double_t> x_t0;
	  vector <Double_t> x_err_t0;

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

	  cout << " res mean " << t0res_mean[mywheel+2][mysector-1][mystation-1][mySL-1][2] << endl;

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
// 	  int pippo;
// 	  cin >> pippo;
// 	  if(pippo == -1) goto end;
	}
      }
    }
  }
 end:
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
//   c1.SaveAs("resplots.ps");



  c1.SaveAs("resplots.ps)");
  c2.SaveAs("t0plots.ps)");
  

}

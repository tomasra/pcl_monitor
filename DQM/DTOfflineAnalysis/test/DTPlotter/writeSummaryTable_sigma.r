//------------------------------
//
// Write table of resolutions 
//
// only *ByLayer is acceptable 
//
// root -q -b writeSummaryTable_sigma.r
//
//
//------------------------------
#include <iomanip>

void writeSummaryTable_sigma() {

  gROOT->LoadMacro("macros2.C");
  gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/Histograms.h");
  gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/DTDetId.cc+");
  gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/Utils.cc+");
  

  // Configurable parameters --------------------

  //--- DATA:
  bool isMC = false;

//   TString filename = "ZMu_2012D_22jan13_BP7X_noDRR_statByLayer.root";
//   TString table = "sigma_2012D_22jan13_BP7X_noDRR_statByLayer.txt";

  TString filename = "DYJetsToLL_M-50_BP7X_noDRR_statByLayer.root";
  TString table = "sigma_DYJetsToLL_M-50_BP7X_noDRR_statByLayer.txt";

  if (filename.Contains("chamberByLayer")) {
    TString granularity = "SL";  // sectors independently, for chamberByLayer
  } else if  (filename.Contains("statByLayer")) {
    TString granularity = "stat";    // collapse sectors; for statByLayer
  } else {
    cout << "unknown granularity, exiting..." << endl;
    return;
  }



    // Interval for the fit of residual distributions
  float nsigma = 2.;

  //--------------------

  float cmToMicron = 10000.;

  ofstream f(table,ios_base::out);
  f << fixed;  
  f << "# W St sec SL vdrift resolution " << endl;

  
  TFile *file = new TFile(filename);


  TH1F* hsigmaTheta = new TH1F("hsigmaTheta","hsigmaTheta", 15,1.33 , 1.63);
  TH1F* hsigmaphirapp21 = new TH1F("hsigmaphirapp21","hsigmaphirapp21",100,0.9,1.2);
  TH1F* hsigmaphirapp32 = new TH1F("hsigmaphirapp32","hsigmaphirapp32",100,0.9,1.2);
  TH1F* hsigmaphirapp43 = new TH1F("hsigmaphirapp43","hsigmaphirapp43",100,0.9,1.2);
  TH1F* hsigmaphirapp41 = new TH1F("hsigmaphirapp41","hsigmaphirapp41",100,0.9,1.2);
  

  int smin = 0;
  int smax = 0;
  if (granularity=="SL") {
    smin = 1;
    smax = 14;  
  } else if (granularity=="stat"){
    smin = 0;
    smax = 0;
  }


  for (int wheel = -2; wheel<3; ++wheel) {
    for (int station =1; station<=4; ++station) { 
      for (int sector = smin; sector<=smax; ++sector) {

	if (station!=4 && sector>12) continue;

	float vd = 0.00543;
	float vdtheta = 0.00543;
	
	if (isMC && abs(wheel)==2 && station==1){	  
	  vd = 0.00532;
	}

	double sigmaSL1[5];
	double sigmaSL2[5];
	double sigmaSL3[5];
	double sigmaErrSL1[5];
	double sigmaErrSL2[5];
	double sigmaErrSL3[5];
	double rSL2L14;
	double rSL2L23;
	double rtheta;
	double srSL2L1;
	double srSL2L2;
	double srSL2L3;
	double srSL2L4;
	double srSL2L14;
	double srSL2L23;
	double srtheta;
	double rSL3L4SL1L1,rSL3L3SL1L2,rSL3L2SL1L3,rSL3L1SL1L4;
	double rapp21,rapp32,rapp43,rapp41;
	double srSL3L4,srSL1L1,srSL3L4SL1L1,srSL3L3,srSL1L2,srSL3L3SL1L2,srSL3L2,srSL1L3,srSL3L2SL1L3,srSL3L1,srSL1L4,srSL3L1SL1L4;
	double srapp21,srapp32,srapp43,srapp41;
	double stheta14 = 0.;
	double stheta23 = 0.;
	double stheta = 0.;
	double sphi18,sphi27,sphi36,sphi45,sphi;


	HRes1DHits *hResPhi1[5];
	HRes1DHits *hResTheta[5];
	HRes1DHits *hResPhi2[5];


	for (int layer = 1; layer<=4; ++layer) {
	  
	  DTDetId detId1(wheel, station, sector, 1, layer, 0);
	  DTDetId detId2(wheel, station, sector, 2, layer, 0);
	  DTDetId detId3(wheel, station, sector, 3, layer, 0);
	  
	  
	  hResPhi1[layer] = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId1, "Cut1"),file);
	  
	  hResTheta[layer] = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId2, "Cut1"),file);
	  
	  hResPhi2[layer] = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId3, "Cut1"),file);
	  
	}


	TCanvas c;
 
	if (station!=4) {
	  TH1F* tmpTheta14 = (TH1F*) hResTheta[1]->hResPos->Clone("tmpTheta14");
	  tmpTheta14->Add(hResTheta[4]->hResPos);
	  TH1F* tmpTheta23 = (TH1F*) hResTheta[2]->hResPos->Clone("tmpTheta23");
	  tmpTheta23->Add(hResTheta[3]->hResPos);

	  TF1* ftheta14 = drawGFit(tmpTheta14, nsigma, -2. , 2.);
	  TF1* ftheta23 = drawGFit(tmpTheta23, nsigma, -2. , 2. );

	  stheta14 = ftheta14->GetParameter("Sigma")*1.83;
	  stheta23 = ftheta23->GetParameter("Sigma")*1.20;
	  stheta = (stheta14+stheta23)/2.;
	}

	TH1F* tmpPhi18 = (TH1F*) hResPhi1[1]->hResPos->Clone("tmpPhi18");
	tmpPhi18->Add(hResPhi2[4]->hResPos);
	TH1F* tmpPhi27 = (TH1F*) hResPhi1[2]->hResPos->Clone("tmpPhi27");
	tmpPhi27->Add(hResPhi2[3]->hResPos);
	TH1F* tmpPhi36 = (TH1F*) hResPhi1[3]->hResPos->Clone("tmpPhi36");
	tmpPhi36->Add(hResPhi2[2]->hResPos);
	TH1F* tmpPhi45 = (TH1F*) hResPhi1[4]->hResPos->Clone("tmpPhi45");
	tmpPhi45->Add(hResPhi2[1]->hResPos);
	
	TF1* fphi18 = drawGFit(tmpPhi18, nsigma, -2. , 2. );
	TF1* fphi27 = drawGFit(tmpPhi27, nsigma, -2. , 2. );
	TF1* fphi36 = drawGFit(tmpPhi36, nsigma, -2. , 2. );
	TF1* fphi45 = drawGFit(tmpPhi45, nsigma, -2. , 2. );
	
	
	sphi18 = fphi18->GetParameter("Sigma")*1.171;
	sphi27 = fphi27->GetParameter("Sigma")*1.15974;
	sphi36 = fphi36->GetParameter("Sigma")*1.14914;
	sphi45 = fphi45->GetParameter("Sigma")*1.1394;


	sphi = (sphi18+sphi27+sphi36+sphi45)/4.;


	cout 
	  << " " << wheel << " " << station << " " << sector 
	  <<  " sphi18: " << sphi18 <<" sphi27: "<<sphi27<< " sphi36: "<< sphi36<< " sphi45:  "<<sphi45 << endl;
	if (station!=4) {
	  cout  << " stheta14: " << stheta14 << " stheta23: " << stheta23 << " stheta: " << stheta << endl;
	}
	

	int secmin=sector;
	int secmax=sector;
	if (sector ==0) {
	  secmin=1;
	  secmax=14;  
	}
	for (int sec = secmin; sec<=secmax; sec++) {
	  if (station!=4 && sec>12) continue;
//-- Use format of vdrift calibration tables
// 	  writeVDriftTable(f,wheel,station,sec,1, vd, sphi);
// 	  if (station!=4) {writeVDriftTable(f,wheel,station,sec,2, vdtheta, stheta);
// 	  writeVDriftTable(f,wheel,station,sec,3, vd, sphi);


	  f                 << wheel << " " << station << " " << sec << " 1 -1 " << sphi << endl;
	  if (station!=4) f << wheel << " " << station << " " << sec << " 2 -1 " << stheta << endl;
	  f                 << wheel << " " << station << " " << sec << " 3 -1 " << sphi << endl;

	}
      } // sector
    } //station
  } //wheel
}

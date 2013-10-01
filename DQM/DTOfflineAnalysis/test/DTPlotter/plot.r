//----------------------------------------------------------------------
// Run: 
// .x plot.r("file",w,st[,se][,l])
//
// se=0 -> all sectors (for statByView)
// se!=0, l!=0 for chamberByLayer etc.
//
//----------------------------------------------------------------------


void plot(TString filename, int wheel, int station, int sector=0, int layer=0) {
  plot(filename,"Cut1",wheel,station,sector,layer);
}


void plot(TString filename, TString cut, int wheel, int station, int sector, int layer=0) {

   if (! TString(gSystem->GetLibraries()).Contains("DTDetId_cc")) {
     cout << "loading" << endl;
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/Histograms.h");
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/DTDetId.cc+");
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/Utils.cc+");
     gROOT->LoadMacro("macros2.C");
   }


  //----------------------------------------------------------------------
  //  Configurable options

   opt2Dplot = "col"; // Plot options scatter plots
   addProfile = false; // Draw simple profile for 2D plots (red)
   addSlice = true;   // Draw mean of fitted gaussian in slides for 2D plots (blue

  int rbx =1; // rebin x in scatter plots
  int rby =1; // rebin y in scatter plots
  int rbp = 1; // rebin profile

  float nsigma = 2; // interval for the fit of residual distributions
  bool plotDist = true; // true  = use plots for resiudual vs dist 
                        // false = vs pos
  //----------------------------------------------------------------------


 
  TStyle * style = getStyle("tdr");
  style->cd();  
  setPalette();
  //  gStyle->SetOptStat(111); // print also mean value

  float cmToMicron = 10000.;
  float vdrift = 54.3;


  TFile *file = new TFile(filename);

  DTDetId detId1(wheel, station, sector, 1, layer, 0);
  DTDetId detId2(wheel, station, sector, 2, layer, 0);
  DTDetId detId3(wheel, station, sector, 3, layer, 0);
  

  // Hit plots, step 3
  HRes1DHits *hResPhi1 = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId1, cut),file);
  HRes1DHits *hResTheta = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId2, cut),file);
  HRes1DHits *hResPhi2 = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId3, cut),file);
  HRes1DHits *hResPhi = hResPhi1; // for ByView granularity
  // Hit plots step 1
  HRes1DHits *hResPhiS1 = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId1, cut)+"_S1",file);
  HRes1DHits *hResThetaS1 = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId2, cut)+"_S1",file);

  cout << "hResPhi set name:  " << hResPhi->name << endl;
  cout << "hResTheta set name:" << hResTheta->name << endl;

  // Segment plots
  DTDetId chDetId(wheel, station, sector, 0, 0, 0);
  HSegment*   hSegChamberSel = new HSegment(Utils::getHistoNameFromDetIdAndSet(chDetId, cut),file);
  
  TString canvbasename = filename;
  canvbasename = canvbasename.Replace(canvbasename.Length()-5,5,"") + TString("_") + Utils::getHistoNameFromDetIdAndSet(detId2, cut);

  // Select canvases
  bool doPhiAndThetaS3 = true;
  bool doAngularDeps = true;
  bool doPhiThetaVsXY = true;
  bool doNHits = false;

  bool doPhiBySL = false;   // only for "SL" or "ByLayer


  //-------------------- Residuals in phi and theta 
  if (doPhiAndThetaS3) {
    TCanvas* c1= new TCanvas;
    c1->SetTitle(canvbasename+"_PhiTheta");
    c1->Divide(2,2);
    
    c1->cd(1);
    TH1F* hRes;
    if (plotDist) hRes=hResPhi->hResDist;
    else hRes=hResPhi->hResPos;
    TF1* fphi=drawGFit(hRes, nsigma, -0.4, 0.4);

    c1->cd(2);
    plotAndProfileX(hResPhi->hResDistVsDist,rbx,rby,rbp,-.1, .1, 0, 2.1);
    float m_phi = fphi->GetParameter("Mean")*cmToMicron;
    float s_phi = fphi->GetParameter("Sigma")*cmToMicron;

    if (hResTheta->hResDist) {
      c1->cd(3);
      if (plotDist) hRes=hResTheta->hResDist;
      else hRes=hResTheta->hResPos;
      TF1* ftheta=drawGFit(hRes, nsigma, -0.4, 0.4);

      c1->cd(4);  
      plotAndProfileX(hResTheta->hResDistVsDist,rbx,rby,rbp,-.1, .1, 0, 2.1);
      float m_theta = ftheta->GetParameter("Mean")*cmToMicron;
      float s_theta = ftheta->GetParameter("Sigma")*cmToMicron;  
    }

    cout << canvbasename << "  Step3"
	 << detId1 << endl
	 << "                 Phi: M= " << int(floor(m_phi+0.5))
	 << " S= "      << int(s_phi+0.5)
	 << "; Theta: M= " << int(floor(m_theta+0.5))
	 << " S= "  << int(s_theta+0.5) << endl;
  }


  //-------------------- Angular dependencies
  if (doAngularDeps) {
    TCanvas* c1= new TCanvas;
    c1->SetName(canvbasename+" MeanVsAngles");
    c1->SetTitle(canvbasename+" Angles");

    rbx=1;
    rby=1;

    c1->Divide(2,2);
    c1->cd(1);
    hSegChamberSel->hPhiLoc->GetXaxis()->SetRangeUser(-1.,1.);
    hSegChamberSel->hPhiLoc->Draw();

    c1->cd(2);
    plotAndProfileX(hResPhi->hResDistVsAngle,rbx,rby,1,-.04, .04, -0.5, 0.5);

    c1->cd(3);
    if (hSegChamberSel->hThetaLoc){
      hSegChamberSel->hThetaLoc->Draw();
    }
    
    c1->cd(4);
    if (hResTheta->hResDistVsAngle){
      plotAndProfileX(hResTheta->hResDistVsAngle,rbx,rby,1,-.04, .04, -1, 1);
    }

  }


  //-------------------- Phi/theta vs X and Y
  if (doPhiThetaVsXY) {
    TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename+"_PhiThetavsXY");
    c2->Divide(2,2);

    c2->cd(1);
    plotAndProfileX(hResPhi->hResDistVsX,  2,rby,2,-.04, .04, -130,130);

    c2->cd(2);  
    plotAndProfileX(hResPhi->hResDistVsY,  2,rby,2,-.04, .04, -130,130);

    c2->cd(3);  
    plotAndProfileX(hResTheta->hResDistVsX,  2,rby,2,-.04, .04, -130,130);

    c2->cd(4);  
    plotAndProfileX(hResTheta->hResDistVsY,  2,rby,2,-.04, .04, -130,130);

  }


    //-------------------- nHits, chi2
  if (doNHits) { 
       TCanvas* c1= new TCanvas;
    c1->SetTitle(canvbasename+"_NHitsT0");
    c1->Divide(2,2);
    c1->cd(1);
    
    TH2F * hNh = hSegChamberSel->hNHits;
    hNh->SetXTitle("#phi hits");
    hNh->SetYTitle("#theta hits");
    hNh->Draw("BOX");

    c1->cd(2);
    hNh->ProjectionY()->Draw();

    c1->cd(3);
    hNh->ProjectionX()->Draw();


    c1->cd(4);
    hSegChamberSel->hChi2->Draw();
    gPad->Update();
    TPaveStats *st = (TPaveStats*)hSegChamberSel->hChi2->FindObject("stats");
    st->SetOptStat(111);
    st->Draw();
  }



  // Phi residuals divided by SL (only with SL or ByLayer granularity)
  if (doPhiBySL) {
    TCanvas* c2= new TCanvas;
    c2->SetName(canvbasename+"_Phi1Phi2");
    c2->SetTitle(canvbasename+"_Phi1Phi2");
    c2->Divide(2,2);

    c2->cd(1);
    TF1* fphi1=drawGFit(hResPhi1->hResDist, nsigma, -0.4, 0.4);

    c2->cd(2);  
    plotAndProfileX(hResPhi1->hResDistVsDist,  rbx,rby,rbp,-.1, .1, 0, 2.1);

    c2->cd(3);  
    TF1* fphi2=drawGFit(hResPhi2->hResDist, nsigma, -0.4, 0.4);

    c2->cd(4);  
    plotAndProfileX(hResPhi2->hResDistVsDist,  rbx,rby,rbp,-.1, .1, 0, 2.1);

    m_phi1 = fphi1->GetParameter("Mean")*cmToMicron;
    s_phi1 = fphi1->GetParameter("Sigma")*cmToMicron;
    m_phi2 = fphi2->GetParameter("Mean")*cmToMicron;
    s_phi2 = fphi2->GetParameter("Sigma")*cmToMicron;
    
    cout << canvbasename
	 << " Phi1: M= " << int(floor(m_phi1+0.5)) << " s= " << int(floor(s_phi1+0.5))
	 << " Phi2: M= " << int(floor(m_phi2+0.5)) << " s= " << int(floor(s_phi2+0.5))
	 << " delta=" << int(floor(m_phi2-m_phi1+0.5)) << endl;

  }


  
}


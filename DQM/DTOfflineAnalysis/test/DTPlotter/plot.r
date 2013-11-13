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


void plot(TString filename, TString cut, int wheel, int station, int sector=0, int layer=0) {

   if (! TString(gSystem->GetLibraries()).Contains("DTDetId_cc")) {
     cout << "loading" << endl;
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/Histograms.h");
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/DTDetId.cc+");
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/Utils.cc+");
     gROOT->LoadMacro("macros2.C");
   }


  //----------------------------------------------------------------------
  //  Configurable options

   opt2Dplot = "col";  // Plot options for scatter plots
   addProfile = false; // Draw simple profile for 2D plots (red)
   addSlice = true;    // Draw mean of fitted gaussian in slides for 2D plots (blue)
   addMedian = false;   // Draw meadian profile of 2D plots (red)

  int rbx =1; // rebin x in scatter plots
  int rby =1; // rebin y in scatter plots
  int rbp = 1; // rebin profile

  float nsigma = 2; // interval for the fit of residual distributions
  bool plotDist = true; // true  = use plots for resiudual vs dist 
                        // false = vs pos
  //----------------------------------------------------------------------


 
  TStyle * style = getStyle("tdr");
  style->cd();
  gStyle->SetTitleSize(0.05,"XYZ"); // Set larger axis titles
  gStyle->SetTitleOffset(1.3,"Y");
  gStyle->SetOptTitle(0); // remove histogram titles

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

  cout << "hResPhi set name:  " << hResPhi->name << " " << hResPhi << endl;
  cout << "hResTheta set name:" << hResTheta->name << " " << hResTheta << endl;

  // Segment plots
  DTDetId chDetId(wheel, station, sector, 0, 0, 0);
  HSegment*   hSegChamberSel = new HSegment(Utils::getHistoNameFromDetIdAndSet(chDetId, cut),file);
  
  TString canvbasename = filename;
  
  canvbasename = canvbasename.Replace(canvbasename.Length()-5,5,"") + TString("_") + Utils::getHistoNameFromDetIdAndSet(DTDetId(wheel,station,sector,0,layer,0), cut);

  // Select canvases
  bool doPhiAndThetaS3 = true;
  bool doAngularDeps = true;
  bool doPhiThetaVsXY = true;
  bool doPhiThetaVsXYS1 = false;
  bool doNHits = true;
  bool doVd = true;

  // Special plots
  bool doPhiBySL = false; // only for "SL" or "ByLayer
  bool doResVsCell = false; // makes sense only for "SL" or "ByLayer

  bool debugProfile=false;


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

    c1->Divide(2,2,0.0005,0.0005);
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
    c2->Divide(2,2,0.0005,0.0005);

    c2->cd(1);
    plotAndProfileX(hResPhi->hResDistVsX,  1,rby,1,-.04, .04, -130,130);

    c2->cd(2);  
    plotAndProfileX(hResPhi->hResDistVsY,  1,rby,1,-.04, .04, -130,130);

    c2->cd(3);  
    plotAndProfileX(hResTheta->hResDistVsX, 1,rby,1,-.04, .04, -130,130);

    c2->cd(4);  
    plotAndProfileX(hResTheta->hResDistVsY,  1,rby,1,-.04, .04, -130,130);

  }

  //-------------------- Phi/theta vs X and Y @ S1
  if (doPhiThetaVsXYS1 && hResPhiS1->hResDistVsX) {
    TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename+"_PhiThetavsXY_S1");
    c2->Divide(2,2,0.0005,0.0005);

    c2->cd(1);
    plotAndProfileX(hResPhiS1->hResDistVsX,  1,rby,1,-.04, .04, -130,130);

    c2->cd(2);  
    plotAndProfileX(hResPhiS1->hResDistVsY,  1,rby,1,-.04, .04, -130,130);

    c2->cd(3);  
    plotAndProfileX(hResThetaS1->hResDistVsX,  1,rby,1,-.04, .04, -130,130);

    c2->cd(4);  
    plotAndProfileX(hResThetaS1->hResDistVsY,  1,rby,1,-.04, .04, -130,130);

  }

    //-------------------- nHits, chi2
  if (doNHits) { 
       TCanvas* c1= new TCanvas;
    c1->SetTitle(canvbasename+"_NHitsT0");
    c1->Divide(2,2,0.0005,0.0005);
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



  //-------------------- Phi residuals divided by SL (only with SL or ByLayer granularity)
  if (doPhiBySL) {
    TCanvas* c2= new TCanvas;
    c2->SetName(canvbasename+"_Phi1Phi2");
    c2->SetTitle(canvbasename+"_Phi1Phi2");
    c2->Divide(2,2,0.0005,0.0005);

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

  
  //-------------------- Residuals by cell#
  // used to debug periodic modulation of residual vs X
  // (makes sense only with SL or ByLayer granularity; produced detail=2)
  if (doResVsCell) {
        TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename+"_resVsCell");
    c2->Divide(2,2,0.0005,0.0005);

    c2->cd(1);
    plotAndProfileX(hResPhi->hResDistVsCell,  1,1,1,-.04,.04, 1,60);

    c2->cd(3);  
    plotAndProfileX(hResTheta->hResDistVsCell,  1,1,1,-.04,.04, 0,60);

  }
  

  //-------------------- Example to inspect slices of profile histograms
  if(debugProfile) {
    float xvalues[5] = {-0.7, -0.65, -0.6, -0.5, -0.4};
    TH2F* h = hResTheta->hResDistVsAngle;
    //    h->Rebin2D(2,1);

    TH2F* hhh=h->Clone();
    TCanvas* c1= new TCanvas;
    c1->SetTitle(canvbasename+"_test");
    c1->Divide(3,2);
    c1->cd(1);
    plotAndProfileX(hhh,1,1,1,-0.04,0.04);

    for (int i=0; i<5; ++i){
      TLine * l = new TLine(xvalues[i],-0.1,xvalues[i],0.1);
      l->SetLineColor(kRed);
      l->Draw();
    }

    double xq[1] = {0.5};    
    for (int i=0; i<5; ++i){
      c1->cd(i+2);
      int bin=hhh->GetXaxis()->FindBin(xvalues[i]);
      TString name=Form("x=%f",xvalues[i]);
      TH1D * proj = h->ProjectionY(name ,bin, bin);
      proj->SetTitle(name);
      proj->Draw();      
      proj->Fit("gaus","q");
      proj->GetXaxis()->SetRangeUser(-0.1,0.1);

      double median[1];
      proj->GetQuantiles(1,median,xq);
      double m1=median[0];
      int nbins = proj->GetNbinsX();
      proj->SetBinContent(1, proj->GetBinContent(0)+proj->GetBinContent(1));
      proj->SetBinContent(nbins, proj->GetBinContent(nbins)+proj->GetBinContent(nbins+1));
      proj->GetQuantiles(1,median,xq);
      cout << name << " "  << m1 << " " << median[0] << endl;


    }
  }
  

  //-------------------- plot vdrift vs x/y
  if (doVd) {
    TCanvas* c1= new TCanvas;
    c1->SetTitle(canvbasename+"_vdrift");
    c1->Divide(2,2);

    if (hSegChamberSel->hVDrift->GetEntries() != 0){
      c1->cd(1);
      plotAndProfileX(hSegChamberSel->hVDriftVsX,2,1,1,0.0052, 0.0056, -130., 130.);

      c1->cd(2);
      plotAndProfileX(hSegChamberSel->hVDriftVsY,2,1,1,0.0052, 0.0056, -130., 130.);
      hSegChamberSel->hVDriftVsY->GetXaxis()->SetTitle("Local Y (cm)");
      hSegChamberSel->hVDriftVsY->GetYaxis()->SetTitle("v_{drift} (cm/ns)");
    }


    c1->cd(3);
    TF1* fDvd=drawGFit(hSegChamberSel->hVDrift, 1.2, 0, 1);

//     hSegChamberSel->hFailVdAngle->SetXTitle("#alpha of segments with no vdrift (rad)");
//     hSegChamberSel->hFailVdAngle->Draw();

    c1->cd(4);
    //    plotAndProfileX(hSegChamberSel->hVDriftVsPhi,1,1,1,0.0052, 0.0056, -.5, .5);
    
    plotAndProfileX(hSegChamberSel->hdVDriftVsY,2,1,1,-0.03,0.03, -130., 130.);

  }




}

//------------------------------
//
// .x plot.r("file",w,st,se[,l])
//
// l=0 (default for statByView, chamberByView
// se=0 for statByView
//
//------------------------------


void plotValidation(TString filename, int wheel, int station, int sector, int layer=0) {
  plot(filename,"Cut1",wheel,station,sector,layer);
}


void plot(TString filename, TString cut, int wheel, int station, int sector, int layer=0) {

   if (! TString(gSystem->GetLibraries()).Contains("DTDetId_cc")) {
     cout << "loading" << endl;
     gROOT->LoadMacro("$CMSSW_BASE/src/Validation/DTRecHits/test/Histograms.h");
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/DTDetId.cc+");
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/Utils.cc+");
     gROOT->LoadMacro("macros2.C");
   }


  //----------------------------------------------------------------------
  //  Configurable options

   opt2Dplot = "col"; // color scatter plots
   //   opt2Dplot = "box";
   addProfile = false;
   addSlice = true;

  int rbx =1; // rebin x in scatter plots
  int rby =1; // rebin y in scatter plots
  int rbp = 2; // rebin profile

  float nsigma = 2; // interval for the fit of residual distributions
  bool plotDist = true; // true: use resiudual vs dist 
                        // false = vs pos

  //----------------------------------------------------------------------


 
  TStyle * style = getStyle("tdr");
  style->cd();  
  gStyle->SetPalette(5);
  //  gStyle->SetOptStat(111);

  float cmToMicron = 10000.;
  float vdrift = 54.3;


  TFile *file = new TFile(filename);

  DTDetId detId1(wheel, station, sector, 1, layer, 0);
  DTDetId detId2(wheel, station, sector, 2, layer, 0);
  DTDetId detId3(wheel, station, sector, 3, layer, 0);
  
//   HRes1DHit *hResPhi1 = new HRes1DHit("S3RPhi",file);
//   HRes1DHit *hResTheta = new HRes1DHit("S3RZ_W2",file);
  HRes1DHit *hResPhi1  = new HRes1DHit(Utils::getDTValidationHistoNameFromDetId(detId1,"S3"),file);
  HRes1DHit *hResTheta = new HRes1DHit(Utils::getDTValidationHistoNameFromDetId(detId2,"S3"),file);
//   HRes1DHits *hResPhi2 = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId3, cut),file);
  HRes1DHit *hResPhi = hResPhi1; // for ByView granularity
//   HRes1DHits *hResPhiS1 = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId1, cut)+"_S1",file);
//   HRes1DHits *hResThetaS1 = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId2, cut)+"_S1",file);


  HEff1DHit* hEffS1RPhi= new HEff1DHit(Utils::getDTValidationHistoNameFromDetId(detId1,"S1"),file);
  HEff1DHit* hEffS3RPhi= new HEff1DHit(Utils::getDTValidationHistoNameFromDetId(detId1,"S3"),file);
  HEff1DHit* hEffS1RZ=0;
  HEff1DHit* hEffS3RZ=0;
  if (station!=4) {
    hEffS1RZ=   new HEff1DHit(Utils::getDTValidationHistoNameFromDetId(detId2,"S1"),file);
    hEffS3RZ=   new HEff1DHit(Utils::getDTValidationHistoNameFromDetId(detId2,"S3"),file);
  }
  
  DTDetId chDetId(wheel, station, sector, 0, 0, 0);

  TString chName = Utils::getDTValidationHistoNameFromDetId(chDetId,"");
  cout << chName << endl;

  HRes4DHit* hRes4D= new HRes4DHit(chName, file);
  //  cout << (long) hRes4D->hResAlpha << endl;
  


  // Result of fits
  float m_phi = 0.;
  float s_phi = 0.;
  float m_theta = 0.;
  float s_theta = 0.;
  float m_phi1 = 0.;
  float s_phi1 = 0.;
  float m_phi2 = 0.;
  float s_phi2 = 0.;
  float m_phiS1 = 0.;
  float s_phiS1 = 0.;
  float m_phiS2 = 0.;
  float s_phiS2 = 0.;
  float m_thetaS1 = 0.;
  float s_thetaS1 = 0.;
  float m_thetaS2 = 0.;
  float s_thetaS2 = 0.;
  float t0phi   =0.;
  float t0theta =0.;

  
  TString canvbasename = filename;
  canvbasename = canvbasename.Replace(canvbasename.Length()-5,5,"") + TString("_") + Utils::getDTValidationHistoNameFromDetId(chDetId, "");
  cout << "Canvas basename is: " << canvbasename << endl;

  // byView
  bool doPhiAndThetaS3 =true;
  bool doHitPull = true;
  bool doEff = false;
  bool doT0= false;
  bool doSegRes=false;

  bool doPhiAndThetaS1 = false;
  bool doPhiBySL = false;
  bool doPhiBySLS1AndS3 = false;
  bool doPhiThetaVsXY = false;
  bool doPhiThetaS1VsXY = false;

  // bySL
//   bool doPhiAndThetaS3 = false;
//   bool doPhiAndThetaS1 = false;
//   bool doPhiBySL = true;
//   bool doPhiBySLS1AndS3 = false;
//   bool doPhiThetaVsXY = false;
//   bool doPhiThetaS1VsXY = false;

  // Residuals in phi (SL1) and theta 
  if (doPhiAndThetaS3) {
    TCanvas* c1= new TCanvas;
    c1->SetTitle(canvbasename+"_ResPhiTheta");
    c1->Divide(2,2);
    
    c1->cd(1);

    TH1F* hRes;
    hRes=hResPhi->hRes;

    hResPhi->hRes->Rebin(2);
    TF1* fphi=drawGFit(hRes, nsigma, -0.4, 0.4);

    c1->cd(2);

    plotAndProfileX(hResPhi->hResVsPos,rbx,rby,rbp,-.1, .1, 0, 2.1);


    m_phi = fphi->GetParameter("Mean")*cmToMicron;
    s_phi = fphi->GetParameter("Sigma")*cmToMicron;

    if (hResTheta->hRes) {

      c1->cd(3);
      hRes=hResTheta->hRes;

      hResTheta->hRes->Rebin(2);
      TF1* ftheta=drawGFit(hRes, nsigma, -0.4, 0.4);

      c1->cd(4);  
      plotAndProfileX(hResTheta->hResVsPos,rbx,rby,rbp,-.1, .1, 0, 2.1);  
    
      m_theta = ftheta->GetParameter("Mean")*cmToMicron;
      s_theta = ftheta->GetParameter("Sigma")*cmToMicron;  
    }
    

    cout << canvbasename << "  Step3"
	 << detId1 << endl
	 << "                 Phi: M= " << int(floor(m_phi+0.5))
	 << " S= "      << int(s_phi+0.5)
	 << "; Theta: M= " << int(floor(m_theta+0.5))
	 << " S= "  << int(s_theta+0.5) << endl;
  }

  if (doHitPull){
    TCanvas* c1= new TCanvas;
    c1->SetTitle(canvbasename+"_PullPhiTheta");
    c1->Divide(2,2);
    
    c1->cd(1);

    TH1F* hPull;
    hPull=hResPhi->hPull;

    //    hResPhi->hPull->Rebin(2);
    TF1* fphi=drawGFit(hPull, nsigma, -5, 5);

    c1->cd(2);

    plotAndProfileX(hResPhi->hPullVsPos,rbx,rby,rbp,-5, 5, 0, 2.1);


    m_phi = fphi->GetParameter("Mean")*cmToMicron;
    s_phi = fphi->GetParameter("Sigma")*cmToMicron;

    if (hResTheta->hPull) {

      c1->cd(3);
      hPull=hResTheta->hPull;

      //      hResTheta->hPull->Rebin(2);
      TF1* ftheta=drawGFit(hPull, nsigma, -5, 5);

      c1->cd(4);  
      plotAndProfileX(hResTheta->hPullVsPos,rbx,rby,rbp,-5, 5, 0, 2.1);  
    
      m_theta = ftheta->GetParameter("Mean")*cmToMicron;
      s_theta = ftheta->GetParameter("Sigma")*cmToMicron;  
    }
    

    cout << canvbasename << "  Step3"
	 << detId1 << endl
	 << "                 Phi: M= " << int(floor(m_phi+0.5))
	 << " S= "      << int(s_phi+0.5)
	 << "; Theta: M= " << int(floor(m_theta+0.5))
	 << " S= "  << int(s_theta+0.5) << endl;
  }


  if (doEff) {
    TCanvas* c1= new TCanvas;
    c1->SetTitle(canvbasename+"_EffPhiTheta");
    c1->Divide(2,2);
    c1->cd(1);
    plotEff(hEffS1RPhi->hEffVsDist, hEffS3RPhi->hEffVsDist);
    c1->cd(3);
    if (station!=4) plotEff(hEffS1RZ->hEffVsDist, hEffS3RZ->hEffVsDist);
//     c1->cd(2);
//     //plotEff(hEffS1RPhi->hEffVsPhi, hEffS3RPhi->hEffVsPhi);
//     plotEff(hEffS1RPhi->hEffVsEta, hEffS3RPhi->hEffVsEta);
//     c1->cd(4);
//     //    if (station!=4) plotEff(hEffS1RZ->hEffVsPhi, hEffS3RZ->hEffVsPhi);
//     if (station!=4) plotEff(hEffS1RZ->hEffVsEta, hEffS3RZ->hEffVsEta);

  }

  if (doT0) {
    TCanvas* c1= new TCanvas;
    c1->SetTitle(canvbasename+"_NHitsT0");
    c1->Divide(2,2);
    c1->cd(1);
    
    TH2F * hNh = (TH2F *) file->Get("DQMData/Run 1/DT/Run summary/4DSegments/4D_"+chName+"_hNHits");
    hNh->SetXTitle("#phi hits");
    hNh->SetYTitle("#theta hits");
    hNh->Draw("BOX");
    c1->cd(2);
    hNh->ProjectionY()->Draw();
    c1->cd(3);
    hNh->ProjectionX()->Draw();
    c1->cd(4);
    TH2F * ht0 = (TH2F *) file->Get("DQMData/Run 1/DT/Run summary/4DSegments/4D_"+chName+"_ht0");
    ht0->SetXTitle("t0 #phi");
    ht0->SetYTitle("t0 #theta");
    ht0->Draw("BOX");


  }

  if (doSegRes){
    TCanvas* c1= new TCanvas;
    c1->SetTitle(canvbasename+"_ResSeg");
    c1->Divide(2,2);
    c1->cd(1);
    //    hRes4D->hResX->Rebin(2);
    drawGFit(hRes4D->hResX, nsigma, -0.1, 0.1);
    c1->cd(2);
    //    hRes4D->hResAlpha->Rebin(2);
    drawGFit(hRes4D->hResAlpha, nsigma, -0.01, 0.01);
    c1->cd(3);
    hRes4D->hResYRZ->Rebin(2);
    drawGFit(hRes4D->hResYRZ, nsigma, -0.4, 0.4);
    c1->cd(4);
    hRes4D->hResBeta->Rebin(2);
    drawGFit(hRes4D->hResBeta, nsigma, -0.4, 0.4);
    
  }
  

  

    
  

  // Stuff beyond here does not apply to validation (right now)
  //----------------------------------------------------------------------

  // Residuals in phi (SL1) and theta for Step1
  if (doPhiAndThetaS1) {
    TCanvas* c1= new TCanvas;
    c1->SetName(canvbasename+"_PhiThetaS1");
    c1->SetTitle(canvbasename+"_PhiThetaS1");
    c1->Divide(2,2);
    
    c1->cd(1);

    TH1F* hRes;
    if (plotDist) hRes=hResPhiS1->hResDist;
    else hRes=hResPhiS1->hResPos;


    hResPhiS1->hResDist->Rebin(2);
    TF1* fphi=drawGFit(hRes, nsigma, -0.4, 0.4);

    c1->cd(2);
    plotAndProfileX(hResPhiS1->hResDistVsDist,rbx,rby,rbp,-.1, .1, 0, 2.1);


    m_phi = fphi->GetParameter("Mean")*cmToMicron;
    s_phi = fphi->GetParameter("Sigma")*cmToMicron;

    if (hResThetaS1->hResDist) {

      c1->cd(3);
      if (plotDist) hRes=hResThetaS1->hResDist;
      else hRes=hResThetaS1->hResPos;

      hResThetaS1->hResDist->Rebin(2);
      TF1* ftheta=drawGFit(hRes, nsigma, -0.4, 0.4);

      c1->cd(4);  
      plotAndProfileX(hResThetaS1->hResDistVsDist,rbx,rby,rbp,-.1, .1, 0, 2.1);  
    
      m_theta = ftheta->GetParameter("Mean")*cmToMicron;
      s_theta = ftheta->GetParameter("Sigma")*cmToMicron;  
    }
    

    cout << canvbasename << "  Step1"
      	 << detId1 << endl
	 << "                 Phi: M= " << int(floor(m_phi+0.5))
	 << " S= "      << int(s_phi+0.5)
	 << "; Theta: M= " << int(floor(m_theta+0.5))
	 << " S= "  << int(s_theta+0.5) << endl;
  }

  

  //--- t0seg phi, vdrift
  if (false) {    
    TCanvas* c1= new TCanvas;
    c1->SetName(canvbasename+" t0 - vdrift");
    c1->SetTitle(canvbasename+" t0 - vdrift");
    c1->Divide(2,2);
    c1->cd(1);
    //    hSegChamberSel->ht0Phi->Rebin(2);
    TF1* ft0phi=drawGFit(hSegChamberSel->ht0Phi, 1, -40, 40);

    if (hSegChamberSel->ht0Theta) {  
      c1->cd(2);
      //      hSegChamberSel->ht0Theta->Rebin(2);
      TF1* ft0phi=drawGFit(hSegChamberSel->ht0Theta, 1.5, -40, 40);
    }


    if (hSegChamberSel->hVDrift->GetEntries() != 0){
    
      c1->cd(3);
    //    c1->SetTitle(canvbasename+"_DeltaVd");
      hSegChamberSel->hVDrift->Rebin(2);
      TF1* fDvd=drawGFit(hSegChamberSel->hVDrift, 1.5, -0.1, 0.1);

      c1->cd(4);
      plotAndProfileX(hSegChamberSel->hVDriftVsPhi,rbx,rby,1,-.1, .1, -.5, .5);
    }
  }  

  //  return;

  // plot vdrift vs y
  // FIXME: shall we implement a more refined fit?
  if (false) {
    TCanvas* c1= new TCanvas;
    c1->SetTitle(canvbasename+" vdrift");
    c1->Divide(1,2);

    if (hSegChamberSel->hVDrift->GetEntries() != 0){
      c1->cd(1);
      plotAndProfileX(hSegChamberSel->hVDriftVsX,4,2,1,0.0047, 0.005948, -150., 150., false);
      c1->cd(2);
      plotAndProfileX(hSegChamberSel->hVDriftVsY,4,4,1,0.0047, 0.005948, -100., 100., false);

    }
  }

  bool talk = false; // FIXME: What's this crap??
  if (talk) {
    TCanvas* c1= new TCanvas;
    c1->SetTitle(canvbasename+" vdrift (TALK)");
    plotAndProfileX(hSegChamberSel->hVDriftVsY,4,4,1,0.0047, 0.005948, -100., 100., false);
    hSegChamberSel->hVDriftVsY->GetXaxis()->SetTitle("Local Y (cm)");
    hSegChamberSel->hVDriftVsY->GetYaxis()->SetTitle("v_{drift} (cm/ns)");

  }

  

  // t0seg
  if (false) {
    
    TCanvas* c1= new TCanvas;
    c1->SetTitle(canvbasename+"_t0");
    c1->Divide(2,2);

    c1->cd(1);
    TF1* ft0phi=drawGFit(hSegChamberSel->ht0Phi, 1., -40, 40);

    c1->cd(2);
    plotAndProfileX(hSegChamberSel->ht0PhiVsPhi,rbx,rby,1,-10, 10, -0.5, 0.5);

    c1->cd(3);
    TF1* ft0theta=drawGFit(hSegChamberSel->ht0Theta, 1.5, -40, 40);

    t0phi = ft0phi->GetParameter("Mean");
    t0theta = ft0theta->GetParameter("Mean");

//     c1->cd(4);
//     hSegChamberSel->ht0thetaVsPhi->Draw();


  }


  //--- Angular dependencies
  if (false) {
    TCanvas* c1= new TCanvas;
    c1->SetName(canvbasename+" MeanVsAngles");
    c1->SetTitle(canvbasename+" Angles");

    c1->Divide(3,2);
    c1->cd(1);
    hSegChamberSel->hPhiLoc->GetXaxis()->SetRangeUser(-1.,1.);
    hSegChamberSel->hPhiLoc->Draw();

    c1->cd(2);
    plotAndProfileX(hResPhi->hResDistVsAngle,rbx,rby,1,-.1, .1, -0.5, 0.5);


    c1->cd(3);
    plotAndProfileX(hSegChamberSel->ht0PhiVsPhi,rbx,rby,1,-10, 10, -0.5, 0.5);


    c1->cd(4);
    if (hSegChamberSel->hThetaLoc){
      //    hSegChamberSel->hThetaLoc->GetXaxis()->SetRangeUser(-1.,1.);
      hSegChamberSel->hThetaLoc->Draw();
    }
    
    c1->cd(5);
    if (hResTheta->hResDistVsAngle){
      plotAndProfileX(hResTheta->hResDistVsAngle,rbx,rby,1,-.1, .1, -1, 1);
    }
    

    c1->cd(6);
    hSegChamberSel->hChi2->Draw();
    gPad->Update();
    TPaveStats *st = (TPaveStats*)hSegChamberSel->hChi2->FindObject("stats");
    st->SetOptStat(111);
    //    gPad->Update();
  }


  //--- Angular dependencies
  if (false) {
    TCanvas* c1= new TCanvas;
    c1->SetName(canvbasename+" SigmaVsAngles");
    c1->SetTitle(canvbasename+" SigmaVsAngles");

    c1->Divide(2,2);
    c1->cd(1);
    hSegChamberSel->hPhiLoc->GetXaxis()->SetRangeUser(-1.,1.);
    hSegChamberSel->hPhiLoc->Draw();

//     c1->cd(2);
//     plotAndProfileX(hResPhi->hResDistVsAngle,rbx,rby,1,-.1, .1, -0.5, 0.5);

    double minYSigma = 0.017;
    double maxYSigma = 0.026;

    double minXSigma = -0.3;
    double maxXSigma = 0.3;

    if(detId2.wheel == 0) {
      minXSigma = -0.3;
      maxXSigma = 0.3;
    } else if(abs(detId2.wheel) == 1) {
      minXSigma = -0.75;
      maxXSigma = -0.3;
    } else if(abs(detId2.wheel) == 2) {
      minXSigma = -1.05;
      maxXSigma = -0.75;
    }

    c1->cd(2);
    // SIGMA Phi vs phi
    //    plotAndProfileX(hSegChamberSel->ht0PhiVsPhi,rbx,rby,1,-10, 10, -0.5, 0.5);
    TH1F *ht = plotAndProfileSigmaX(hResPhi->hResDistVsAngle,rbx,rby,1,0.02, 0.032, -0.5, 0.5);
    ht->GetXaxis()->SetTitle("Angle in #phi view (rad)");
    ht->GetYaxis()->SetTitle("#sigma_{x} (cm)");


    c1->cd(3);
    if (hSegChamberSel->hThetaLoc){
      //    hSegChamberSel->hThetaLoc->GetXaxis()->SetRangeUser(-1.,1.);
      hSegChamberSel->hThetaLoc->Draw();
    }
    
    c1->cd(4);
    if (hResTheta->hResDistVsAngle){
      // mean phi vs theta
      TH1F *htTheta = plotAndProfileSigmaX(hResPhi->hResDistVsTheta,rbx,rby,1,minYSigma, maxYSigma, minXSigma, maxXSigma);
      htTheta->GetXaxis()->SetTitle("Angle in #theta view (rad)");
      htTheta->GetYaxis()->SetTitle("#sigma_{x} (cm)");
      if(talk) {
	TFile temp("temp.root","UPDATE");
	temp.cd();
	htTheta->Write();
	temp.Close();
      }
    }
    

    c1->cd(6);
    // sigma phi vs theta
    //    gPad->Update();
  }




  // To test computation of ttrig
  if (false) {
    TCanvas* c1= new TCanvas;
    c1->SetTitle(canvbasename+"_PhiTheta");
    c1->Divide(2,2);
    
    c1->cd(1);
    hResPhi->hResDist->Rebin(1);
    TF1* fphi=drawGFit(hResPhi->hResDist, nsigma, -0.4, 0.4);

    c1->cd(2);
    plotAndProfileX(hResPhi->hResDistVsDist,rbx,rby,rbp,-.1, .1, 0, 2.1);

    c1->cd(3);  
    hResTheta->hResDist->Rebin(1);
    TF1* ftheta=drawGFit(hResTheta->hResDist, nsigma, -0.4, 0.4);

    c1->cd(4);  
    plotAndProfileX(hResTheta->hResDistVsDist,rbx,rby,rbp,-.1, .1, 0, 2.1);

    cout << filename
	 << " Phi: M= " << int(fphi->GetParameter("Mean")*cmToMicron)
	 << " S= "  << int(fphi->GetParameter("Sigma")*cmToMicron)
	 << "; Theta: M= " << int(ftheta->GetParameter("Mean")*cmToMicron) 
	 << " S= "  << int(ftheta->GetParameter("Sigma")*cmToMicron) <<endl;
    
    cout << " phi off "  <<  int(fphi->GetParameter("Mean")*cmToMicron)/vdrift
	 << " theta off "  <<  int(ftheta->GetParameter("Mean")*cmToMicron)/vdrift
	 << endl;
  }
  

  // Phi binned by angle
  if (false) {
    TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename+"_PhiByAngle");
    c2->Divide(2,3);

    c2->cd(1);
    TF1* fphi0_15=draw2GFit(hResPhi0_15->hResDist, nsigma, -0.4, 0.4);

    c2->cd(2);
    plotAndProfileX(hResPhi0_15->hResDistVsDist,  rbx,rby,rbp,-.1, .1, 0, 2.1);

    c2->cd(3);  
    TF1* fphi15_30=draw2GFit(hResPhi15_30->hResDist, nsigma, -0.4, 0.4);

    c2->cd(4);  
    plotAndProfileX(hResPhi15_30->hResDistVsDist,  rbx,rby,rbp,-.1, .1, 0, 2.1);

    c2->cd(5);  
    TF1* fphi30=draw2GFit(hResPhi30->hResDist, nsigma, -0.4, 0.4);

    c2->cd(6);  
    plotAndProfileX(hResPhi30->hResDistVsDist,  rbx,rby,rbp,-.1, .1, 0, 2.1);


  }

  

  // Phi divided by SL
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

  
  // 2D segment
  if (false) {
    TCanvas* c1= new TCanvas;
    c1->SetTitle(canvbasename+"_PhiTheta2D");
    c1->Divide(2,2);

    c1->cd(1);
    TF1* fphi=draw2GFit(hRes2DPhi->hResDist, nsigma, -0.4, 0.4);

    c1->cd(2);
    plotAndProfileX(hRes2DPhi->hResDistVsDist, rbx,rby,rbp, -.1, .1, 0, 2.1);

     c1->cd(3);  
     TF1* ftheta=draw2GFit(hRes2DTheta->hResDist, nsigma, -0.4, 0.4);

     c1->cd(4);  
     plotAndProfileX(hRes2DTheta->hResDistVsDist, rbx,rby,rbp,-.1, .1, 0, 2.1);
  }


  // 2D segment, phi divided by SL
  if (false) {
    TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename+"_Phi1Ph2_2D");
    c2->Divide(2,2);

    c2->cd(1);
    TF1* fphi1=draw2GFit(hRes2DPhi1->hResDist, nsigma, -0.4, 0.4);

    c2->cd(2);  
    plotAndProfileX(hRes2DPhi1->hResDistVsDist,  rbx,rby,rbp,-.1, .1, 0, 2.1);

    c2->cd(3);  
    TF1* fphi2=draw2GFit(hRes2DPhi2->hResDist, nsigma, -0.4, 0.4);

    c2->cd(4);  
    plotAndProfileX(hRes2DPhi2->hResDistVsDist,  rbx,rby,rbp,-.1, .1, 0, 2.1);

    cout << canvbasename
	 << " 2D Phi1: M= " << int(fphi1->GetParameter("Mean")*cmToMicron) 
	 << " Phi2: M= " << int(fphi2->GetParameter("Mean")*cmToMicron) 
	 << " delta=" << int((fphi2->GetParameter("Mean") - fphi1->GetParameter("Mean"))*cmToMicron) << endl;

  }

  // Phi, Step 1 and Step 2
  if (doPhiBySLS1AndS3) {
    TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename+"_PhiS1S2");
    c2->Divide(2,2);

    c2->cd(1);
    TF1* fphiS1=draw2GFit(hResPhiS1->hResDist, nsigma, -0.4, 0.4);

    c2->cd(2);  
    plotAndProfileX(hResPhiS1->hResDistVsDist,  rbx,rby,rbp,-.1, .1, 0, 2.1);

    c2->cd(3);  
    TF1* fphiS2=draw2GFit(hResPhiS2->hResDist, nsigma, -0.4, 0.4);

    c2->cd(4);  
    plotAndProfileX(hResPhiS2->hResDistVsDist,  rbx,rby,rbp,-.1, .1, 0, 2.1);

    m_phiS1 = fphiS1->GetParameter("Mean")*cmToMicron;
    m_phiS2 = fphiS2->GetParameter("Mean")*cmToMicron;
    s_phiS1 = fphiS1->GetParameter("Sigma")*cmToMicron;
    s_phiS2 = fphiS2->GetParameter("Sigma")*cmToMicron;

  }
  
  // Theta, S1 and S2
  if (false) {
    TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename+"_ThetaS1S2");
    c2->Divide(2,2);

    c2->cd(1);
    TF1* fthetaS1=draw2GFit(hResThetaS1->hResDist, nsigma, -0.4, 0.4);

    c2->cd(2);  
    plotAndProfileX(hResThetaS1->hResDistVsDist,  rbx,rby,rbp,-.1, .1, 0, 2.1);

    c2->cd(3);  
    TF1* fthetaS2=draw2GFit(hResThetaS2->hResDist, nsigma, -0.4, 0.4);

    c2->cd(4);  
    plotAndProfileX(hResThetaS2->hResDistVsDist,  rbx,rby,rbp,-.1, .1, 0, 2.1);

    m_thetaS1 = fthetaS1->GetParameter("Mean")*cmToMicron;
    m_thetaS2 = fthetaS2->GetParameter("Mean")*cmToMicron;
    s_thetaS1 = fthetaS1->GetParameter("Sigma")*cmToMicron;
    s_thetaS2 = fthetaS2->GetParameter("Sigma")*cmToMicron;

  }


  //  return;
  
  //  ----------------------------------------------------------------------

  

  // Phi/theta vs X and Y, S1
  if (false) {
    TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename+"_PhiThetaS1vsXY");
    c2->Divide(2,2);

    c2->cd(1);
    plotAndProfileX(hResPhiS1->hResDistVsX,  rbx,rby,2,-.1, .1, -130,130);

    c2->cd(2);  
    plotAndProfileX(hResPhiS1->hResDistVsY,  rbx,rby,2,-.1, .1, -130,130);

    c2->cd(3);  
    plotAndProfileX(hResThetaS1->hResDistVsX,  rbx,rby,2,-.1, .1, -130,130);

    c2->cd(4);  
    plotAndProfileX(hResThetaS1->hResDistVsY,  rbx,rby,2,-.1, .1, -130,130);

  }  

  if(talk) {
    TCanvas* c2= new TCanvas(canvbasename+"_PhiThetaS1vsXY",canvbasename+"_PhiThetaS1vsXY");
    c2->SetName(canvbasename+"_PhiThetaS1vsXY (TALK)");

    c2->SetTitle(canvbasename+"_PhiThetaS1vsXY (TALK)");
    c2->Divide(1,2);

    c2->cd(1);
    plotAndProfileX(hResPhiS1->hResDistVsY,  rbx,rby,2,-.1, .1, -130,130);

    c2->cd(2);
    plotAndProfileX(hResThetaS1->hResDistVsY,  rbx,rby,2,-.1, .1, -130,130);

  }


  // Phi/theta vs X and Y, S2
  if (false) {
    TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename+"_PhiThetaS2vsXY");
    c2->Divide(2,2);

    c2->cd(1);
    plotAndProfileX(hResPhiS2->hResDistVsX,  rbx,rby,2,-.1, .1, -130,130);

    c2->cd(2);  
    plotAndProfileX(hResPhiS2->hResDistVsY,  rbx,rby,2,-.1, .1, -130,130);

    c2->cd(3);  
    plotAndProfileX(hResThetaS2->hResDistVsX,  rbx,rby,2,-.1, .1, -130,130);

    c2->cd(4);  
    plotAndProfileX(hResThetaS2->hResDistVsY,  rbx,rby,2,-.1, .1, -130,130);

  }  


  // Phi/theta vs X and Y
  if (doPhiThetaVsXY && !talk) {
    TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename+"_PhiThetavsXY");
    c2->Divide(2,2);

    c2->cd(1);
    plotAndProfileX(hResPhi->hResDistVsX,  rbx,rby,2,-.04, .04, -130,130);

    c2->cd(2);  
    plotAndProfileX(hResPhi->hResDistVsY,  rbx,rby,2,-.04, .04, -130,130);

    c2->cd(3);  
    plotAndProfileX(hResTheta->hResDistVsX,  rbx,rby,2,-.1, .1, -130,130);

    c2->cd(4);  
    plotAndProfileX(hResTheta->hResDistVsY,  rbx,rby,2,-.1, .1, -130,130);

  }

 if(talk) {
   TCanvas* c2= new TCanvas(canvbasename+"_PhiThetavsXY",canvbasename+"_PhiThetavsXY");
    c2->SetName(canvbasename+"_PhiThetavsXY (TALK)");

    c2->SetTitle(canvbasename+"_PhiThetavsXY (TALK)");
    c2->Divide(1,2);

    c2->cd(1);
    plotAndProfileX(hResPhi->hResDistVsY,  rbx,rby,2,-.1, .1, -130,130);

    c2->cd(2);
    plotAndProfileX(hResTheta->hResDistVsY,  rbx,rby,2,-.1, .1, -130,130);

  }


  // Phi/theta vs X and Y
  if (doPhiThetaS1VsXY && !talk) {
    TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename+"_PhiThetaS1vsXY");
    c2->Divide(2,2);

    c2->cd(1);
    plotAndProfileX(hResPhiS1->hResDistVsX,  rbx,rby,2,-.1, .1, -130,130);

    c2->cd(2);  
    plotAndProfileX(hResPhiS1->hResDistVsY,  rbx,rby,2,-.1, .1, -130,130);

    c2->cd(3);  
    plotAndProfileX(hResThetaS1->hResDistVsX,  rbx,rby,2,-.1, .1, -130,130);

    c2->cd(4);  
    plotAndProfileX(hResThetaS1->hResDistVsY,  rbx,rby,2,-.1, .1, -130,130);

  }


  
  //Theta vs Y
  if (false) {
    TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename+"_ThetavsXY");

    plotAndProfileX(hResTheta->hResDistVsY,  rbx,rby,2,-.2, .2, -130,130);

  }


  // Phi/theta vs Y, S2 vs s3 (duplicate, rearrangement of the above)
  if (false) {
    TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename+"_PhiThetaS2vsXY");
    c2->Divide(2,2);

    c2->cd(1);
    plotAndProfileX(hResPhiS2->hResDistVsY,  rbx,rby,2,-.1, .1);

    c2->cd(2);  
    plotAndProfileX(hResPhi->hResDistVsY,  rbx,rby,2,-.1, .1);

    c2->cd(3);  
    plotAndProfileX(hResThetaS2->hResDistVsY,  rbx,rby,2,-.1, .1);

    c2->cd(4);  
    plotAndProfileX(hResTheta->hResDistVsY,  rbx,rby,2,-.1, .1);
  }


  // Difference between S2 and S3
  if (false) {
    TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename);
    c2->Divide(2,2);

    c2->cd(1);
    TF1* fphi1=draw2GFit(hResPhidS3S2->hResDist, nsigma, -0.4, 0.4);

    c2->cd(2);  
    plotAndProfileX(hResPhidS3S2->hResDistVsDist,  1,1,1,-.1, .1, 0, 2.1);

    c2->cd(3);  
    TF1* fphi2=draw2GFit(hResThetadS3S2->hResDist, nsigma, -0.4, 0.4);

    c2->cd(4);  
    plotAndProfileX(hResThetadS3S2->hResDistVsDist,  1,1,1,-.1, .1, 0, 2.1);
    
  }
  

  //  Difference between S2 and S3, vs X and Y
  if (false) {
    TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename);
    c2->Divide(2,2);

    c2->cd(1);
    plotAndProfileX(hResPhidS3S2->hResDistVsX,  1,1,1,-.1, .1);

    c2->cd(2);  
    plotAndProfileX(hResPhidS3S2->hResDistVsY,  1,1,1,-.1, .1);

    c2->cd(3);  
    plotAndProfileX(hResThetadS3S2->hResDistVsX,  1,1,1,-.1, .1);

    c2->cd(4);  
    plotAndProfileX(hResThetadS3S2->hResDistVsY,  1,1,1,-.1, .1);
  }

  //  Difference between S2 and S3 for phi1 and phi2, vs X and Y
  if (false) {
    TCanvas* c2= new TCanvas;
    c2->SetTitle(canvbasename);
    c2->Divide(2,2);

    c2->cd(1);
    plotAndProfileX(hResPhi1dS3S2->hResDistVsX,  1,1,1,-.1, .1);

    c2->cd(2);  
    plotAndProfileX(hResPhi1dS3S2->hResDistVsY,  1,1,1,-.1, .1);

    c2->cd(3);  
    plotAndProfileX(hResPhi2dS3S2->hResDistVsX,  1,1,1,-.1, .1);

    c2->cd(4);  
    plotAndProfileX(hResPhi2dS3S2->hResDistVsY,  1,1,1,-.1, .1);
  }

//   f << canvbasename 
//     << "  " << m_phi << " " << s_phi
//     << "  " << m_phi1 << " " << s_phi1
//     << "  " << m_phi2 << " " << s_phi2
//     << "  " << m_phiS1 << " " << s_phiS1
//     << "  " << m_phiS2 << " " << s_phiS2
//     << "  " << m_theta << " " << s_theta
//     << "  " << m_thetaS1 << " " << s_thetaS1
//     << "  " << m_thetaS2 << " " << s_thetaS2 
//     << "  " << t0phi << " " << t0theta 
//     << endl;

  
//   f << canvbasename
//        << canvbasename
//        << " Phi: D= " << int(fphi->GetParameter("Mean")*cmToMicron)
//        << " S= "  << int(fphi->GetParameter("Sigma")*cmToMicron)
//        << " Phi1: D= " << int(fphi1->GetParameter("Mean")*cmToMicron)
//        << " S= "  << int(fphi1->GetParameter("Sigma")*cmToMicron)
//        << " Phi2: D= " << int(fphi2->GetParameter("Mean")*cmToMicron)
//        << " S= "  << int(fphi2->GetParameter("Sigma")*cmToMicron)
//        << "; Theta: D= " << int(ftheta->GetParameter("Mean")*cmToMicron) 
//        << " S= "  << int(ftheta->GetParameter("Sigma")*cmToMicron) << endl << endl;

} 

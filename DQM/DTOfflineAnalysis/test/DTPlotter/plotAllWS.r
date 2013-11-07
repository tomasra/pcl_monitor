void plotAllWS(TString filename, int sector, int sl) {

   if (! TString(gSystem->GetLibraries()).Contains("DTDetId_cc")) {
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/Histograms.h");
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/DTDetId.cc+");
     gROOT->LoadMacro("$CMSSW_BASE/src/DQM/DTOfflineAnalysis/test/root_lib/Utils.cc+");
     gROOT->LoadMacro("macros2.C");
     gROOT->LoadMacro("ranges.C+");
     //     gROOT->LoadMacro("summaryPlot.C+");
   }
   
   
   bool doRes = true;
   bool doResVsDist = true;
   bool doResVsAngle = true;
   bool doResVsX = true;
   bool doResVsY = true;
   bool doAngleDist = true;
   
   float nsigma = 2;
   
   TStyle * style = getStyle("tdr");
   style->cd();  

   gStyle->SetCanvasDefW(1375); // Set larger canvas
   gStyle->SetCanvasDefH(800);  
   gStyle->SetTitleSize(0.05,"XYZ"); // Set larger axis titles
   gStyle->SetTitleOffset(1.5,"Y");
   gStyle->SetOptTitle(0); // remove histogram titles

   gROOT->ForceStyle();

   setPalette();
   opt2Dplot = "col";
   float nsigma = 2;

   TFile *file = new TFile(filename);
   
   
   TString canvbasename = filename;
   canvbasename = canvbasename.Replace(canvbasename.Length()-5,5,"") + TString("_Se") + (long) sector + "_SL" + (long) sl;
   
   
   HRes1DHits* hRes[5][4]; // W, S;  
   HSegment*   hSeg[5][4];
   //HSegment*   hSeg;
   
   for (int wheel = -2; wheel<=2; ++wheel) {
     for (int station = 1; station<=3; ++station) {
       int iW = wheel+2;
       int iSt= station-1;
       DTDetId detId2(wheel, station, sector, sl, 0, 0); 
       DTDetId chDetId(wheel, station, sector, 0, 0, 0);
       hRes[iW][iSt] = new HRes1DHits(Utils::getHistoNameFromDetIdAndSet(detId2, "Cut1"),file);
       hSeg[iW][iSt] = new HSegment(Utils::getHistoNameFromDetIdAndSet(chDetId, "Cut1"),file);
       
     }
   }
   
  if(doRes){
    TCanvas* c0= new TCanvas(canvbasename+"_AllWSRes", canvbasename+"_AllWSRes");    
    
    c0->Divide(5,3,0.0005,0.0005);

   
   for (int wheel = -2; wheel<=2; ++wheel) {
     for (int station = 1; station<=3; ++station) {
       int iW = wheel+2;
       int iSt= station-1;
       // DTDetId detId(wheel, station, sector, sl, 0, 0);
       int ipad=iW+1 + (2-iSt)*5;
       c0->cd(ipad); ++ipad;

       float min;
       float max;

       DTDetId chDetId(wheel, station, sector, sl, 0, 0);
       rangeAngle(chDetId, min, max);
      //  cout << "min" << min << endl;
//        cout << "max" << max << endl;

       TH1F* h = hRes[iW][iSt]->hResDist;
       
    //    if(sl==2){
// 	 TH1F* hAlpha = hSeg[iW][iSt]->hThetaLoc;
//        }

       TF1* fres=drawGFit(h, nsigma, -0.4, 0.4);
       
     //h->GetXaxis()->SetRangeUser(-0.4,0.4);
     // h->Draw();

     }
   }
 }
  

  if (doResVsDist) {
    TCanvas* c1= new TCanvas(canvbasename+"_AllWSResVsDist", canvbasename+"_AllWSResVsDists");    
    c1->Divide(5,3,0.0005,0.0005);


    for (int wheel = -2; wheel<=2; ++wheel) {
      for (int station = 1; station<=3; ++station) {
	int iW = wheel+2;
	int iSt= station-1;

	int ipad=iW+1 + (2-iSt)*5;
	c1->cd(ipad); ++ipad;
	plotAndProfileX(hRes[iW][iSt]->hResDistVsDist,1,1,1,-.1, .1, 0, 2.1);
      }
    }
  }
  

  if (doResVsAngle) {
//     SummaryPlot hs_p0("p0");
//     SummaryPlot hs_p1("p1");

    TCanvas* c2= new TCanvas(canvbasename+"_AllWSResVsAngle", canvbasename+"_AllWSResVsAngle");
    
    c2->Divide(5,3,0.0005,0.0005);
    
    for (int wheel = -2; wheel<=2; ++wheel) {
      for (int station = 1; station<=3; ++station) {
	int iW = wheel+2;
	int iSt= station-1;

	int ipad=iW+1 + (2-iSt)*5;
	c2->cd(ipad); ++ipad;

	float min, max;
	DTDetId chDetId(wheel, station, sector, sl, 0, 0);
	rangeAngle(chDetId, min, max);
	TH1F* hprof = plotAndProfileX(hRes[iW][iSt]->hResDistVsAngle,1,1,1,-0.02,0.02,min ,max);
	
	//	if (wheel==0&&station==1) {
	//	  cout << hprof->GetName() << endl;
	TF1 *angleDep= new TF1("angleDep","[0]*cos(x)+[1]", min, max);
	angleDep->SetParameters(0.01,0.001);
	
	hprof->Fit(angleDep,"RQN"); 
	angleDep->Draw("same");
	float p0 = angleDep->GetParameter(0);
	float p1 = angleDep->GetParameter(1);
	
	// 	  cout << "p0 = " << p0 << endl;
	// 	  cout << "p1 = " << p1 << endl;
	
// 	hs_p0.Fill(wheel, station, sector, p0);
// 	hs_p1.Fill(wheel, station, sector, p1);
	
	//cout << chDetId << " " << p0 << " " << p1 << endl;
	
	//}
      }
    }

    // Summary plot (still being developed)
//     TCanvas* c6= new TCanvas(canvbasename+"_AllWSAngleCorr_p0", canvbasename+"_AllWSAngleCorr_p0");    
//     hs_p0.hsumm->GetYaxis()->SetRangeUser(0.,0.5);
//     hs_p0.hsumm->Draw("p");
    
    
//     float p0_m[3][3];
//     float p1_m[3][3];
    
//     for (int wheel = 0; wheel<=2; ++wheel) {
//       for (int station = 1; station<=3; ++station) {

// 	float p0_n = hs_p0.hsumm->GetBinContent(hs_p0.bin(-wheel,station,0));
// 	float p0_p = hs_p0.hsumm->GetBinContent(hs_p0.bin(wheel,station,0));
// 	float p1_n = hs_p1.hsumm->GetBinContent(hs_p1.bin(-wheel,station,0));
// 	float p1_p = hs_p1.hsumm->GetBinContent(hs_p1.bin(wheel,station,0));
// 	p0_m[wheel][station] = (p0_n + p0_p)/2;
// 	p1_m[wheel][station] = (p1_n + p1_p)/2;
// 	cout << wheel << "   "   << station << "   " <<  p0_m[wheel][station] <<  "   "<<p1_m[wheel][station] <<endl;
//       }
      
//     }

  }
    
  if (doResVsX) {
    TCanvas* c3=new TCanvas(canvbasename+"_AllWSResVsX", canvbasename+"_AllWSResVsX");    
    
    c3->Divide(5,3,0.0005,0.0005);

    for (int wheel = -2; wheel<=2; ++wheel) {
      for (int station = 1; station<=3; ++station) {
	int iW = wheel+2;
	int iSt= station-1;

	int ipad=iW+1 + (2-iSt)*5;
	c3->cd(ipad); ++ipad;
	plotAndProfileX(hRes[iW][iSt]->hResDistVsX,2,1,1,-0.05, 0.05, -150, 150); // FIXME
      }
    }
  }

 if (doResVsY) {

   TCanvas* c4=new TCanvas(canvbasename+"_AllWSResVsY", canvbasename+"_AllWSResVsY");    
     
    c4->Divide(5,3,0.0005,0.0005);

    for (int wheel = -2; wheel<=2; ++wheel) {
      for (int station = 1; station<=3; ++station) {
	int iW = wheel+2;
	int iSt= station-1;

	int ipad=iW+1 + (2-iSt)*5;
	c4->cd(ipad); ++ipad;
	plotAndProfileX(hRes[iW][iSt]->hResDistVsY,2,1,1,-0.05, 0.05, -150, 150); // FIXME
      }
    }
  }

 if(doAngleDist){
   TCanvas* c5= new TCanvas(canvbasename+"_AllWSAngleDist", canvbasename+"_AllWSAngleDist");
   
   c5->Divide(5,3,0.0005,0.0005);
   
   for (int wheel = -2; wheel<=2; ++wheel) {
     for (int station = 1; station<=3; ++station) {
       int iW = wheel+2;
       int iSt= station-1;
       // DTDetId detId(wheel, station, sector, sl, 0, 0);
       int ipad=iW+1 + (2-iSt)*5;
       c5->cd(ipad); ++ipad;

       float min;
       float max;

       DTDetId chDetId(wheel, station, sector, sl, 0, 0);
       rangeAngle(chDetId, min, max);
      //  cout << "min" << min << endl;
//        cout << "max" << max << endl;

       TH1F* hAlpha = hSeg[iW][iSt]->hPhiLoc;
       
       if(sl==2){
	 TH1F* hAlpha = hSeg[iW][iSt]->hThetaLoc;
       }

   
       
       hAlpha->GetXaxis()->SetRangeUser(min,max);
       hAlpha->Draw();

     }
   }
 }
 
}





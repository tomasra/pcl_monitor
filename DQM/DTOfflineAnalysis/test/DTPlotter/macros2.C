
// Global options
TString opt2Dplot = "col";
bool addProfile = false;
bool addSlice   = true;
bool addMedian  = false;

TF1* draw2GFit(TH1 * h1, float nsigmas, float min, float max){

  gPad->SetGrid(1,1);
  gStyle->SetGridColor(15);
  h1->GetXaxis()->SetRangeUser(min,max);
  float minfit = h1->GetMean() - h1->GetRMS();
  float maxfit = h1->GetMean() + h1->GetRMS();

  static int i = 0;
  TString nameF1 = TString("g") + (Long_t)i;
  i++;
  //  TF1* g = new TF1(nameF1,"gaus", -0.4,0.4);
  TF1* g = new TF1(nameF1,"gaus", minfit, maxfit);
  h1->Fit(g,"RQ");

  //  cout<< h1->GetName() << endl;

  TF1* g1 = new TF1(nameF1,"gaus(0)+gaus(3)", min, max);
  g1->SetParNames("Const", "Mean", "Sigma", "tail const", "tail Mean", "tail Sigma");
  g1->SetLineColor(2);
  g1->SetLineWidth(2);
  g1->SetParameter(0,  0.9*g->GetParameter(0));
  g1->SetParameter(1,  g->GetParameter(1));
  g1->SetParameter(2,  g->GetParameter(2));
  g1->SetParLimits(2,0.,max);
  g1->SetParameter(3,  0.1*g->GetParameter(0));
  g1->SetParameter(4,  g->GetParameter(1));
  g1->SetParameter(5,  2*g->GetParameter(2));
  g1->SetParLimits(5,0.,max);
  
//   minfit = g1->GetParameter("Mean") - nsigmas*g1->GetParameter("Sigma");
//   maxfit = g1->GetParameter("Mean") + nsigmas*g1->GetParameter("Sigma");
//   g1->SetRange(minfit,maxfit);
  h1->Fit(g1,"RQ");

  // Check that core and tail are found in the expected order
  if (g1->GetParameter(0)< g1->GetParameter(3)){
    float c=g1->GetParameter(3);
    float m=g1->GetParameter(4);
    float s=g1->GetParameter(5);
    g1->SetParameter(3,  g1->GetParameter(0));
    g1->SetParameter(4,  g1->GetParameter(1));
    g1->SetParameter(5,  g1->GetParameter(2));
    g1->SetParameter(0,  c);
    g1->SetParameter(1,  m);
    g1->SetParameter(2,  s);
    h1->Fit(g1,"RQ");
  }

  gPad->Draw();
  return g1;
}

TF1* drawGFit(TH1 * h1, float nsigmas, float min, float max){

  gPad->SetGrid(1,1);
  gStyle->SetGridColor(15);
  h1->GetXaxis()->SetRangeUser(min,max);
  float minfit = h1->GetMean() - h1->GetRMS();
  float maxfit = h1->GetMean() + h1->GetRMS();
  
  TLine * l = new TLine(0,0,0,h1->GetMaximum()*1.05);
  
  l->SetLineColor(3);
  l->SetLineWidth(2);

  static int i = 0;
  TString nameF1 = TString("g") + (Long_t)i;
  i++;
  TF1* g1 = new TF1(nameF1,"gaus",minfit,maxfit);

  g1->SetLineColor(2);
  g1->SetLineWidth(2);
  h1->Fit(g1,"RQ");
  
  minfit = g1->GetParameter("Mean") - nsigmas*g1->GetParameter("Sigma");
  maxfit = g1->GetParameter("Mean") + nsigmas*g1->GetParameter("Sigma");
  g1->SetRange(minfit,maxfit);

  h1->Fit(g1,"RQ");
  TF1* fh=h1->GetFunction(nameF1);
  if (fh) fh->FixParameter(0,g1->GetParameter(0)); // so that it is not shown in legend

  gPad->Draw();
  l->Draw();
  h1->Draw("same"); //redraw on top of the line
  return g1;
}


// void plotSigmaVsX (TH2* h2, int rebinX, int rebinY) {
//   gPad->SetGrid(1,1);
//   gStyle->SetGridColor(15);
//   h2->Rebin2D(rebinX,rebinY);
//   in nbinsX = h2->GetNbinsX();
//   // loop over all 
//   for(int bin = 
//   for

// }

TH1F* plotAndProfileSigmaX (TH2* h2, int rebinX, int rebinY, int rebinProfile, float minY, float maxY, float minX=0, float maxX=0) {
  //  setStyle(h2);
  gPad->SetGrid(1,1);
  gStyle->SetGridColor(15);
  TH2* h2Clone = h2->Clone();
  h2Clone->Rebin2D(rebinX,rebinY);
  h2Clone->GetYaxis()->SetRangeUser(minY,maxY);

  TLine * l = new TLine(h2Clone->GetXaxis()->GetXmin(),0,h2Clone->GetXaxis()->GetXmax(),0);
  if (maxX>minX) {
    h2Clone->GetXaxis()->SetRangeUser(minX,maxX);  
    l->SetX1(minX);
    l->SetX2(maxX);
  }

//   h2Clone->SetMarkerStyle(1);
//   h2Clone->Draw(opt2Dplot);
//   l->SetLineColor(3);
//   l->SetLineWidth(2);
//   l->Draw();
//   if (addProfile) {
//     TAxis* yaxis = h2Clone->GetYaxis();
//     //Add option "s" to draw RMS as error instead than RMS/sqrt(N)
//     TProfile* prof = h2Clone->ProfileX("_pfx", yaxis->FindBin(minY), yaxis->FindBin(maxY));
//     //    TProfile* prof = h2Clone->ProfileX("_pfx");
//     prof->SetMarkerColor(2);
//     prof->SetMarkerStyle(20);
//     prof->SetMarkerSize(0.4);
//     prof->SetLineColor(2);
//     prof->Rebin(rebinProfile);
//     prof->Draw("same");
//   }
//   if (addSlice) {
  TObjArray aSlices;
  TF1 fff("a", "gaus", -0.05, 0.05);   
  h2Clone->FitSlicesY(&fff, 0, -1, 0, "QNRG2", &aSlices);
  TH1F*  ht = aSlices[2]->Clone();    
  ht->SetMarkerColor(4);
  ht->GetYaxis()->SetRangeUser(minY,maxY);
  ht->GetXaxis()->SetRangeUser(minX,maxX);
  ht->Draw();
  //   }

  return ht;

}




// Plot a TH2 + add profiles on top of it
// minY, maxY: Y range for plotting and for computing profile if addProfile==true.
//             Note that the simple profile is very sensitive to the Y range used!
TH1F* plotAndProfileX (TH2* theh, int rebinX, int rebinY, int rebinProfile, float minY, float maxY, float minX=0, float maxX=0) {
  TH2* h2=theh->Clone();
  
  //  setStyle(h2);
  if (h2==0) {
    cout << "plotAndProfileX: null histo ptr" << endl;
    return;
  }
  
  gPad->SetGrid(1,1);
  gStyle->SetGridColor(15);
  h2->Rebin2D(rebinX,rebinY);
  //  h2->GetYaxis()->SetRangeUser(minY,maxY);

  TLine * l = new TLine(h2->GetXaxis()->GetXmin(),0,h2->GetXaxis()->GetXmax(),0);
  if (maxX>minX) {
    h2->GetXaxis()->SetRangeUser(minX,maxX);  
    l->SetX1(minX);
    l->SetX2(maxX);
  }

  h2->SetMarkerStyle(1);
  h2->Draw(opt2Dplot);
  l->SetLineColor(3);
  l->SetLineWidth(2);
  l->Draw();
  if (addProfile) {
    TAxis* yaxis = h2->GetYaxis();
    //Add option "s" to draw RMS as error instead than RMS/sqrt(N)
    TProfile* prof = h2->ProfileX("_pfx", 
				  TMath::Max(1,yaxis->FindBin(minY)), 
				  TMath::Min(yaxis->GetNbins(),yaxis->FindBin(maxY)));
//     cout << yaxis->FindBin(minY) << " " << yaxis->FindBin(maxY) << endl;
//     cout << yaxis->GetNbins();
    //TProfile* prof = h2->ProfileX("_pfx");
    prof->SetMarkerColor(2);
    prof->SetMarkerStyle(20);
    prof->SetMarkerSize(0.4);
    prof->SetLineColor(2);
    prof->Rebin(rebinProfile);
    prof->Draw("same");
  }

  TH1F* ht=0;

  if (addSlice) {
    TObjArray aSlices;
    //    TF1 fff("a", "gaus", -0.1, 0.1);   
    h2->FitSlicesY(0, 0, -1, 0, "QNR", &aSlices); // add "G2" to merge 2 consecutive bins
    
    ht = (TH1F*) aSlices[1]->Clone();
    Utils::newName(ht);
    ht->SetMarkerColor(4);
    ht->Draw("same");
  }

  if (addMedian) {
    double xq[1] = {0.5};
    double median[1];

    TAxis* axis =  h2->GetXaxis();
    TH1F* medprof = new TH1F(h2->GetName()+TString("medians"),"medians", axis->GetNbins(), axis->GetXmin(), axis->GetXmax());
    float bw =  h2->GetYaxis()->GetBinLowEdge(2)-h2->GetYaxis()->GetBinLowEdge(1);
    

    TString projname = h2->GetName()+TString("_pmedian");
    for (int bin=1; bin<=h2->GetNbinsX(); ++bin){
      TH1D * proj = h2->ProjectionY(projname, bin, bin);
      double integral = proj->Integral();
      if (integral==0) continue;
      // Take overflow and underflow into account
      int nbins = proj->GetNbinsX();
      proj->SetBinContent(1, proj->GetBinContent(0)+proj->GetBinContent(1));
      proj->SetBinContent(0,0);
      proj->SetBinContent(nbins, proj->GetBinContent(nbins)+proj->GetBinContent(nbins+1));
      proj->SetBinContent(nbins+1,0);
      proj->GetQuantiles(1,median,xq);
      medprof->SetBinContent(bin,median[0]);
      // Approximated uncertainty on median, probably underestimated.
      medprof->SetBinError(bin,bw*sqrt(integral/2.)/2./TMath::Max(1.,proj->GetBinContent(proj->FindBin(median[0]))));
    }
    medprof->SetMarkerColor(2);
    medprof->SetMarkerStyle(20);
    medprof->SetMarkerSize(0.4);
    medprof->Draw("Esame");
  }

  h2->GetYaxis()->SetRangeUser(minY,maxY);

  return ht;
}


// Print all canvases in separate files
void printCanvases(TString type="png", TString path="."){
  TIter iter(gROOT->GetListOfCanvases());
  TCanvas *c;
  while( (c = (TCanvas *)iter()) ) {
    TString name =  path+"/"+c->GetTitle()+"."+type;
    c->Print(name);
  }
}


setPalette()
{
  const Int_t NRGBs = 5;
  const Int_t NCont = 255;
 
//   { // Fine rainbow
//     Double_t stops[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
//     Double_t red[NRGBs]   = { 0.00, 0.00, 0.87, 1.00, 0.51 };
//     Double_t green[NRGBs] = { 0.00, 0.81, 1.00, 0.20, 0.00 };
//     Double_t blue[NRGBs]  = { 0.51, 1.00, 0.12, 0.00, 0.00 };
//   }
 
//   { // blues
//     Double_t stops[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
//     Double_t red[NRGBs]   = { 1.00, 0.84, 0.61, 0.34, 0.00 };
//     Double_t green[NRGBs] = { 1.00, 0.84, 0.61, 0.34, 0.00 };
//     Double_t blue[NRGBs]  = { 1.00, 1.00, 1.00, 1.00, 1.00 };
//   }


//   { // Gray (white->black)
//     Double_t stops[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
//     Double_t red[NRGBs]   = { 1.00, 0.84, 0.61, 0.34, 0.00 };
//     Double_t green[NRGBs] = { 1.00, 0.84, 0.61, 0.34, 0.00 };
//     Double_t blue[NRGBs]  = { 1.00, 0.84, 0.61, 0.34, 0.00 };
//   }


  { // Gray (white->gray)
    //  similar to gStyle->SetPalette(5);
    float max = 0.3;
    float step=(1-max)/(NRGBs-1);
    Double_t stops[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
    Double_t red[NRGBs]   = { 1.00, 1-step, 1-2*step, 1-3*step, 1-4*step };
    Double_t green[NRGBs] = { 1.00, 1-step, 1-2*step, 1-3*step, 1-4*step };
    Double_t blue[NRGBs]  = { 1.00, 1-step, 1-2*step, 1-3*step, 1-4*step };
  }


 TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
 gStyle->SetNumberContours(NCont);
}



TStyle * getStyle(TString name) {
  TStyle *theStyle;

  if ( name == "myStyle" ) {
    theStyle = new TStyle("myStyle", "myStyle");
    //    theStyle->SetOptStat(0);
    theStyle->SetPadBorderMode(0);
    theStyle->SetCanvasBorderMode(0);
    theStyle->SetPadColor(0);
    theStyle->SetCanvasColor(0);
    theStyle->SetMarkerStyle(8);
    theStyle->SetMarkerSize(0.7);
    theStyle->SetStatH(0.3);
    theStyle->SetStatW(0.15);
    //   theStyle->SetTextFont(132);
    //   theStyle->SetTitleFont(132);
    theStyle->SetTitleBorderSize(1);
    theStyle->SetPalette(1);

  } else if( name == "tdr" ) {
    theStyle = new TStyle("tdrStyle","Style for P-TDR");

    // For the canvas:
    theStyle->SetCanvasBorderMode(0);
    theStyle->SetCanvasColor(kWhite);
//      theStyle->SetCanvasDefH(600); //Height of canvas
//      theStyle->SetCanvasDefW(800); //Width of canvas
    theStyle->SetCanvasDefH(750); //Height of canvas
    theStyle->SetCanvasDefW(1000); //Width of canvas

    theStyle->SetCanvasDefX(0);   //POsition on screen
    theStyle->SetCanvasDefY(0);

    // For the Pad:
    theStyle->SetPadBorderMode(0);
    // theStyle->SetPadBorderSize(Width_t size = 1);
    theStyle->SetPadColor(kWhite);
    theStyle->SetPadGridX(true);
    theStyle->SetPadGridY(true);
    theStyle->SetGridColor(0);
    theStyle->SetGridStyle(3);
    theStyle->SetGridWidth(1);

    // For the frame:
    theStyle->SetFrameBorderMode(0);
    theStyle->SetFrameBorderSize(1);
    theStyle->SetFrameFillColor(0);
    theStyle->SetFrameFillStyle(0);
    theStyle->SetFrameLineColor(1);
    theStyle->SetFrameLineStyle(1);
    theStyle->SetFrameLineWidth(1);

    // For the histo:
    // theStyle->SetHistFillColor(1);
    // theStyle->SetHistFillStyle(0);
    theStyle->SetHistLineColor(kBlue);
    theStyle->SetMarkerColor(kBlue);
    //    theStyle->SetHistLineStyle(0);
    //    theStyle->SetHistLineWidth(1);
    // theStyle->SetLegoInnerR(Float_t rad = 0.5);
    // theStyle->SetNumberContours(Int_t number = 20);


     theStyle->SetEndErrorSize(2);
//     theStyle->SetErrorMarker(20);
//     theStyle->SetErrorX(0.);

    theStyle->SetMarkerStyle(20);
    theStyle->SetMarkerSize(0.5);


    //For the fit/function:
    theStyle->SetOptFit(1);
    theStyle->SetFitFormat("5.4g");
    theStyle->SetFuncColor(2);
    theStyle->SetFuncStyle(1);
    theStyle->SetFuncWidth(1);

    //For the date:
    theStyle->SetOptDate(0);
    // theStyle->SetDateX(Float_t x = 0.01);
    // theStyle->SetDateY(Float_t y = 0.01);

    // For the statistics box:
    theStyle->SetOptFile(0);
//     theStyle->SetOptStat(0); // To display the mean and RMS:   SetOptStat("mr");

    theStyle->SetOptStat("e");
    theStyle->SetStatColor(kWhite);
    //    theStyle->SetStatFont(42);
    //    theStyle->SetStatFontSize(0.05);
    theStyle->SetStatTextColor(1);
    theStyle->SetStatFormat("6.4g");
    theStyle->SetStatBorderSize(1);
//     theStyle->SetStatH(0.02);
//     theStyle->SetStatW(0.2);
    // theStyle->SetStatStyle(Style_t style = 1001);
    theStyle->SetStatX(0.94);
    theStyle->SetStatY(0.96);

    // Margins:
//      theStyle->SetPadTopMargin(0.1);
      theStyle->SetPadBottomMargin(0.11);
//      theStyle->SetPadLeftMargin(0.1);
//      theStyle->SetPadRightMargin(0.05);
    theStyle->SetPadLeftMargin(0.15);

    // For the Global title:
    
    //    theStyle->SetOptTitle(0); // Uncomment to remove title
//     theStyle->SetTitleFont(42);
//     theStyle->SetTitleColor(1);
//     theStyle->SetTitleTextColor(1);
    theStyle->SetTitleFillColor(0);
//     theStyle->SetTitleFontSize(0.05);
    // theStyle->SetTitleH(0); // Set the height of the title box
    // theStyle->SetTitleW(0); // Set the width of the title box
    // theStyle->SetTitleX(0); // Set the position of the title box
    theStyle->SetTitleY(0.96); // Set the position of the title box
    theStyle->SetTitleStyle(0);
    theStyle->SetTitleBorderSize(0);


    // For the axis titles:

//     theStyle->SetTitleColor(1, "XYZ");
//     theStyle->SetTitleFont(42, "XYZ");
    //    theStyle->SetTitleSize(0.05, "XYZ");
    // theStyle->SetTitleXSize(Float_t size = 0.02); // Another way to set the size?
    // theStyle->SetTitleYSize(Float_t size = 0.02);
//     theStyle->SetTitleXOffset(0.9);
//     theStyle->SetTitleYOffset(1.25);
    // theStyle->SetTitleOffset(1.1, "Y"); // Another way to set the Offset

    // For the axis labels:

//     theStyle->SetLabelColor(1, "XYZ");
//     theStyle->SetLabelFont(42, "XYZ");
//     theStyle->SetLabelOffset(0.007, "XYZ");
//     theStyle->SetLabelSize(0.045, "XYZ");

    // For the axis:

    theStyle->SetAxisColor(1, "XYZ");
    theStyle->SetStripDecimals(kTRUE);
    theStyle->SetTickLength(0.03, "XYZ");
    theStyle->SetNdivisions(510, "XYZ");
    theStyle->SetPadTickX(1);  // To get tick marks on the opposite side of the frame
    theStyle->SetPadTickY(1);

    // Change for log plots:
    theStyle->SetOptLogx(0);
    theStyle->SetOptLogy(0);
    theStyle->SetOptLogz(0);

    // Postscript options:
    theStyle->SetPaperSize(20.,20.);
    // theStyle->SetLineScalePS(Float_t scale = 3);
    // theStyle->SetLineStyleString(Int_t i, const char* text);
    // theStyle->SetHeaderPS(const char* header);
    // theStyle->SetTitlePS(const char* pstitle);

    // theStyle->SetBarOffset(Float_t baroff = 0.5);
    // theStyle->SetBarWidth(Float_t barwidth = 0.5);
    // theStyle->SetPaintTextFormat(const char* format = "g");
    // theStyle->SetPalette(Int_t ncolors = 0, Int_t* colors = 0);
    // theStyle->SetTimeOffset(Double_t toffset);
    // theStyle->SetHistMinimumZero(kTRUE);
    theStyle->SetTextSize(0.045);
    //    theStyle->SetTextFont(42);
    
    //   style->SetOptFit(101);
    //   style->SetOptStat(1111111); 

  }  else if( name == "d0style" ) {
    theStyle = new TStyle("d0Style","Style for P-TDR");
    int font = 42;


    // For the canvas:
    theStyle->SetCanvasBorderMode(0);
    theStyle->SetCanvasColor(kWhite);
    theStyle->SetCanvasDefH(600); //Height of canvas
    theStyle->SetCanvasDefW(600); //Width of canvas
    theStyle->SetCanvasDefX(0);   //POsition on screen
    theStyle->SetCanvasDefY(0);

    // For the Pad:
    theStyle->SetPadBorderMode(0);
    // theStyle->SetPadBorderSize(Width_t size = 1);
    theStyle->SetPadColor(kWhite);
    theStyle->SetPadGridX(true);
    theStyle->SetPadGridY(true);
    theStyle->SetGridColor(0);
    theStyle->SetGridStyle(3);
    theStyle->SetGridWidth(1);

    // For the frame:
    theStyle->SetFrameBorderMode(0);
    theStyle->SetFrameBorderSize(1);
    theStyle->SetFrameFillColor(0);
    theStyle->SetFrameFillStyle(0);
    theStyle->SetFrameLineColor(1);
    theStyle->SetFrameLineStyle(1);
    theStyle->SetFrameLineWidth(1);

    // For the histo:
    // theStyle->SetHistFillColor(1);
    // theStyle->SetHistFillStyle(0);
    theStyle->SetHistLineColor(1);
    theStyle->SetHistLineStyle(0);
    theStyle->SetHistLineWidth(1);
    // theStyle->SetLegoInnerR(Float_t rad = 0.5);
    // theStyle->SetNumberContours(Int_t number = 20);


     theStyle->SetEndErrorSize(2);
//     theStyle->SetErrorMarker(20);
//     theStyle->SetErrorX(0.);

    theStyle->SetMarkerStyle(20);
    theStyle->SetMarkerSize(0.5);


    //For the fit/function:
    theStyle->SetOptFit(1);
    theStyle->SetFitFormat("5.4g");
    theStyle->SetFuncColor(2);
    theStyle->SetFuncStyle(1);
    theStyle->SetFuncWidth(1);

    //For the date:
    theStyle->SetOptDate(0);
    // theStyle->SetDateX(Float_t x = 0.01);
    // theStyle->SetDateY(Float_t y = 0.01);

    // For the statistics box:
    theStyle->SetOptFile(0);
//     theStyle->SetOptStat(0); // To display the mean and RMS:   SetOptStat("mr");
    theStyle->SetOptStat("e");
    theStyle->SetStatColor(kWhite);
    theStyle->SetStatFont(font);
    theStyle->SetStatFontSize(0.05);
    theStyle->SetStatTextColor(1);
    theStyle->SetStatFormat("6.4g");
    theStyle->SetStatBorderSize(1);
    theStyle->SetStatH(0.02);
    theStyle->SetStatW(0.2);
    // theStyle->SetStatStyle(Style_t style = 1001);
    theStyle->SetStatX(0.82);
//     theStyle->SetStatY(0.5);

    // Margins:
    theStyle->SetPadTopMargin(0.02);
    theStyle->SetPadBottomMargin(0.13);
    theStyle->SetPadLeftMargin(0.16);
    theStyle->SetPadRightMargin(0.02);

    // For the Global title:

    theStyle->SetOptTitle(0);
    theStyle->SetTitleFont(font);
    theStyle->SetTitleColor(1);
    theStyle->SetTitleTextColor(1);
    theStyle->SetTitleFillColor(10);
    theStyle->SetTitleFontSize(0.07);
    // theStyle->SetTitleH(0); // Set the height of the title box
    // theStyle->SetTitleW(0); // Set the width of the title box
    // theStyle->SetTitleX(0); // Set the position of the title box
    // theStyle->SetTitleY(0.985); // Set the position of the title box
    theStyle->SetTitleStyle(1001);
    // theStyle->SetTitleBorderSize(2);

    // For the axis titles:

    theStyle->SetTitleColor(1, "XYZ");
    theStyle->SetTitleFont(font, "XYZ");
    theStyle->SetTitleSize(0.07, "XYZ");
    // theStyle->SetTitleXSize(Float_t size = 0.02); // Another way to set the size?
    // theStyle->SetTitleYSize(Float_t size = 0.02);
    theStyle->SetTitleXOffset(0.85);
    theStyle->SetTitleYOffset(1.25);
    // theStyle->SetTitleOffset(1.1, "Y"); // Another way to set the Offset

    // For the axis labels:

    theStyle->SetLabelColor(1, "XYZ");

    theStyle->SetLabelFont(font, "XYZ");
//     theStyle->SetLabelOffset(0.007, "XYZ");

    theStyle->SetLabelSize(0.07, "XYZ");

    // For the axis:

    theStyle->SetAxisColor(1, "XYZ");
    theStyle->SetStripDecimals(kTRUE);
    theStyle->SetTickLength(0.03, "XYZ");
    theStyle->SetNdivisions(508, "YZ");
    theStyle->SetNdivisions(508, "X");


//     theStyle->SetNdivisions(-500,"xyz");
    theStyle->SetPadTickX(1);  // To get tick marks on the opposite side of the frame
    theStyle->SetPadTickY(1);

    // Change for log plots:
    theStyle->SetOptLogx(0);
    theStyle->SetOptLogy(0);
    theStyle->SetOptLogz(0);

    // Postscript options:
    theStyle->SetPaperSize(20.,20.);
    // theStyle->SetLineScalePS(Float_t scale = 3);
    // theStyle->SetLineStyleString(Int_t i, const char* text);
    // theStyle->SetHeaderPS(const char* header);
    // theStyle->SetTitlePS(const char* pstitle);

    // theStyle->SetBarOffset(Float_t baroff = 0.5);
    // theStyle->SetBarWidth(Float_t barwidth = 0.5);
    // theStyle->SetPaintTextFormat(const char* format = "g");
    // theStyle->SetPalette(Int_t ncolors = 0, Int_t* colors = 0);
    // theStyle->SetTimeOffset(Double_t toffset);
    // theStyle->SetHistMinimumZero(kTRUE);
    theStyle->SetTextSize(0.06);
    theStyle->SetTextFont(font);
    
    //   style->SetOptFit(101);
    //   style->SetOptStat(1111111); 
    // From d0macro.C
   theStyle->SetLabelFont(42,"X");       // 42
   theStyle->SetLabelFont(42,"Y");       // 42
   theStyle->SetLabelOffset(0.000,"X");  // D=0.005
   theStyle->SetLabelOffset(0.005,"Y");  // D=0.005
   theStyle->SetLabelSize(0.07,"X");
   theStyle->SetLabelSize(0.07,"Y");
   theStyle->SetTitleOffset(0.9,"X");
   theStyle->SetTitleOffset(1.2,"Y");
   theStyle->SetTitleSize(0.07,"X");
   theStyle->SetTitleSize(0.07,"Y");
   theStyle->SetTitle(0);

  } else {
    // Avoid modifying the default style!
    theStyle = gStyle;
  }
  return theStyle;
}


TH1F* getValHist(TFile* a,  int wheel, int station, int sl, TString hn) {
  TString hname = "DQMData/Run 1/DT/Run summary/1DRecHits/1D_S3";
      
  if (sl == 2) {
    hname = hname+"RZ_W";
  } else {
    hname = hname+"RPhi_W";
  }
      
  hname = hname+(long) abs(wheel) + "_" + hn + "MB" + (long) station;
      
      
  return (TH1F*) a->Get(hname);
}


TH2F* getVal2DHist(TFile* a,  int wheel, int sl, TString hn) {
  TString hname = "DQMData/Run 1/DT/Run summary/1DRecHits/1D_S3";
      
  if (sl == 2) {
    hname = hname+"RZ_W";
  } else {
    hname = hname+"RPhi_W";
  }
      
  hname = hname+(long) abs(wheel) + "_" + hn;
      
      
  return (TH2F*) a->Get(hname);
}


// Write a line to file f, in the format of the vdrift table
void writeVDriftTable(ofstream& f, int wheel, int station, int sector, int sl, float vdrift, float sigma) {
  f << wheel << " " << station << " " << sector << " " << sl << " 0 0 -1 -1 -1 " << vdrift << " " << sigma << endl;
}


// Write a line to file f, in the format of the ttrig table
void writeTTrigTable(ofstream& f, int wheel, int station, int sector, int sl, float ttrig) {
  f << wheel << " " << station << " " << sector << " " << sl << " 0 0 " << ttrig << " 0 0 -1 -1 " << endl;
}


void plotEff(TH1* h1, TH1* h2=0, TH1* h3=0) {
  float minY=0.6;
  float maxY=1.05;
  h1->GetYaxis()->SetRangeUser(minY,maxY);
  h1->GetXaxis()->SetRangeUser(0.,2.1);
  h1->SetStats(0);
  h1->Draw();
  
  if (h2) {
    h2->SetLineColor(kRed);
    h2->SetMarkerColor(kRed);
    h2->SetStats(0);
    h2->Draw("same");
    
    if (h3) {
      h3->SetLineColor(kBlack);
      h3->SetMarkerColor(kBlack);
      h3->SetStats(0);
      h3->Draw("same");
    }
  }
}



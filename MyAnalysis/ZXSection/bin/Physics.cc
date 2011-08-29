TH1F *HPT1, *HPT2, *HPTFull, *HMomentum, *HRestMass;
TH1F *HTheta1, *HTheta2, *HDeltaPhi, *HThetaFull;
TH1F *HEta1, *HEta2, *HEtaFull;
TH1F *HMet, *HJets, *HVertexNo;

Double_t DeltaPhi(Double_t Phi1, Double_t Phi2)
{
  Double_t TempRes = Phi2 - Phi1;
  
  while (TempRes >  TMath::Pi()) TempRes -= TMath::Pi()*2;
  while (TempRes < -TMath::Pi()) TempRes += TMath::Pi()*2;

  return TempRes;
}

Bool_t InitializeHistograms(FGJob *Job)
{
  TList *TempList = new TList;

  hOutputFile -> cd();
  hOutputFile -> mkdir(Job -> FileName);
  hOutputFile -> cd(OutputPath + ":/" + (Job -> FileName));

  TempList -> Add((TObject *)(HPT1 = new TH1F("Leading Momentum", "Leading lepton transverse momentum", 200, 0, 600)));
  TempList -> Add((TObject *)(HPT2 = new TH1F("Trailing Momentum", "Leading lepton transverse momentum", 200, 18, 225)));
  TempList -> Add((TObject *)(HPTFull = new TH1F("Dilepton Momentum", "Leading lepton transverse momentum", 200, 0, 700)));

  TempList -> Add((TObject *)(HMomentum = new TH1F("Momentum",  "Dilepton momentum", 200, 0, 1200))); 
  TempList -> Add((TObject *)(HRestMass = new TH1F("Rest Mass", "Dilepton rest mass", 160, 75, 107))); 
 
  HMomentum -> GetXaxis() -> SetTitle("p");
  HMomentum -> GetYaxis() -> SetTitle("\\frac{\\partial #sigma (pb)}{\\partial p}");
  HRestMass -> GetXaxis() -> SetTitle("Py");
  HRestMass -> GetYaxis() -> SetTitle("\\frac{\\partial #sigma (pb)}{\\partial m}");

  TempList -> Add((TObject *)(   HTheta1 = new TH1F("Leading Theta", "First lepton Theta angle Distribution", 200, 0, TMath::Pi())));
  TempList -> Add((TObject *)(   HTheta2 = new TH1F("Trailing Theta", "Second lepton Theta angle Distribution", 200, 0, TMath::Pi())));
  TempList -> Add((TObject *)(HThetaFull = new TH1F("Dilepton Theta", "Dilepton Theta angle Distribution", 200, 0, TMath::Pi())));
  TempList -> Add((TObject *)( HDeltaPhi = new TH1F("Dilepton DeltaPhi", "Dilepton Phi angle Distribution", 200, -TMath::Pi(), TMath::Pi())));

  TempList -> Add((TObject *)(    HEta1 = new TH1F("Leading Eta", "First lepton pseudorapidity Distribution", 200, -3, 3)));
  TempList -> Add((TObject *)(    HEta2 = new TH1F("Trailing Eta", "Second lepton pseudorapidity Distribution", 200, -3, 3)));
  TempList -> Add((TObject *)( HEtaFull = new TH1F("Dilepton Eta", "Dilepton pseudorapidity Distribution", 200, -11, 11)));
  TempList -> Add((TObject *)(     HMet = new TH1F("Missing transverse", "Missing transverse energy Distribution", 200, -0, 300))); 
  TempList -> Add((TObject *)(    HJets = new TH1F("Jet number", "Jet number Distribution", 20, 0, 20))); 
  TempList -> Add((TObject *)(HVertexNo = new TH1F("Vertex count", "Vertex number", 15, 0, 15))); 

  for (Int_t i = 0; TempList -> At(i) != 0; i++)
  {
    ((TH1F *)TempList -> At(i)) -> SetFillColor(FGColor(ColorCount));
    ((TH1F *)TempList -> At(i)) -> Sumw2();
  }

  return kTRUE;
}

Bool_t FillHistograms(PhysicsEvent_t *Event, Float_t Weight, FGJob *Job)
{
  LorentzVector zll = Event -> leptons[0] + Event -> leptons[1];
  Double_t Momentum = zll.X()*zll.X() + zll.Y()*zll.Y() + zll.Z()*zll.Z();

  //if (Event -> Tag == 1) {
  if (TMath::Sqrt(zll.T()*zll.T() - Momentum) > 76 &&
      TMath::Sqrt(zll.T()*zll.T() - Momentum) < 106) {
    HPT1 -> Fill(TMath::Sqrt(Event -> leptons[0].X() * Event -> leptons[0].X() + 
                             Event -> leptons[0].Y() * Event -> leptons[0].Y()), Weight * (Job -> Normalization));
    HPT2 -> Fill(TMath::Sqrt(Event -> leptons[1].X() * Event -> leptons[1].X() + 
                             Event -> leptons[1].Y() * Event -> leptons[1].Y()), Weight * (Job -> Normalization));

    HPTFull -> Fill(TMath::Sqrt(zll.X() * zll.X() + zll.Y() * zll.Y()), Weight * (Job -> Normalization));

    HDeltaPhi -> Fill(DeltaPhi(Event -> leptons[0].Phi(), Event -> leptons[1].Phi()), Weight * (Job -> Normalization));

    HEta1 -> Fill(Event -> leptons[0].Eta(), Weight * (Job -> Normalization));
    HEta2 -> Fill(Event -> leptons[1].Eta(), Weight * (Job -> Normalization));
    HEtaFull -> Fill(zll.Eta(), Weight * (Job -> Normalization));

    HMet -> Fill(Event -> met[0].T(), Weight * (Job -> Normalization));
    HJets -> Fill(Event -> jets.size(), Weight * (Job -> Normalization));
    HVertexNo -> Fill(Event -> VertexCount, Weight * (Job -> Normalization));

    HMomentum -> Fill(TMath::Sqrt(Momentum), Weight * (Job -> Normalization));
    HRestMass -> Fill(TMath::Sqrt(zll.T()*zll.T() - Momentum), Weight * (Job -> Normalization));
  
    HTheta1    -> Fill(Event -> leptons[0].Theta(), Weight * (Job -> Normalization));
    HTheta2    -> Fill(Event -> leptons[1].Theta(), Weight * (Job -> Normalization));
    HThetaFull -> Fill(zll.Theta(), Weight * (Job -> Normalization));

    Job -> ContentSum +=  Weight * (Job->Normalization);
    if (!(Job -> isMC)) ParserEventAdd(Event, Job);
    }

  return kTRUE;
}

Bool_t SaveHistograms(FGJob *Job)
{
  TObjArray *HistogramStack = new TObjArray(TCollection::kInitCapacity, 0);

  /*HistogramStack -> Add(HPT1);
  HistogramStack -> Add(HPT2);
  HistogramStack -> Add(HPTFull);*/

  HistogramStack -> Add(HMomentum);
  HistogramStack -> Add(HRestMass);

  /*HistogramStack -> Add(HTheta1);
  HistogramStack -> Add(HTheta2);
  HistogramStack -> Add(HDeltaPhi);
  HistogramStack -> Add(HThetaFull);

  HistogramStack -> Add(HEta1);
  HistogramStack -> Add(HEta2);
  HistogramStack -> Add(HEtaFull);

  HistogramStack -> Add(HMet);
  HistogramStack -> Add(HJets);
  HistogramStack -> Add(HVertexNo);*/

  //HistogramStack -> Add(HTest);

  hOutputFile -> cd(OutputPath + ":/" + (Job -> FileName));
  //  cout << "Mi sposto nella cartella " << OutputPath + ":/" + (Job -> FileName) << "\n";
  
  HMomentum -> SetTitle(Job -> FileName);
  HRestMass -> SetTitle(Job -> FileName);

  HistogramStack -> Write();
  
  hOutputFile -> Flush();
//HistogramStack -> Write();

  return kTRUE;
}


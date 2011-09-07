TH2F *HPT1, *HPT2, *HPTFull, *HMomentum, *HRestMass;
TH2F *HTheta1, *HTheta2, *HDeltaPhi, *HThetaFull;
TH2F *HEta1, *HEta2, *HEtaFull;
TH2F *HMet, *HJets, *HVertexNo;

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

  TempList -> Add((TObject *)(HPT1 = new TH2F("Leading Momentum", "Leading lepton transverse momentum", 100, 0, 2, 200, 0, 600)));
  TempList -> Add((TObject *)(HPT2 = new TH2F("Trailing Momentum", "Leading lepton transverse momentum", 100, 0, 2, 200, 18, 225)));
  TempList -> Add((TObject *)(HPTFull = new TH2F("Dilepton Momentum", "Leading lepton transverse momentum", 100, 0, 2, 200, 0, 700)));

  HPT1 -> GetYaxis() -> SetTitle("p");
  HPT2 -> GetYaxis() -> SetTitle("p");
  HPTFull -> GetYaxis() -> SetTitle("p");

  TempList -> Add((TObject *)(HMomentum = new TH2F("Momentum",  "Dilepton momentum", 100, 0, 2, 200, 0, 1200))); 
  TempList -> Add((TObject *)(HRestMass = new TH2F("Rest Mass", "Dilepton rest mass", 100, 0, 2, 160, 75,  107))); 
 
  HMomentum -> GetYaxis() -> SetTitle("p");
  HRestMass -> GetYaxis() -> SetTitle("m");

  TempList -> Add((TObject *)(   HTheta1 = new TH2F("Leading Theta", "First lepton Theta angle Distribution", 100, 0, 2, 200, 0, TMath::Pi())));
  TempList -> Add((TObject *)(   HTheta2 = new TH2F("Trailing Theta", "Second lepton Theta angle Distribution", 100, 0, 2, 200, 0, TMath::Pi())));
  TempList -> Add((TObject *)(HThetaFull = new TH2F("Dilepton Theta", "Dilepton Theta angle Distribution", 100, 0, 2, 200, 0, TMath::Pi())));
  TempList -> Add((TObject *)( HDeltaPhi = new TH2F("Dilepton DeltaPhi", "Dilepton Phi angle Distribution", 100, 0, 2, 200,
						                                                      -TMath::Pi(), TMath::Pi())));
  HTheta1 -> GetYaxis() -> SetTitle("#theta");
  HTheta2 -> GetYaxis() -> SetTitle("#theta");
  HThetaFull -> GetYaxis() -> SetTitle("#theta");
  HDeltaPhi -> GetYaxis() -> SetTitle("#DELTA #phi");

  TempList -> Add((TObject *)(    HEta1 = new TH2F("Leading Eta", "First lepton pseudorapidity Distribution", 100, 0, 2, 200, -3, 3)));
  TempList -> Add((TObject *)(    HEta2 = new TH2F("Trailing Eta", "Second lepton pseudorapidity Distribution", 100, 0, 2, 200, -3, 3)));
  TempList -> Add((TObject *)( HEtaFull = new TH2F("Dilepton Eta", "Dilepton pseudorapidity Distribution", 100, 0, 2, 200, -11,  11)));
  TempList -> Add((TObject *)(     HMet = new TH2F("Missing transverse", "Missing transverse energy Distribution", 100, 0, 2, 200, -0, 300))); 
  TempList -> Add((TObject *)(    HJets = new TH2F("Jet number", "Jet number Distribution", 100, 0, 2, 20, 0, 20))); 
  TempList -> Add((TObject *)(HVertexNo = new TH2F("Vertex count", "Vertex number", 100, 0, 2, 15, 0, 15))); 

  HEta1 -> GetYaxis() -> SetTitle("#eta");
  HEta2 -> GetYaxis() -> SetTitle("#eta");
  HEtaFull -> GetYaxis() -> SetTitle("#eta");
  HMet -> GetYaxis() -> SetTitle("Energy");
  HJets -> GetYaxis() -> SetTitle("Jet count");
  HVertexNo -> GetYaxis() -> SetTitle("Vertex count");

  for (Int_t i = 0; TempList -> At(i) != 0; i++)
  {
    ((TH2F *)TempList -> At(i)) -> GetXaxis() -> SetTitle("Instant Lumi (#frac{Hz}{#mu b})");
    ((TH2F *)TempList -> At(i)) -> SetFillColor(FGColor(ColorCount));
    ((TH2F *)TempList -> At(i)) -> Sumw2();
  }

  return kTRUE;
}

Double_t EfficiencyCorrection(PhysicsEvent_t *Event)
{
  return 1;
}


Bool_t FillHistograms(PhysicsEvent_t *Event, Float_t Weight, FGJob *Job)
{
  LorentzVector zll = Event -> leptons[0] + Event -> leptons[1];
  Double_t Momentum = zll.X()*zll.X() + zll.Y()*zll.Y() + zll.Z()*zll.Z();

  //if (Event -> Tag == 1) {
  Job -> Normalization = 1;
  Weight = 1;
  if (TMath::Sqrt(zll.T()*zll.T() - Momentum) > 76 &&
      TMath::Sqrt(zll.T()*zll.T() - Momentum) < 106) {
    HPT1 -> Fill(Event -> BXDelivered[0],
		 TMath::Sqrt(Event -> leptons[0].X() * Event -> leptons[0].X() + 
                             Event -> leptons[0].Y() * Event -> leptons[0].Y()), Weight * (Job -> Normalization));
    HPT2 -> Fill(Event -> BXDelivered[0],
		 TMath::Sqrt(Event -> leptons[1].X() * Event -> leptons[1].X() + 
                             Event -> leptons[1].Y() * Event -> leptons[1].Y()), Weight * (Job -> Normalization));

    HPTFull -> Fill(Event -> BXDelivered[0],
		    TMath::Sqrt(zll.X() * zll.X() + zll.Y() * zll.Y()), Weight * (Job -> Normalization));

    HDeltaPhi -> Fill(Event -> BXDelivered[0],
		      DeltaPhi(Event -> leptons[0].Phi(), Event -> leptons[1].Phi()), Weight * (Job -> Normalization));

    HEta1 -> Fill(Event -> BXDelivered[0], Event -> leptons[0].Eta(), Weight * (Job -> Normalization));
    HEta2 -> Fill(Event -> BXDelivered[0], Event -> leptons[1].Eta(), Weight * (Job -> Normalization));
    HEtaFull -> Fill(Event -> BXDelivered[0], zll.Eta(), Weight * (Job -> Normalization));

    HMet -> Fill(Event -> BXDelivered[0], Event -> met[0].T(), Weight * (Job -> Normalization));
    HJets -> Fill(Event -> BXDelivered[0], Event -> jets.size(), Weight * (Job -> Normalization));
    HVertexNo -> Fill(Event -> BXDelivered[0], Event -> VertexCount, Weight * (Job -> Normalization));

    HMomentum -> Fill(Event -> BXDelivered[0], TMath::Sqrt(Momentum), Weight * (Job -> Normalization));
    HRestMass -> Fill(Event -> BXDelivered[0], TMath::Sqrt(zll.T()*zll.T() - Momentum), Weight * (Job -> Normalization));
  
    HTheta1    -> Fill(Event -> BXDelivered[0], Event -> leptons[0].Theta(), Weight * (Job -> Normalization));
    HTheta2    -> Fill(Event -> BXDelivered[0], Event -> leptons[1].Theta(), Weight * (Job -> Normalization));
    HThetaFull -> Fill(Event -> BXDelivered[0], zll.Theta(), Weight * (Job -> Normalization));

    Job -> ContentSum +=  Weight * (Job->Normalization);
    if (!(Job -> isMC)) ParserEventAdd(Event, Job, EfficiencyCorrection(Event));
    }

  return kTRUE;
}

Bool_t SaveHistograms(FGJob *Job)
{
  TObjArray *HistogramStack = new TObjArray(TCollection::kInitCapacity, 0);

  HistogramStack -> Add(HPT1);
  HistogramStack -> Add(HPT2);
  HistogramStack -> Add(HPTFull);

  HistogramStack -> Add(HMomentum);
  HistogramStack -> Add(HRestMass);

  HistogramStack -> Add(HTheta1);
  HistogramStack -> Add(HTheta2);
  HistogramStack -> Add(HDeltaPhi);
  HistogramStack -> Add(HThetaFull);

  HistogramStack -> Add(HEta1);
  HistogramStack -> Add(HEta2);
  HistogramStack -> Add(HEtaFull);

  HistogramStack -> Add(HMet);
  HistogramStack -> Add(HJets);
  HistogramStack -> Add(HVertexNo);

  //HistogramStack -> Add(HTest);

  hOutputFile -> cd(OutputPath + ":/" + (Job -> FileName));
  //  cout << "Mi sposto nella cartella " << OutputPath + ":/" + (Job -> FileName) << "\n";
  
  HMomentum -> SetTitle(Job -> FileName);
  HRestMass -> SetTitle(Job -> FileName);

  HistogramStack -> Write();

  //for (Int_t i = 0; HistogramStack -> At(i) != 0; i++)
  //{
  TH1D *Projection = ((TH2F *)HistogramStack -> At(0)) -> ProjectionX("Projection");
  //((TH2F *)HistogramStack -> At(i)) -> GetName() + TString(" projection"));
    ((TH2F *)HistogramStack -> At(0)) -> GetYaxis() -> SetTitle("Event count");
    Projection -> Write();
    //}
  
  hOutputFile -> Flush();
//HistogramStack -> Write();

  return kTRUE;
}


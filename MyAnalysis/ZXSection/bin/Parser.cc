TString FGItoa(Int_t Valore)
{
  char Buffer[10];
  sprintf(Buffer, "%d", Valore);
  TString TempRes = TString(Buffer);
  return TempRes;
}

void LoadFamilyNames()
{
  char Buffer[512];
  TString *Fields[3];
  Int_t CurField, CurChar;
  Int_t FamilyId;
  Bool_t Quotes;
  
  for (Int_t i = 0; i < 20; i++)
  {
    FamilyNames[i] = new TString("");
    FamilyTitles[i] = new TString("");
  }

  FILE *hFile = fopen("test/ParsersLabels.txt", "r");
  if (feof(hFile)) cout << "Errore: apertura file parser.\n";
  
  while (!feof(hFile))
  {
    fgets(Buffer, 512, hFile);
    //cout << Buffer << "\n";
    if (Buffer[0] != '#')
    {
      for (Int_t i = 0; i < 3; i++) Fields[i] = new TString("");
      CurField = 0;
      CurChar = 0;
      Quotes = kFALSE;
    
      while (Buffer[CurChar] > 31)
      {
	if (Buffer[CurChar] == '\"') Quotes = !Quotes;
	else
	{
	  if (Buffer[CurChar] == ' ' && !Quotes)
            {if (CurField < 3) CurField++;}
	  else Fields[CurField] -> Append(Buffer[CurChar]); 
	}
	CurChar++;
      }
      
      if (Fields[0] -> IsDigit())
      {
	FamilyId = Fields[0] -> Atoi();
	FamilyNames[FamilyId] = Fields[1];
	FamilyTitles[FamilyId] = Fields[2];
	cout << FamilyId << " " << *FamilyNames[FamilyId] << " - " << *FamilyTitles[FamilyId] << "\n";
      }
    } 
  }
  fclose(hFile);
}

void SetupParsers()
{
  for (Int_t i = 0; i < MaxParsers; i++)
  {
    Parsers[i].RecordedLumi = 0;
    Parsers[i].DeliveredLumi = 0;
    Parsers[i].EventCount = 0;
    Parsers[i].LumiSecCount = 0;
    Parsers[i].StackId = 0;
    Parsers[i].Sumw2 = 0;
    Parsers[i].isAlive = kFALSE;
  }
}

Bool_t ParsersLumiAdd(Int_t StackID, Int_t Run, FGLumiEntry *Lumi, FGBunch *Bunch)
{
  //Riscrivere
  
  //if (Run > 162712) return kTRUE;
  //if (Run == 163334 && Lumi->Lumi == 1)
      //cout << "Parserlumiadd: " << Run << " " << Lumi -> Lumi << " " << Bunch -> Id << " " << Bunch -> Lumi << "\n";
  for (Int_t i = 0; i < ParserNo; i++)
    if (
	(Parsers[i].StackId == StackID) &&

	((!Parsers[i].CutOnBXLumi) || 
	 (Parsers[i].LowBXLumi < Bunch -> Lumi && Parsers[i].HiBXLumi > Bunch -> Lumi)) &&

	((!Parsers[i].CutOnRunLumi) || 
	 (Parsers[i].LowRun <= Run && Run <= Parsers[i].HiRun)) &&

	((!Parsers[i].LocomotiveOnly) || Bunch -> isLocomotive)
	)
    {
      //cout << "Aggiunta luminosità [" << i << "]: " << Bunch -> Lumi << "\n";

      //cout << Parsers[i].DeliveredLumi<< "\n";
      if (Lumi -> Delivered > 0)
      {
	Parsers[i].DeliveredLumi += Bunch -> Lumi;
	//cout << Parsers[i].DeliveredLumi<< "\n";

	Parsers[i].RecordedLumi += (Lumi -> Recorded) / (Lumi -> Delivered) * Bunch -> Lumi;
	Parsers[i].Sumw2 += Bunch -> Lumi * Bunch -> Lumi;
	Parsers[i].LumiSecCount++;
      }
    };

  return kTRUE;
}

void ParserEventAdd(PhysicsEvent_t *Evento, FGJob *Job, Double_t Weight) //Int_t Run, Int_t Lumi, Float_t Delivered[2], Float_t Recorded[2])
{
  // Riscrivere

  //if (Evento -> Run > 162712) return;
  for (Int_t i = 0; i < ParserNo; i++)
  {
    if (
	((!Parsers[i].CutOnBXLumi) || 
	 (Parsers[i].LowBXLumi < Evento -> BXDelivered[Parsers[i].StackId] &&
	   Parsers[i].HiBXLumi > Evento -> BXDelivered[Parsers[i].StackId])) &&

	 ((!Parsers[i].CutOnRunLumi) || 
	  (Parsers[i].LowRun <= Evento -> Run && Evento -> Run <= Parsers[i].HiRun)) &&

	((!Parsers[i].LocomotiveOnly) || Evento -> isLocomotive[Parsers[i].StackId])
	)
      if (PartOfIntList(Parsers[i].Dataset, Job -> Dataset)) Parsers[i].EventCount += Weight;
  }
}

void ComputeParserCoords()
{
  for (Int_t i = 0; i < ParserNo; i++)
  {
    Parsers[i].isAlive = Parsers[i].LumiSecCount != 0;
    if (Parsers[i].isAlive)
    {
      Parsers[i].X = Parsers[i].DeliveredLumi / Parsers[i].LumiSecCount;
      Parsers[i].ErrX = Parsers[i].Sumw2 + Parsers[i].DeliveredLumi * Parsers[i].DeliveredLumi - 2 * Parsers[i].DeliveredLumi * Parsers[i].Sumw2;
      Parsers[i].ErrX = 0; //TMath::Sqrt(Parsers[i].ErrX / Parsers[i].LumiSecCount);
      Parsers[i].Y = Parsers[i].EventCount / Parsers[i].RecordedLumi / 23;
      Parsers[i].ErrY = TMath::Sqrt(Parsers[i].EventCount) / Parsers[i].DeliveredLumi / 23 + 0.025 * Parsers[i].Y;
    }
  }
}

/*
void ParserPrint()
{
  cout << "\n";
  for (Int_t i = 0; i < ParserNo; i++)
  {
    cout << "Parser #" << i << "\n";
    cout << Parsers[i].X << " " << Parsers[i].Y << " " << Parsers[i].ErrX << " " << Parsers[i].ErrY << "\n";
    cout << Parsers[i].LBound << " " << Parsers[i].UBound << "\n ";
    cout << Parsers[i].EventCount << " " << Parsers[i].DeliveredLumi << " " << Parsers[i].RecordedLumi << "\n";
  }
  }*/

Int_t FindNextFamily(Int_t FamilyId)
{
  Int_t BestResult = -1;
  cout << "Ricerca famiglia partendo da " << FamilyId << " ";

  for (Int_t i = 0; i < ParserNo; i++)
  {
    //cout << i << "/" << ParserNo << " " << Parsers[i].isAlive << " " << Parsers[i].Family << " " << BestResult << "\n";
    if (Parsers[i].isAlive)
    {
      if (Parsers[i].Family > FamilyId && (BestResult == -1 || BestResult > Parsers[i].Family))
	BestResult = Parsers[i].Family;
    }
}

  cout << BestResult << "\n";
  return BestResult;
}

Int_t CountParserFamily(Int_t FamilyId)
{
  Int_t Count = 0;

  for (Int_t i = 0; i < ParserNo; i++)
    if (Parsers[i].isAlive && Parsers[i].Family == FamilyId) Count++;

  return Count;
}

void ExportParsers()
{
  hOutputFile -> cd(OutputPath + ":/");
  TGraphErrors *TempGraphs[40];

  Int_t CurFamily = FindNextFamily(-1);
  //cout << "PrimaFamigliaTrovata: " << CurFamily << "\n";
  while (CurFamily > -1)
  {
    cout << "Esportazione famiglia #" << CurFamily << "\n";
    Int_t PointCount = CountParserFamily(CurFamily);
    TempGraphs[CurFamily] = new TGraphErrors(PointCount);
    TCanvas *TempCanv = new TCanvas(FamilyNames[CurFamily] -> Data(), FamilyTitles[CurFamily] -> Data(), 550, 400);

    Int_t PointId = 0;
    for (Int_t i = 0; i < ParserNo; i++)
    {
      if (Parsers[i].isAlive && Parsers[i].Family == CurFamily)
      {
	TempGraphs[CurFamily] -> SetPoint(PointId, Parsers[i].X, Parsers[i].Y);
	TempGraphs[CurFamily] -> SetPointError(PointId, Parsers[i].ErrX, Parsers[i].ErrY); 
	cout << "Point set: " << PointId << " " << Parsers[i].X << " " << Parsers[i].Y << " " << Parsers[i].ErrX << " " << Parsers[i].ErrY << "\n";
	PointId++;
      }
    }

    TempGraphs[CurFamily] -> SetMarkerColor(FGColor(CurFamily));
    TempGraphs[CurFamily] -> GetXaxis() -> SetTitle("Instant lumi (Hz / #mu b)");
    TempGraphs[CurFamily] -> GetYaxis() -> SetTitle("#sigma (#mu b)");
    // TempGraph -> GetYaxis() -> SetLimits(0, .0005);

    TempGraphs[CurFamily] -> Draw("A*E1");
    TempGraphs[CurFamily] -> Fit("pol1");
    TempCanv -> Write();

    /*
    /////////////////////////////////
    // Esportiamo anche il conteggio

    TempGraphs[CurFamily] = new TGraphErrors(PointCount);
    TempCanv = new TCanvas(FamilyNames[CurFamily] -> Data() + TString("Event count"), 
			   FamilyTitles[CurFamily] -> Data() + TString("Event count"), 550, 400);

    PointId = 0;
    for (Int_t i = 0; i < ParserNo; i++)
    {
      if (Parsers[i].isAlive && Parsers[i].Family == CurFamily)
      {
	TempGraphs[CurFamily] -> SetPoint(PointId, i, Parsers[i].EventCount);
	TempGraphs[CurFamily] -> SetPointError(PointId, Parsers[i].ErrX, Parsers[i].ErrY); 
	cout << "Point set: " << PointId << " " << Parsers[i].X << " " << Parsers[i].Y << " " << Parsers[i].ErrX << " " << Parsers[i].ErrY << "\n";
	PointId++;
      }
    }

    TempGraphs[CurFamily] -> SetMarkerColor(FGColor(CurFamily));
    TempGraphs[CurFamily] -> GetXaxis() -> SetTitle("Instant lumi (Hz / #mu b)");
    TempGraphs[CurFamily] -> GetYaxis() -> SetTitle("Numero di eventi");
    // TempGraph -> GetYaxis() -> SetLimits(0, .0005);

    TempGraphs[CurFamily] -> Draw("A*E1");
    TempGraphs[CurFamily] -> Fit("pol1");
    TempCanv -> Write();

    /////////////////////////////////
    // Esportiamo la lumi recorded

    TempGraphs[CurFamily] = new TGraphErrors(PointCount);
    TempCanv = new TCanvas(FamilyNames[CurFamily] -> Data() + TString("Recorded Lumi"),
			   FamilyTitles[CurFamily] -> Data() + TString("Recorded Lumi"), 550, 400);

    PointId = 0;
    for (Int_t i = 0; i < ParserNo; i++)
    {
      if (Parsers[i].isAlive && Parsers[i].Family == CurFamily)
      {
	TempGraphs[CurFamily] -> SetPoint(PointId, i, Parsers[i].RecordedLumi);
	TempGraphs[CurFamily] -> SetPointError(PointId, Parsers[i].ErrX, Parsers[i].ErrY); 
	cout << "Point set: " << PointId << " " << Parsers[i].X << " " << Parsers[i].Y << " " << Parsers[i].ErrX << " " << Parsers[i].ErrY << "\n";
	PointId++;
      }
    }

    TempGraphs[CurFamily] -> SetMarkerColor(FGColor(CurFamily));
    TempGraphs[CurFamily] -> GetXaxis() -> SetTitle("Instant lumi (Hz / #mu b)");
    TempGraphs[CurFamily] -> GetYaxis() -> SetTitle("Numero di eventi");
    // TempGraph -> GetYaxis() -> SetLimits(0, .0005);

    TempGraphs[CurFamily] -> Draw("A*E1");
    TempGraphs[CurFamily] -> Fit("pol1");
    TempCanv -> Write();*/

    CurFamily = FindNextFamily(CurFamily);
  }

  /*
  //Temporaneo, sistemare.
  TCanvas *TempCanv = new TCanvas("Compare Lumi1", "Lumi 1 data comparison", 550, 400);
  TempGraphs[3] -> Draw("A*E1");
  TempGraphs[5] -> Draw("SAME*E1");
  TempGraphs[7] -> Draw("SAME*E1");
  TempGraphs[9] -> Draw("SAME*E1");
  TempGraphs[11] -> Draw("SAME*E1");
  TempGraphs[13] -> Draw("SAME*E1");
  TempGraphs[15] -> Draw("SAME*E1");
  TempGraphs[17] -> Draw("SAME*E1");
  TempCanv -> Write();

  TempCanv = new TCanvas("Compare Lumi2", "Lumi 2 data comparison", 550, 400);
  TempGraphs[4] -> Draw("A*E1");
  TempGraphs[6] -> Draw("SAME*E1");
  TempGraphs[8] -> Draw("SAME*E1");
  TempGraphs[10] -> Draw("SAME*E1");
  TempGraphs[12] -> Draw("SAME*E1");
  TempGraphs[14] -> Draw("SAME*E1");
  TempGraphs[16] -> Draw("SAME*E1");
  TempGraphs[18] -> Draw("SAME*E1");
  TempCanv -> Write();

  TempCanv = new TCanvas("Compare Lumis", "Lumi 1 and 2 data comparison", 550, 400);
  TempGraphs[1] -> Draw("A*E1");
  TempGraphs[2] -> Draw("SAME*E1");
  TempCanv -> Write();*/

}

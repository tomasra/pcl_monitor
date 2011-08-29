#define MaxParsers 2000
Int_t ParserNo = 0;

struct FGParser
{
  Double_t UBound;
  Double_t LBound;
  Double_t RecordedLumi;
  Double_t DeliveredLumi;

  Int_t EventCount;
  Int_t LumiSecCount;
  Int_t StackId;
  Int_t Family;
  Int_t Dataset;

  Bool_t isAlive;
  Double_t X, Y;
  Double_t ErrX, ErrY;
  Double_t Sumw2;
};

FGParser Parsers[MaxParsers];
TString *FamilyNames[40];
TString *FamilyTitles[40];

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
    cout << Buffer << "\n";
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
      }
    } 
  }
  fclose(hFile);
}

void SetupParsers();

void LoadParsers()
{
  FILE *hFile = fopen("test/Parsers.txt", "r");
  char Buffer[512];
  TString *Fields[6];
  Int_t CurField, CurChar;
  
  SetupParsers();
  LoadFamilyNames();
  if (feof(hFile)) cout << "Errore: apertura file parser.\n";
  ParserNo = -1;
  while (!feof(hFile))
  {
    fgets(Buffer, 512, hFile);
    cout << Buffer << "\n";
    if (Buffer[0] != '#')
    {
      for (Int_t i = 0; i < 6; i++) Fields[i] = new TString("");
      CurField = 0;
      CurChar = 0;
    
      while (Buffer[CurChar] > 31)
      {
	if (Buffer[CurChar] == ' ')
          {if (CurField < 5) CurField++;}
	else Fields[CurField] -> Append(Buffer[CurChar]); 
	CurChar++;
      }
      
      cout << *Fields[0] << "\n";
      cout << *Fields[1] << "\n";
      cout << *Fields[2] << "\n";
      cout << *Fields[3] << "\n";
      cout << *Fields[4] << "\n\n";
      if (Fields[0] -> IsDigit() && Fields[1] -> IsDigit() && Fields[2] -> IsFloat() &&
          Fields[3] -> IsFloat() && Fields[4] -> IsDigit())
      {
	ParserNo++;
	Parsers[ParserNo].Family = Fields[0] -> Atoi();
	Parsers[ParserNo].StackId = Fields[1] -> Atoi();
	Parsers[ParserNo].LBound = Fields[2] -> Atof();
	Parsers[ParserNo].UBound = Fields[3] -> Atof();
	Parsers[ParserNo].Dataset = Fields[4] -> Atoi();
	cout << Parsers[ParserNo].Family << " "<< Parsers[ParserNo].StackId << " "
             << Parsers[ParserNo].LBound << " "<< Parsers[ParserNo].UBound << " "<< Parsers[ParserNo].Dataset << "\n";
      }
    } 
  }

  ParserNo++;
  cout << "Numero parser:" << ParserNo << "\n";
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

void ParsersLumiAdd(Int_t StackId, Int_t Run, Int_t Lumi, Double_t Delivered, Double_t Recorded)
{
  for (Int_t i = 0; i < ParserNo; i++)
  {
    if (Parsers[i].LBound < Delivered && Parsers[i].UBound > Delivered && Parsers[i].StackId == StackId)
    {
      Parsers[i].DeliveredLumi += Delivered;
      Parsers[i].RecordedLumi += Recorded;
      Parsers[i].Sumw2 += Delivered * Delivered;
      Parsers[i].LumiSecCount++;
    }
  }
}

void ParserEventAdd(PhysicsEvent_t *Evento, FGJob *Job) //Int_t Run, Int_t Lumi, Float_t Delivered[2], Float_t Recorded[2])
{
  for (Int_t i = 0; i < ParserNo; i++)
    if (Parsers[i].LBound < Evento -> Delivered[Parsers[i].StackId] &&
	Parsers[i].UBound > Evento -> Delivered[Parsers[i].StackId] &&
	Job -> Dataset == Parsers[i].Dataset)
      Parsers[i].EventCount++;
}

void ComputeParserCoords()
{
  for (Int_t i = 0; i < ParserNo; i++)
  {
    Parsers[i].isAlive = Parsers[i].LumiSecCount != 0;
    if (Parsers[i].isAlive)
    {
      Parsers[i].X = Parsers[i].DeliveredLumi / Parsers[i].LumiSecCount / 23;
      Parsers[i].ErrX = Parsers[i].Sumw2 + Parsers[i].DeliveredLumi * Parsers[i].DeliveredLumi - 2 * Parsers[i].DeliveredLumi * Parsers[i].Sumw2;
      Parsers[i].ErrX = TMath::Sqrt(Parsers[i].ErrX / Parsers[i].LumiSecCount) / 23;
      Parsers[i].Y = Parsers[i].EventCount / Parsers[i].RecordedLumi;
      Parsers[i].ErrY = TMath::Sqrt(Parsers[i].EventCount) / Parsers[i].DeliveredLumi + 0.025 * Parsers[i].Y;
    }
  }
}

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
}

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

  Int_t CurFamily = FindNextFamily(-1);
  //cout << "PrimaFamigliaTrovata: " << CurFamily << "\n";
  while (CurFamily > -1)
  {
    Int_t PointCount = CountParserFamily(CurFamily);
    TGraphErrors *TempGraph = new TGraphErrors(PointCount);
    TCanvas *TempCanv = new TCanvas(FamilyNames[CurFamily] -> Data(), FamilyTitles[CurFamily] -> Data(), 550, 400);

    Int_t PointId = 0;
    for (Int_t i = 0; i < ParserNo; i++)
    {
      if (Parsers[i].isAlive && Parsers[i].Family == CurFamily)
      {
	TempGraph -> SetPoint(PointId, Parsers[i].X, Parsers[i].Y);
	TempGraph -> SetPointError(PointId, Parsers[i].ErrX, Parsers[i].ErrY); 
	cout << "Point set: " << PointId << " " << Parsers[i].X << " " << Parsers[i].Y << " " << Parsers[i].ErrX << " " << Parsers[i].ErrY << "\n";
	PointId++;
      }
    }

    TempGraph -> GetXaxis() -> SetTitle("Instant lumi (Hz / #mu b)");
    TempGraph -> GetYaxis() -> SetTitle("#sigma (1 / #mu b)");
    // TempGraph -> GetYaxis() -> SetLimits(0, .0005);

    TempGraph -> Draw("A*E1");
    TempGraph -> Fit("pol1");
    TempCanv -> Write();
    CurFamily = FindNextFamily(CurFamily);
  }
}

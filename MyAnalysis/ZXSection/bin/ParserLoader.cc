void LoadParsers()
{
  FILE *hFile = fopen("test/Parsers.txt", "r");
  TString Buffer;
  char InBuffer;
  //  FGParserConstructor *Costruttori;

  ParserNo = -1;
  if (feof(hFile)) cout << "Errore: apertura file parser.\n";
  ParserNo = -1;
  while (!feof(hFile))
  {
    InBuffer = fgetc(hFile);
    if (InBuffer > 31) Buffer.Append(InBuffer);
  }

  cout << "Buffer letto: " << Buffer << "\n";

  FGStringList *Righe = CharSplit(&Buffer, ';');
  FGStringList *Hook = Righe;

  while (Hook != 0)
  {    
    if (Hook -> Value.Length() > 0 && (!Hook -> Value.BeginsWith("#")))
    {
      cout << "Riga: " << Hook -> Value << "\n";
      FGStringList *Campi = CharSplit(&(Hook -> Value), ' ');

      if (StringListCount(&Campi) > 9)
      {
	ParserNo++;
	FGStringList *CHook = Campi;
	FGStringList *Datasets;
	
	Parsers[ParserNo].Family = CHook -> Value.Atoi();
	//cout << "Campo: " << CHook -> Value << " - " << Parsers[ParserNo].Family << " - " << ParserNo <<"\n";
	CHook = CHook -> Next;
	Parsers[ParserNo].StackId = CHook -> Value.Atoi();
	//cout << "Campo: " << CHook -> Value << "\n";
	CHook = CHook -> Next;

	Datasets = CharSplit(&(CHook -> Value), ',');
	Parsers[ParserNo].Dataset = StringListToIntList(Datasets); 
	StringListEmpty(&Datasets);
	//cout << "Campo: " << CHook -> Value << "\n";
	CHook = CHook -> Next;

	Parsers[ParserNo].CutOnBXLumi = !(CHook -> Value.BeginsWith("F") || CHook -> Value.BeginsWith("f"));
	CHook = CHook -> Next;
	Parsers[ParserNo].LowBXLumi = CHook -> Value.Atof();
	CHook = CHook -> Next;
	Parsers[ParserNo].HiBXLumi = CHook -> Value.Atof();
	CHook = CHook -> Next;

	Parsers[ParserNo].CutOnRunLumi = !(CHook -> Value.BeginsWith("F") || CHook -> Value.BeginsWith("f"));
	CHook = CHook -> Next;
	Parsers[ParserNo].LowRun = CHook -> Value.Atof();
	CHook = CHook -> Next;
	Parsers[ParserNo].HiRun = CHook -> Value.Atof();
	CHook = CHook -> Next;

	Parsers[ParserNo].LocomotiveOnly = !(CHook -> Value.BeginsWith("F") || CHook -> Value.BeginsWith("f"));

	Parsers[ParserNo].EventCount = 0;
	Parsers[ParserNo].LumiSecCount = 0;
	Parsers[ParserNo].Sumw2 = 0;

	Parsers[ParserNo].DeliveredLumi = 0;
	Parsers[ParserNo].RecordedLumi = 0;
	Parsers[ParserNo].isAlive = kFALSE;

	for (Int_t i = 0; i < 14; i++)
	{
	  ParserNo++;
	  Parsers[ParserNo] = Parsers[ParserNo - 1];
	  Parsers[ParserNo].LowBXLumi = Parsers[ParserNo].HiBXLumi;
	  Parsers[ParserNo].HiBXLumi =  Parsers[ParserNo].LowBXLumi + Parsers[ParserNo - 1].HiBXLumi - Parsers[ParserNo - 1].LowBXLumi;
	  }
      } else cout << "Campi insufficenti per caricare il parser.\n";
      StringListEmpty(&Campi);
    }
    Hook = Hook -> Next;
  }
  StringListEmpty(&Righe);
  ParserNo++;
}

void PrintParsers()
{
  for (Int_t i = 0; i < ParserNo; i++)
  {
    cout << "\n\nId: " << i;
    cout << "\nFamiglia: " << Parsers[i].Family;
    cout << "\nStackId: " << Parsers[i].StackId;
    cout << "\nDatasets: ";
    PrintIntList(Parsers[i].Dataset);

    cout << "\nCutOnBxLumi: " << Parsers[i].CutOnBXLumi;
    cout << "\nLowBxLumi: " << Parsers[i].LowBXLumi;
    cout << "\nHiBxLumi: " << Parsers[i].HiBXLumi;

    cout << "\nCutOnRunLumi: " << Parsers[i].CutOnRunLumi;
    cout << "\nLowRun: " << Parsers[i].LowRun;
    cout << "\nHiRun: " << Parsers[i].HiRun;
    
    cout << "\nLocomotiveOnly: " << Parsers[i].LocomotiveOnly;
    cout << "\nEventCount: " << Parsers[i].EventCount;
    cout << "\nSumw2: " << Parsers[i].Sumw2;
    cout << "\nLumiSecCount: " << Parsers[i].LumiSecCount;

    cout << "\nDeliveredLumi: " << Parsers[i].DeliveredLumi;
    cout << "\nRecordedLumi: " << Parsers[i].RecordedLumi;
    cout << "\nisAlive: " << Parsers[i].isAlive;

    cout << "\nX: " << Parsers[i].X;
    cout << "\nY: " << Parsers[i].Y;
    cout << "\nErrX: " << Parsers[i].ErrX;
    cout << "\nErrY: " << Parsers[i].ErrY << "\n";
  }
}

/*void LoadParsers()
{
  FILE *hFile = fopen("test/Parsers.txt", "r");
  TString Buffer;
  char InBuffer;
  FGParserConstructor *Costruttori;

  LoadFamilyNames();
  if (feof(hFile)) cout << "Errore: apertura file parser.\n";
  ParserNo = -1;
  while (!feof(hFile))
  {
    InBuffer = fgetc(hFile);
    Buffer.Append(InBuffer);
  }

  Costruttori = ProcessParserString(&Buffer);
}

FGParserConstructor *ProcessParserString(TString *Buffer)
{
  FGParserConstructor *Lista = 0;
  FGStringList *Righe = CharSplitNoParent(Buffer, ';');
  FGStringList *Hook = Righe;

  while (Hook != 0)
  {
    Int_t ParNo = 0;
    char CurChar;
    Int_t SecNo = 0;
    TString Sections[2];

    for (Int_t i = 0; i < Hook -> Value.Length(); i++)
    {
      CurChar = Hook -> Value.Data()[i];
      if (CurChar == '(') ParNo++;
      else
      {
        if (CurChar == ')')
	{
	  ParNo--;
	  if (ParNo == 0 && SecNo == 0) SecNo++;
	}
	else Sections[SecNo].Append(CurChar); 
      }
    }
    
    FGStringList *Campi = CharSplit(Sections[0], '=');
    if (Campi == 0 || Campi -> Next == 0) cout << "Errore, carattere di uguaglianza multiplo";
    else 
    {
      Int_t Flag;
      FGParserConstructor *Lista = 0;

      Lista = 

      Flag = strcmp(open, Campi -> Value.Data());
      switch Campi -> Value.Data()
      {
        case "family": 
if (flag == 0) cout<<"its locked"<<endl;
break;
case "closedoor":
if (flag == 0) cout<<"its already closed"<<endl;
break;
case "backward":
if (flag == 0) lvl3();
break;
}
    }
    Hook = Hook -> Next;
  } 
}

void LoadParsers()
{
  FILE *hFile = fopen("test/Parsers.txt", "r");
  char Buffer[512];
  TString *Fields[MaxDatasets + 6];
  Int_t CurField, CurChar;
  
  SetupParsers();
  LoadFamilyNames();
  if (feof(hFile)) cout << "Errore: apertura file parser.\n";
  ParserNo = -1;
  while (!feof(hFile))
  {
    fgets(Buffer, 512, hFile);
    //cout << Buffer << "\n";
    if (Buffer[0] != '#')
    {
      for (Int_t i = 0; i < (MaxDatasets + 6); i++) Fields[i] = new TString("");
      CurField = 0;
      CurChar = 0;
    
      while (Buffer[CurChar] > 31)
      {
	if (Buffer[CurChar] == ' ')
          {if (CurField < MaxDatasets + 5) CurField++;}
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
        for (Int_t i = 0; i < MaxDatasets; i++) Parsers[ParserNo].Dataset[i] = -1;
	for (Int_t i = 4; i <= CurField; i++) if (Fields[i] -> IsDigit()) Parsers[ParserNo].Dataset[i - 4] = Fields[i] -> Atoi();	

	//cout << Parsers[ParserNo].Family << " "<< Parsers[ParserNo].StackId << " "
             //<< Parsers[ParserNo].LBound << " "<< Parsers[ParserNo].UBound << " "<< Parsers[ParserNo].Dataset << "\n";
      }
    } 
  }

  ParserNo++;
  cout << "Numero parser:" << ParserNo << "\n";
  fclose(hFile);
}*/

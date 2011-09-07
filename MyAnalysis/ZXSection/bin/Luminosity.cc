
FGLumiEntry *GetLuminosity(Int_t StackID, Int_t Run, Int_t Lumi)
{
  FGLumiRun *Hook;
  FGLumiEntry *EntryHook;

  Hook = LumiDB[StackID].LumiDB;
  while (Hook != 0 && Hook -> Run < Run) Hook = Hook -> Next;
  if (Hook == 0 || Hook -> Run != Run) return 0;

  EntryHook = Hook -> Chain;
  while (EntryHook != 0 && EntryHook -> Lumi < Lumi) EntryHook = EntryHook -> Next;
  if (EntryHook == 0 || EntryHook -> Lumi != Lumi) return 0;

  return EntryHook;
}

void InitializeLumiDB(FGLumiDB *DB)
{
  DB -> LumiDB = 0;
}

Float_t GetBXLuminosity2(Int_t StackID, Int_t Run, Int_t Lumi, Int_t BX)
{
  FGLumiEntry *LumiEntry;
  TString fPath;
  char Buffer[10];

  LumiEntry = GetLuminosity(StackID, Run, Lumi);
  
  if (LumiEntry == 0)
  {
    // cout << "Lumi entry non trovata.\n";
    return -1;
  }

  if (StackID == 0) fPath = TString("/data/fguatier/LumiCalcDB_Bin/" + FGItoa(Run) + "/" + FGItoa(LumiEntry -> Lumi) + ".txt");
  else fPath = TString("/data/fguatier/LumiCalc2DB_Bin/" + FGItoa(Run) + "/" + FGItoa(LumiEntry -> Lumi) + ".txt");
   
  ifstream hFile;
  hFile.open (fPath.Data(), ios::in | ios::binary);

  if (!hFile.is_open()) 
  {
    cout << "\"" << fPath << "\" - " << fPath.Length() << "\n";
    cout << strerror(errno) << "\n";
    cout << "Errore: Lumifile non trovato.\n";
    cout << fPath << "\n";
    return -20;
  }
  //else cout << "File aperto con successo.\n";
  
  while (!(hFile.eof()))
  {
    hFile.read(Buffer, 6);
    
    FGBunch TempBunch;
    TempBunch.Id = *((Short_t *)(&Buffer[0]));
    TempBunch.Lumi = *((Float_t *)(&Buffer[2]));
    if (TempBunch.Id == BX)
    {
      hFile.close();
      //cout << "Luminosity fetch: " << Run << " " << Lumi << " " << BX << " -> " << TempBunch.Lumi << "\n";
      return TempBunch.Lumi;
    }
  }

  hFile.close();
  return -1;
}

Float_t LumiEntryToParsers2(Int_t StackID, Int_t Run, FGLumiEntry *LumiEntry)
{
  Float_t Sum = 0;
  TString fPath;
  char Buffer[20];
  Short_t PrevId = -1000;

  if (StackID == 0) fPath = TString("/data/fguatier/LumiCalcDB_Bin/" + FGItoa(Run) + "/" + FGItoa(LumiEntry -> Lumi) + ".txt");
  else fPath = TString("/data/fguatier/LumiCalc2DB_Bin/" + FGItoa(Run) + "/" + FGItoa(LumiEntry -> Lumi) + ".txt");
   
  ifstream hFile;
  hFile.open (fPath.Data(), ios::in | ios::binary);

  if (!hFile.is_open()) 
  {
    cout << "\"" << fPath << "\" - " << fPath.Length() << "\n";
    cout << strerror(errno) << "\n";
    cout << "Errore: Lumifile non trovato.\n";
    cout << fPath << "\n";
    return -20;
  }
  //else cout << "File aperto con successo.\n";
  
  while (!(hFile.eof()))
  {
    hFile.read(Buffer, 6);
    
    FGBunch TempBunch;
    TempBunch.Id = *((Short_t *)(&Buffer[0]));
    if (PrevId + 30 < TempBunch.Id)
    {
	IntListAdd(&(LumiEntry -> Locomotive), TempBunch.Id);
	TempBunch.isLocomotive = kTRUE;
    } else TempBunch.isLocomotive = kFALSE;
    PrevId = TempBunch.Id;
    TempBunch.Lumi = *((Float_t *)(&Buffer[2]));
    Sum += TempBunch.Lumi;
    ParsersLumiAdd(StackID, Run, LumiEntry, &TempBunch);

    //cout << "Aggiunto BX: " << Run << " " << LumiEntry -> Lumi << " " << TempBunch.Id << " " << TempBunch.Lumi << "\n";
  }

  hFile.close();
  return Sum;
}

/*Float_t GetBXLuminosity(Int_t StackID, Int_t Run, Int_t Lumi, Int_t BX)
{
  cout << "Attenzione, chiamata a funzione obsoleta.\n";

  FGLumiEntry *LumiEntry;
  TString fPath;

  LumiEntry = GetLuminosity(StackID, Run, Lumi);
  if (LumiEntry == 0)
  {
    cout << "Lumi entry non trovata" << Run << " " << Lumi << " " << BX << "\n";
    return -2;
  }

  if (StackID == 0) fPath = TString("/data/fguatier/LumiCalcDB/" + FGItoa(Run) + "_" + FGItoa(LumiEntry -> Lumi) + ".txt");
  else fPath = TString("/data/fguatier/LumiCalc2DB/" + FGItoa(Run) + "_" + FGItoa(LumiEntry -> Lumi) + ".txt");
   
  FILE *hFile = fopen(fPath.Data(), "r");

  if (hFile == 0) 
  {
    cout << "\"" << fPath << "\" - " << fPath.Length() << "\n";
    cout << strerror(errno) << "\n";
    cout << "Errore: Lumifile non trovato.\n";
    cout << fPath << "\n";
    return -20;
  }
  //else cout << "Lumifile trovato!\n";

  char Buffer[512];

  while (!feof(hFile))
  {
    fgets (Buffer, 512, hFile);
    TString TSBuffer = TString(Buffer);
    FGStringList *Campi = CharSplit(&TSBuffer, ' ');

    if (Campi == 0 || Campi -> Next == 0)
    {
      //cout << "Riga database non valida, \"" << TSBuffer << " \"\n";
    }
    else
    {
      if (!Campi -> Value.IsDigit()) cout << "Numero bunch non valido.\n";
      else
      {
        if (!Campi -> Next -> Value.IsFloat()) cout << "Lumi bunch non valida.\n";
        else
        {
	  if (Campi -> Value.Atoi() == BX) 
	  {
	    Float_t TempRes = Campi -> Next -> Value.Atof();
	    StringListEmpty(&Campi);
	    fclose(hFile);
	    return TempRes;
	  }
        }
      }
    }
    StringListEmpty(&Campi);
  }

  fclose(hFile);
  cout << "Bunch non trovato," << Run << " " << Lumi << " " << BX << "\n";
  return -1;
  }*/

/*Float_t LumiEntryToParsers(Int_t StackID, Int_t Run, FGLumiEntry *LumiEntry)
{
  cout << "Attenzione, chiamata a funzione obsoleta.\n";

  Float_t Sum = 0;
  TString fPath;
  char Buffer[512];
  Short_t PrevId = -1000;

  if (StackID == 0) fPath = TString("/data/fguatier/LumiCalcDB/" + FGItoa(Run) + "_" + FGItoa(LumiEntry -> Lumi) + ".txt");
  else fPath = TString("/data/fguatier/LumiCalc2DB/" + FGItoa(Run) + "_" + FGItoa(LumiEntry -> Lumi) + ".txt");
   
  FILE *hFile = fopen(fPath.Data(), "r");

  if (hFile == 0) 
  {
    cout << "\"" << fPath << "\" - " << fPath.Length() << "\n";
    cout << strerror(errno) << "\n";
    cout << "Errore: Lumifile non trovato.\n";
    cout << fPath << "\n";
    return -20;
  }
  else cout << "File aperto con successo.\n";
  
  while (!feof(hFile))
  {
    fgets (Buffer, 512, hFile);
    TString TSBuffer = TString(Buffer);
    FGStringList *Campi = CharSplit(&TSBuffer, ' ');

    if (Campi == 0 || Campi -> Next == 0)
    {
      cout << "Riga database non valida.\n";
    }
    else
    {
      if (!Campi -> Value.IsDigit()) cout << "Numero bunch non valido.\n";
      else
      {
        if (!Campi -> Next -> Value.IsFloat()) cout << "Lumi bunch non valida.\n";
        else
        {
	  FGBunch TempBunch;

	  TempBunch.Id = Campi -> Value.Atoi();
	  if (PrevId + 30 < TempBunch.Id) IntListAdd(&(LumiEntry -> Locomotive), TempBunch.Id);
	  PrevId = TempBunch.Id;
	  TempBunch.Lumi = Campi -> Next -> Value.Atof();
	  Sum += TempBunch.Lumi;
	  ParsersLumiAdd(StackID, Run, LumiEntry, &TempBunch);
        }
      }
    }
    StringListEmpty(&Campi);
    }

  fclose(hFile);
  return Sum;
  }*/

FGLumiEntry *AddLumiEntry(Int_t StackID, Int_t Run, Int_t Lumi, Float_t Delivered, Float_t Recorded)//, Int_t FirstBX, Int_t BXCount)
{
  FGLumiRun **Hook;
  FGLumiEntry **EntryHook;

  Hook = &(LumiDB[StackID].LumiDB);
  while (*Hook != 0 && (**Hook).Run < Run) Hook = &((**Hook).Next);
    
  if (*Hook == 0 || (**Hook).Run != Run) //Se non trova la run entry
  {
    FGLumiRun *TempLumiRun = new FGLumiRun;
    
    TempLumiRun -> Next = *Hook;
    TempLumiRun -> Run = Run;
    TempLumiRun -> Chain = 0;
    (*Hook) = TempLumiRun;
    EntryHook = &(TempLumiRun -> Chain);
  } 
  else EntryHook = &((**Hook).Chain);

  while (*EntryHook != 0 && (**EntryHook).Lumi < Lumi) EntryHook = &((**EntryHook).Next);

  if (*EntryHook == 0 || (**EntryHook).Lumi != Lumi) //Se non trova la lumi entry
  {
    FGLumiEntry *TempLumiEntry = new FGLumiEntry;
    
    TempLumiEntry -> Next = *EntryHook;
    TempLumiEntry -> Lumi = Lumi;
    TempLumiEntry -> Delivered = Delivered;
    TempLumiEntry -> Recorded = Recorded;
    //TempLumiEntry -> FirstBX = FirstBX;
    //TempLumiEntry -> BXCount = BXCount;
    TempLumiEntry -> Locomotive = 0;
    *EntryHook = TempLumiEntry;

    return TempLumiEntry;
  } 
  else return 0;
}

Bool_t LoadLuminosityDB(Int_t StackID, TString fPath)
{
  FILE *hFile;
  char Buffer[512];
  Int_t ReadState, LineCount = 0;
  Double_t TotDeli = 0, TotReco = 0;
  TString Row;
  Bool_t LineOk;
  TString RowPart[7];
  
  cout << "Caricamento di " << fPath << "\n";
  cout.flush();

  hFile = fopen(fPath.Data(), "r");
  if (hFile == 0) {cout << "Impossibile aprire il database luminosità, operazione abortita.\n"; perror("Errore"); return kFALSE;};
  while (!(feof(hFile) || (LimitedLumi && LineCount > 5000)))
  {
    fgets (Buffer, 512, hFile);
    if (Buffer[0] != '#')
    {
      Row = TString(Buffer);
      ReadState = 0;
      for (Int_t i = 0; i < 8; i++) RowPart[i] = TString("");

      for (Int_t i = 0; i < Row.Length() - 2; i++)
      {
	if (Row.Data()[i] == ' ' && ReadState < 8) ReadState++;
	else
	{
	  RowPart[ReadState].Append(Row.Data()[i]);
	}
      }

      LineOk = RowPart[0].IsDigit() && RowPart[1].IsDigit() &&
	RowPart[2].IsFloat() && RowPart[3].IsFloat();// && 
	//RowPart[4].IsDigit() && RowPart[5].IsDigit();
      if (LineOk)
      {
	Int_t Run, Lumi;
	Float_t Delivered, Recorded;
	FGLumiEntry *TempEntry = 0;
	
	Run = RowPart[0].Atoi();
	Lumi = RowPart[1].Atoi();
	Delivered = RowPart[2].Atof();
	Recorded = RowPart[3].Atof();
	//FirstBX = RowPart[4].Atoi();
	//BXCount = RowPart[5].Atoi();
	
	/*if (Run == 163334)
	cout << "Riga importata: " << Run << " - " << Lumi << " - " <<
                                      Delivered << " - " << Recorded << " -> " <<
                                      FirstBX << " " << BXCount << "\n";*/
	    for (Int_t i = 0; i < 40; i++) cout << "\b";
	if (LineCount % 1000 == 0) cout << LineCount << " righe importate.";
	TempEntry = AddLumiEntry(StackID, Run, Lumi, Delivered, Recorded);//, FirstBX, BXCount);
        //if (TempEntry != 0) LumiEntryToParsers(StackID, Run, TempEntry);
	//else cout << "Errore, impossibile aggiungere entry. " << StackID << " " << Run << " " << Lumi << "\n";

        TotDeli += Delivered;
        TotReco += Recorded;
        LineCount++;
      }
      else
      {
	cout << "Errore: riga non valida.  ";
	cout << RowPart[0] << "-" << RowPart[1] << "-" << RowPart[2] << "-" << RowPart[3] << "-" << RowPart[4] << "-" << RowPart[5] << "\n";
      }
      //else cout << "Riga non valida: " << RowPart[0] << " - " << RowPart[1] << " - " << RowPart[2] << " - " << RowPart[3] << " - " << RowPart[4] << "\n";
    }
  }

  cout << LineCount << " righe importate.\n";
  cout << "Lumi delivered: " << TotDeli << "\nLumi recorded: " << TotReco << "\n"; 

  fclose(hFile);
  return kTRUE;
}

void LumiDBToParser(Int_t StackID)
{
  Int_t RunCount = 0;
  Int_t CurRun = 0;
  FGLumiRun *Hook = LumiDB[StackID].LumiDB;
 
  while (Hook != 0)
  {
    RunCount++;
    Hook = Hook -> Next;
  }

  Hook = LumiDB[StackID].LumiDB;
  while (Hook != 0)
  {
    FGLumiEntry *EntryHook = Hook -> Chain;

    CurRun++;
    //for (Int_t i = 0; i < 20; i++) cout << "\b";
    //PrintParsers();
    cout << "Run " << CurRun << " di " << RunCount << "\n";
    //cout.flush();
    
    while (EntryHook != 0)
    {
      LumiEntryToParsers2(StackID, Hook -> Run, EntryHook);
      EntryHook = EntryHook -> Next;
    }

    Hook = Hook -> Next;
  }
}

void PrintLuminosityDB(Int_t StackID)
{
  FGLumiRun *Hook;
  FGLumiEntry *EntryHook;

  Hook = LumiDB[StackID].LumiDB;
  while (Hook != 0)
  {
    EntryHook = Hook -> Chain;
    cout << Hook -> Run << "\n";

    while (EntryHook != 0)
    {
      cout << "    " << EntryHook -> Lumi << " - " << EntryHook -> Delivered << " - " << EntryHook -> Recorded << "\n";
      EntryHook = EntryHook -> Next;
    }

    Hook = Hook -> Next;
  }
}

Bool_t LoadFullLuminosityDB()
{
  FILE *hFile;
  char Buffer[512];
  Int_t LumiVer;
  TString *LumiPath;

  InitializeLumiDB(&(LumiDB[0]));
  InitializeLumiDB(&(LumiDB[1]));

  //LumiDBPath.Remove(LumiDBPath.Length() - 1, 1);
  hFile = fopen(LumiDBPath.Data(), "r");
  
  if (hFile == 0)
  {
    cout << "Impossibile aprire il file indice del database luminosità. Operazione abortita.\n";
    perror("Errore");
    cout << "\n";
    return kFALSE;
  }
  
  while (!feof(hFile))
  {
    fgets (Buffer, 512, hFile);
    
    if (Buffer[0] != '#' && Buffer[0] != 0)
    {
      LumiVer = Buffer[0] - '0';
      LumiPath = new TString("");
      for (Int_t i = 2; Buffer[i] != '\0' && Buffer[i] != 10 && Buffer[i] != 13; i++) LumiPath -> Append(Buffer[i]);
      cout << "Caricamento database: " << *LumiPath << " - " << "Versione: " << LumiVer << "\n";
      LoadLuminosityDB(LumiVer, *LumiPath);
    }
    
  }
  fclose(hFile);

  LumiDBToParser(0);
  LumiDBToParser(1);

  return kTRUE;
}

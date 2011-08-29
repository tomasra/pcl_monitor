struct FGLumiEntry
{
  Int_t Lumi;
  Float_t Delivered;
  Float_t Recorded;
  FGLumiEntry *Next; 
};

struct FGLumiRun
{
  Int_t Run;
  FGLumiEntry *Chain;
  FGLumiRun *Next;
};

struct FGLumiBin
{
  Float_t LBound, UBound;
  Float_t Mean, RMS;
  Float_t MeanD, RMSD;
  Float_t IntLuminosity;
  Float_t IntLuminosityD;
  Float_t Content;
};

struct FGLumiInjector
{
  FGLumiRun *EntryPoint;
  FGLumiInjector *Next;
};

struct FGLumiDB
{
  FGLumiRun *LumiDB;
};

FGLumiDB LumiDB[2];

void InitializeLumiDB(FGLumiDB *DB)
{
  DB -> LumiDB = 0;
}

Bool_t AddLumiEntry(Int_t StackID, Int_t Run, Int_t Lumi, Float_t Delivered, Float_t Recorded)
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
    *EntryHook = TempLumiEntry;

    return kTRUE;
  } 
  else return kFALSE;
}

Bool_t LoadLuminosityDB(Int_t StackID, TString fPath)
{
  FILE *hFile;
  char Buffer[512];
  Int_t ReadState, LineCount = 0;
  Double_t TotDeli = 0, TotReco = 0;
  TString Row;
  Bool_t LineOk;
  TString RowPart[4];
  
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
      for (Int_t i = 0; i < 5; i++) RowPart[i] = TString("");

      for (Int_t i = 0; i < Row.Length() - 2; i++)
      {
	if (Row.Data()[i] == ',' && ReadState < 4) ReadState++;
	else
	{
	  RowPart[ReadState].Append(Row.Data()[i]);
	}
      }

      LineOk = RowPart[0].IsDigit() && RowPart[1].IsDigit() && RowPart[2].IsFloat() && RowPart[3].IsFloat();
      /*if (!RowPart[0].IsDigit()) cout << "Errore 0\n";
      if (!RowPart[1].IsDigit()) cout << "Errore 1\n";
      if (!RowPart[2].IsFloat()) cout << "Errore 2\n";
      if (!RowPart[3].IsFloat()) cout << "Errore 3\n";*/

      if (LineOk)
      {
	Int_t Run, Lumi;
	Float_t Delivered, Recorded;
	
	Run = RowPart[0].Atoi();
	Lumi = RowPart[1].Atoi();
	Delivered = RowPart[2].Atof();
	Recorded = RowPart[3].Atof();
	//cout << "Riga importata: " << Run << " - " << Lumi << " - " << Delivered << " - " << Recorded << "\n";
 	AddLumiEntry(StackID, Run, Lumi, Delivered, Recorded);
        ParsersLumiAdd(StackID, Run, Lumi, Delivered, Recorded);
        TotDeli += Delivered;
        TotReco += Recorded;
        LineCount++;
      }
      //else cout << "Riga non valida: " << RowPart[0] << " - " << RowPart[1] << " - " << RowPart[2] << " - " << RowPart[3] << " - " << RowPart[4] << "\n";
    }
  }

  cout << LineCount << " righe importate.\n";
  cout << "Lumi delivered: " << TotDeli << "\nLumi recorded: " << TotReco << "\n"; 

  fclose(hFile);
  return kTRUE;
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
  return kTRUE;
}

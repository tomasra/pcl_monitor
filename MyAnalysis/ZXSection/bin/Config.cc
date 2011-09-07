
struct FGConfigProfile
{
  TString *ConfigName;
  TString *ConfigData;
  FGConfigProfile *Next;
};

FGConfigProfile *ConfigChain = 0;

Bool_t LoadConfigurationFile()
{
  FILE *hFile;
  char Buffer[512];
  Int_t LineLen, ReadState;
  string sss;
  FGConfigProfile *Temp;
  FGConfigProfile **Tail;

  hFile = fopen("./test/Config.txt", "r");
  Tail = &ConfigChain;
  if (hFile == 0) {cout << "Impossibile aprire il file di configurazione. Operazione abortita.\n"; return kFALSE;}

  while (!feof(hFile))
  {
    fgets (Buffer, 512, hFile);
    if (Buffer[0] != '#')
    {
      for (LineLen = 0; Buffer[LineLen] != '\0'; LineLen++);   
      LineLen--;

      Temp = new FGConfigProfile;
      Temp -> ConfigData = new TString("");
      Temp -> ConfigName = new TString("");

      ReadState = 0;
      for (Int_t k = 0; k < LineLen; k++)
      {
        switch (ReadState)
        {
        case 0:
          {
	    if (Buffer[k] == ':') ReadState++;
	    else Temp -> ConfigName -> Append(Buffer[k]);
	  } break;
        case 1:
	  if (Buffer[k+1] != ' ') ReadState++; break;
        case 2:
          if (Buffer[k] != 10 && Buffer[k] != 13) Temp -> ConfigData -> Append(Buffer[k]);
        }
      }
      
      *Tail = Temp;
      Temp -> Next = 0;
      Tail = &(Temp -> Next);
    }
  }

  fclose(hFile);
  return kTRUE;
}

TString *SeekConfiguration(TString Key)
{
  FGConfigProfile *Hook;
  TString *TempRes = 0;

  Hook = ConfigChain;
  while (Hook != 0)
  {
    if (Hook -> ConfigName -> CompareTo(Key) == 0)
    {
      TempRes = Hook -> ConfigData;
      Hook = 0;
    }
    else Hook = Hook -> Next;
  }

  return TempRes;
}

Bool_t LoadConfiguration()
{
  ConfigChain = 0;
  LoadConfigurationFile();

  InputPath = *SeekConfiguration(TString("InputDir"));
  OutputDir = *SeekConfiguration(TString("OutputFile"));
  OutputDir.Append(FGItoa(WebVersion) + TString(".root"));

  RootFileDirName = *SeekConfiguration(TString("RootDir"));
  JobFilePath = *SeekConfiguration(TString("JobFile"));
  OutputLumi = SeekConfiguration(TString("OutputLumi")) -> Atof();
  LumiDBPath = *SeekConfiguration(TString("LumiDBPath"));

  cout << "InputPath: " << InputPath << "\n";
  cout << "OutputDir: " << OutputDir << "\n";
  cout << "RootFileName: " << RootFileDirName << "\n";
  cout << "JobFile: " << JobFilePath << "\n";
  cout << "OutputLumi: " << OutputLumi << "\n\n";

  return kTRUE;
}

struct FGTreeObject
{
  FGTreeObject *Previous;
  FGTreeObject *Next;
  FGTreeObject *Son;
  FGTreeObject *Parent;
  TObject *Elemento;
  TString *Path;
};

TString TreeRowTemplate, TreeCellTemplate, TreeElementTemplate;
TFile *hWebFile;
FGTreeObject *WebFileStructure;
TString *WebFilePath;

TString *ReadWholeFile(const char *fPath)
{
  FILE *fp;
  Long_t len;
  char *buf;
  TString *TempRes;
  
  fp=fopen(fPath,"rb");
  fseek(fp,0,SEEK_END); //go to end
  len=ftell(fp); //get position at end (length)

  fseek(fp,0,SEEK_SET); //go to beg.
  buf=(char *)malloc(len); //malloc buffer
  fread(buf,len,1,fp); //read into buffer
  fclose(fp);

  TempRes = new TString(buf, len);
  return TempRes;
}

Bool_t WriteToFile(TString *Data, const char *fPath)
{
  ofstream out(fPath, ios::out | ios::binary);
  if(!out) {
    cout << "Impossibile aprire il file di output\n";
    return kFALSE;
  }
  out.write(Data -> Data(), Data -> Length());
  out.close();

  //cout << "Salvato file " << fPath << "\n";
  return kTRUE;
}

TString WebObjectIndentStructure(FGTreeObject *Oggetto, Bool_t ToShell = kFALSE)
{
  char Buffer[255];
  Int_t BufId = 0;
  FGTreeObject *Hook;
  TString TempRes = TString("");
  
  Hook = Oggetto;
  while (Hook != 0)
  {
    if (Hook -> Next == 0)
    { 
      if (Hook == Oggetto)
      {
	if (Hook -> Previous == 0) Buffer[BufId] = '-';
	else Buffer[BufId] = 'L';
      }
      else Buffer[BufId] = ' ';
    }
    else 
    {
      if (Hook == Oggetto)
      {
	if (Hook -> Previous == 0) Buffer[BufId] = 'F';
        else Buffer[BufId] = 'T';
      }
      else Buffer[BufId] = 'I';
    }
 
    BufId++;
    Hook = Hook -> Parent;
  }
  if (!ToShell) for (Int_t i = BufId - 1; i > -1; i--) TempRes.Append(Buffer[i]);
  else for (Int_t i = BufId - 1; i > -1; i--)
  {
    switch (Buffer[i])
    {
    case 'T': TempRes.Append((char)195); break;
    case 'L': TempRes.Append((char)196); break;
    case ' ': TempRes.Append(' '); break;
    }
  } 

  return TempRes;
}

Int_t WebObjectDepth(FGTreeObject *Oggetto)
{
  Int_t TempRes;

  for (TempRes = 0; Oggetto -> Parent != 0; TempRes++) Oggetto = Oggetto -> Parent;
  return TempRes;
}

TString WebStructureCFullPath(FGTreeObject Oggetto)
{
  TString *TempStr = new TString(*(Oggetto.Path));
  TempStr -> ReplaceAll("/", "_");
  if (!TempStr -> IsNull()) TempStr -> Append("_");
  TempStr -> Append(Oggetto.Elemento -> GetName());
  return *TempStr;
}

TString WebStructureCBasePath(FGTreeObject Oggetto)
{
  TString *TempStr = new TString(*(Oggetto.Path));
  TempStr -> ReplaceAll("/", "_");
  return *TempStr;
}

TString WebStructurePageName(FGTreeObject Oggetto)
{
  TString *TempStr = new TString(WebStructureCFullPath(Oggetto));
  if (TempStr -> EndsWith(".root")) TempStr = new TString("index");
  TempStr -> Append(".html");
  return *TempStr;
}

Bool_t PlotWebStructure(FGTreeObject *Hook)
{
  while (Hook != 0)
  {
    //Int_t d = WebObjectDepth(Hook);
    //for (Int_t i = 0; i < d; i++) cout << "  ";
    cout << WebObjectIndentStructure(Hook, kFALSE);
    cout << (WebStructurePageName(*Hook)).Data() << "\n";
    if (Hook -> Son != 0) PlotWebStructure(Hook -> Son);
    Hook = Hook -> Next;
  }

  return kTRUE;
}

Bool_t GrabFolder(TString Path, FGTreeObject *Parent)
{
  TDirectory *TempDir;
  TList *KeyList;

  TempDir = hWebFile -> GetDirectory(*WebFilePath + ":" + Path);
  if (TempDir == 0) {cout << "Impossibile caricare cartella. Esportazione web annullata.\n"; return kFALSE;}

  KeyList = TempDir -> GetListOfKeys();
  if (KeyList == 0) {cout << "Impossibile caricare chiavi. Esportazione web annullata.\n"; return kFALSE;}

  for (Int_t i = 0; KeyList -> At(i) != 0; i++)
  {
    FGTreeObject *TempObject = new FGTreeObject;
    FGTreeObject **Hook;
    FGTreeObject *HookShadow = 0;

    TempObject -> Elemento = ((TKey *)KeyList -> At(i)) -> ReadObj();
    if (TempObject == 0) {cout << "Impossibile caricare oggetto. Esportazione web annullata.\n"; return kFALSE;}

    TempObject -> Parent = Parent;
    TempObject -> Son = 0;
    TempObject -> Path = new TString(Path.Data());

    if (Parent == 0) Hook = &WebFileStructure; else Hook = &(Parent -> Son);
    while (*Hook != 0) {HookShadow = *Hook; Hook = &((*Hook) -> Next);}
    
    *Hook = TempObject;
    TempObject -> Previous = HookShadow;
    TempObject -> Next = 0;

    if (TempObject -> Elemento -> IsFolder()) GrabFolder(TString(Path) + TempObject -> Elemento -> GetName(), TempObject);
  } 

  return kTRUE;
}

Bool_t GrabWebTree()
{
  WebFileStructure = new FGTreeObject();
  
  WebFileStructure -> Son = 0;
  WebFileStructure -> Previous = 0;
  WebFileStructure -> Next = 0;
  WebFileStructure -> Parent = 0;
  WebFileStructure -> Path = new TString("");
  
  WebFileStructure -> Elemento = hWebFile -> GetDirectory("");
  if (WebFileStructure -> Elemento == 0) {cout << "Impossibile caricare la cartella radice, esportazione web annullata.\n"; return kFALSE;}

  GrabFolder(TString(), WebFileStructure);
  
  return kTRUE;
}

TString WebObjectHTMLTreeRow(FGTreeObject *Oggetto, TString *DiskDestination, TString *WebUrl)
{
  TString TempR, TempC, TempE, Indent;
  TString CellStack;
  
  Indent = TString(WebObjectIndentStructure(Oggetto));
  TempR = TString(TreeRowTemplate);
  CellStack = TString("");

  for (Int_t k = 0; k < Indent.Length(); k++)
  {
    TempC = TString(TreeCellTemplate);
    TempC.ReplaceAll("$ImageChar$", ' '); //Indent.Data()[k]);
    CellStack.Append(TempC);
  }
  
   TempE = TString(TreeElementTemplate);
   TempE.ReplaceAll("$ClassName$", Oggetto -> Elemento -> ClassName());
   TempE.ReplaceAll("$Name$", Oggetto -> Elemento -> GetName());
   TempE.ReplaceAll("$ObjPath$", *WebUrl + WebStructurePageName(*Oggetto));
   CellStack.Append(TempE);

   TempR.ReplaceAll("$Cells$", CellStack);
   return TempR;
}

TString ExportWebObjectHTMLTree(FGTreeObject *Oggetto, TString *DiskDestination, TString *WebUrl)
{
  TString TempRes = TString("");
  FGTreeObject *HookStack[100];
  Int_t Depth;
  
  TreeRowTemplate = *ReadWholeFile("html/TreeRowTemplate.html");
  TreeCellTemplate = *ReadWholeFile("html/TreeCellTemplate.html");
  TreeElementTemplate = *ReadWholeFile("html/TreeElementTemplate.html");
  
  Depth = 0;
  HookStack[0] = WebFileStructure;
  while (Depth > -1)
  {
    while (HookStack[Depth] != 0 && HookStack[Depth] -> Son == 0)
    {
      FGTreeObject *Hook = Oggetto;
      while (Hook != 0 && Hook -> Parent != HookStack[Depth] -> Parent) Hook = Hook -> Parent;
      if (Hook != 0 || Oggetto == HookStack[Depth] -> Parent) TempRes.Append(WebObjectHTMLTreeRow(HookStack[Depth], DiskDestination, WebUrl));
      HookStack[Depth] = HookStack[Depth] -> Next;
    }
    if (HookStack[Depth] == 0)
    {
      Depth--;
      if (Depth > -1) HookStack[Depth] = HookStack[Depth] -> Next;
    }
    else
    {
      FGTreeObject *Hook = Oggetto;
      while (Hook != 0 && Hook -> Parent != HookStack[Depth] -> Parent) Hook = Hook -> Parent;
      if (Hook != 0 || Oggetto == HookStack[Depth] -> Parent) TempRes.Append(WebObjectHTMLTreeRow(HookStack[Depth], DiskDestination, WebUrl));
      HookStack[Depth + 1] = HookStack[Depth] -> Son;
      Depth++;
    }
  }

  return TempRes;
}

Bool_t ExportWebStructure(FGTreeObject *Hook, TString *DiskDestination, TString *WebUrl)
{
  if (Hook == WebFileStructure) gSystem -> Exec("rm " + *DiskDestination + "*");
  
  {
    Int_t d = WebObjectDepth(Hook);
    for (Int_t i = 0; i < d; i++) cout << "  ";
    //cout << WebObjectIndentStructure(Hook, kFALSE);
    cout << (WebStructurePageName(*Hook)).Data() << "\n";
  }

  TString *ContentStack = new TString("");
  TString *FullTemplate;
  Bool_t IsDir;

  IsDir = Hook -> Elemento -> IsFolder();
  FullTemplate = ReadWholeFile("html/ObjectPage.html");

  FullTemplate -> ReplaceAll("$NomeOggetto$", Hook -> Elemento -> GetName());
  FullTemplate -> ReplaceAll("$Pattern$", OutputPath + '\\' + *(Hook -> Path));
  FullTemplate -> ReplaceAll("$HomePath$", *WebUrl + WebStructurePageName(*WebFileStructure));
  FullTemplate -> ReplaceAll("$Tree$", ExportWebObjectHTMLTree(Hook, DiskDestination, WebUrl));

  if (Hook -> Next == 0) FullTemplate -> ReplaceAll("$NextObjPath$", "");
  else FullTemplate -> ReplaceAll("$NextObjPath$", *WebUrl + WebStructurePageName(*Hook -> Next));
  if (Hook -> Previous == 0) FullTemplate -> ReplaceAll("$PrevObjPath$", "");
  else FullTemplate -> ReplaceAll("$PrevObjPath$", *WebUrl + WebStructurePageName(*Hook -> Previous));
  if (Hook -> Parent == 0) FullTemplate -> ReplaceAll("$LevelUpPath$", "");
  else FullTemplate -> ReplaceAll("$LevelUpPath$", *WebUrl + WebStructurePageName(*Hook -> Parent));
  
  if (IsDir)
  {
    TString *TempStr = 0;
    FGTreeObject *Arm = Hook -> Son;
    
    if (Hook -> Parent != 0)
    {
      TempStr = ReadWholeFile("html/FileTemplate.html");
      TempStr -> ReplaceAll("$FileName$", "..");
      TempStr -> ReplaceAll("$ClassName$", "FGPrevFolder");
      TempStr -> ReplaceAll("$FileLink$", *WebUrl + WebStructurePageName(*Hook -> Parent));
      ContentStack -> Append(*TempStr);
    }

    while (Arm != 0)
    {
      TempStr = ReadWholeFile("html/FileTemplate.html");
      TempStr -> ReplaceAll("$FileName$", Arm -> Elemento -> GetName());
      TempStr -> ReplaceAll("$ClassName$", Arm -> Elemento -> ClassName());
      TempStr -> ReplaceAll("$FileLink$", *WebUrl + WebStructurePageName(*Arm));

      ContentStack -> Append(*TempStr);
      ExportWebStructure(Arm, DiskDestination, WebUrl);      
      Arm = Arm -> Next;
    }
  }
  else
  {
    TCanvas *TempCanv = 0;
    TVirtualPad *TempPad = 0;
    TString *DrawOptions = new TString("");

    if (strcmp(Hook -> Elemento -> ClassName(), "TCanvas") == 0)
    {
      TempCanv = (TCanvas *)Hook -> Elemento;
      TempCanv -> SetCanvasSize(550, 400);
      TempCanv -> Draw();
    } else TempCanv = new TCanvas("TempCanvas", "Temporary canvas", 550, 400);

    if (strcmp(Hook -> Elemento -> ClassName(), "TH1F") == 0) DrawOptions -> Append("HIST");

    TempPad = TempCanv -> GetPad(0);
    if (TempPad == 0) {cout << "Pad retrival fallito, operazione abortita.\n"; return kFALSE;}
    TempCanv -> SetFillColor(kWhite);

    TempPad -> SetLogy(0);
    Hook -> Elemento -> Draw(DrawOptions -> Data()); 
    TempCanv -> SaveAs(*DiskDestination + WebStructureCFullPath(*Hook) +  "_Lin.png");

    if (!LowQuality)
    {
      TempPad -> SetLogy(1);
    
      Hook -> Elemento -> Draw(DrawOptions -> Data());
      if (!DebugMode)TempCanv -> SaveAs(*DiskDestination + WebStructureCFullPath(*Hook) +  "_Log.png");

      TempCanv -> SetCanvasSize(1024, 768);

      TempPad = TempCanv -> GetPad(0);
      if (TempPad == 0) {cout << "Pad retrival fallito, operazione abortita.\n"; return kFALSE;}
    
      TempPad -> SetLogy(0);
      Hook -> Elemento -> Draw(DrawOptions -> Data());
      if (!DebugMode) TempCanv -> SaveAs(*DiskDestination + WebStructureCFullPath(*Hook) +  "_LinHQ.png");

      TempPad -> SetLogy(1);
      Hook -> Elemento -> Draw(DrawOptions -> Data());
      if (!DebugMode) TempCanv -> SaveAs(*DiskDestination + WebStructureCFullPath(*Hook) +  "_LogHQ.png");
    }
    ContentStack = ReadWholeFile("html/GraphicTemplate.html");
    ContentStack -> ReplaceAll("$ImageLin$", *WebUrl + WebStructureCFullPath(*Hook) +  "_Lin.png");
    ContentStack -> ReplaceAll("$ImageLog$", *WebUrl + WebStructureCFullPath(*Hook) +  "_Log.png");
    ContentStack -> ReplaceAll("$ImageLinHQ$", *WebUrl + WebStructureCFullPath(*Hook) +  "_LinHQ.png");
    ContentStack -> ReplaceAll("$ImageLogHQ$", *WebUrl + WebStructureCFullPath(*Hook) +  "_LogHQ.png"); 

    if (Hook -> Elemento != TempCanv) delete TempCanv;
  }

  FullTemplate -> ReplaceAll("$Content$", *ContentStack);
  WriteToFile(FullTemplate, *DiskDestination + WebStructurePageName(*Hook)); 

  return kTRUE; 
}

void FullWebExport(TString FilePath)
{
  hWebFile = new TFile(FilePath);
  
  WebFilePath = new TString(FilePath);

  cout << "Costruzione albero web.\n";
  GrabWebTree();

  cout << "\n\nEsportazione struttura:\n\n";
  //PlotWebStructure(WebFileStructure);
  ExportWebStructure(WebFileStructure, new TString("/afs/cern.ch/user/f/fguatier/www/"), new TString(""));
  //ExportWebStructure(WebFileStructure, new TString("/afs/cern.ch/user/f/fguatier/www/"), new TString("http://fguatier.web.cern.ch/fguatier/"));
}

struct FGBunch
{
  Short_t Id;
  Float_t Lumi;
  Bool_t isLocomotive;
};

struct FGLumiEntry
{
  Int_t Lumi;
  Float_t Delivered;
  Float_t Recorded;
  Int_t FirstBX;
  Int_t BXCount;
  FGIntList *Locomotive;
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

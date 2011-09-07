#define MaxParsers 2000
#define MaxDatasets 20
Int_t ParserNo = 0;

struct FGParser
{
  Double_t RecordedLumi;
  Double_t DeliveredLumi;

  Bool_t CutOnBXLumi;
  Double_t LowBXLumi;
  Double_t HiBXLumi;
  Int_t NextBXLumiCut;

  Bool_t CutOnRunLumi;
  Int_t LowRun;
  Int_t HiRun;
  Int_t NextRunCut;

  Bool_t LocomotiveOnly;

  Double_t EventCount;
  Int_t LumiSecCount;
  Int_t StackId;
  Int_t Family;
  FGIntList *Dataset;

  Bool_t isAlive;
  Double_t X, Y;
  Double_t ErrX, ErrY;
  Double_t Sumw2;
};

struct FGParserConstructor
{
  FGParser Parser;
  Bool_t LumiCutSet;
  Bool_t RunLumiSet;
  Bool_t LocomotiveSet;
  Bool_t StackIdSet;
  Bool_t FamilySet;
  Bool_t DatasetSet;
};

FGParser Parsers[MaxParsers];
TString *FamilyNames[40];
TString *FamilyTitles[40];

void InitializeParserConstructor(FGParserConstructor *Constructor)
{
  Constructor -> Parser.RecordedLumi = 0;
  Constructor -> Parser.DeliveredLumi = 0;

  Constructor -> Parser.CutOnBXLumi = kFALSE;
  Constructor -> Parser.LowBXLumi = 0;
  Constructor -> Parser.HiBXLumi = 0;
  Constructor -> Parser.NextBXLumiCut = 0;

  Constructor -> Parser.CutOnRunLumi = kFALSE;
  Constructor -> Parser.LowRun = 0;
  Constructor -> Parser.HiRun = 0;
  Constructor -> Parser.NextRunCut = 0;

  Constructor -> Parser.LocomotiveOnly = kFALSE;

  Constructor -> Parser.EventCount = 0;
  Constructor -> Parser.LumiSecCount = 0;
  Constructor -> Parser.StackId = 0;
  Constructor -> Parser.Family = 0;
  Constructor -> Parser.Dataset = 0;

  Constructor -> Parser.Sumw2 = 0;

  Constructor -> LumiCutSet = kFALSE;
  Constructor -> RunLumiSet = kFALSE;
  Constructor -> LocomotiveSet = kFALSE;
  Constructor -> StackIdSet = kFALSE;
  Constructor -> FamilySet = kFALSE;
  Constructor -> DatasetSet = kFALSE;
}

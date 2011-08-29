struct FGJob
{
public :
  Int_t ProgressiveId;
  TString FinalState;
  TString FileName;
  Int_t SampleCount;
  Float_t XSection;
  Double_t BranchingRatio;
  Double_t Normalization;
  Bool_t toSynopsis;
  Bool_t isMC;
  Int_t Dataset;
  Double_t ContentSum;
  TString *Label;
  FGJob *Next;
};

FGJob *JobQueue;

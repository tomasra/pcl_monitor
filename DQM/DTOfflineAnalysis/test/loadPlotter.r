{
  gROOT->LoadMacro("macros.C");     // Load service macros
  gSystem->Load("root_lib/libEvent.so");
  // Get the style
  TStyle * style = getStyle("d0style");
  // Style options
  style->SetOptStat(111111);
  style->SetOptFit(1111);
  style->SetOptTitle(1);
  
  style->cd();

  // Retrieve histogram sets
//   TFile *f = gROOT->GetListOfFiles()->Last();
  DTHistoPlotter *plotter = new DTHistoPlotter();
  TFile *file_tm4 = new TFile("/data/c/cerminar/data/DTAnalysis/DTCalibration/histo_t-4.root");
  plotter->addFile(-2,file_tm4);
  TFile *file_tm2 = new TFile("/data/c/cerminar/data/DTAnalysis/DTCalibration/histo_t-2.root");
  plotter->addFile(-1,file_tm2);
  TFile *file_t0 = new TFile("/data/c/cerminar/data/DTAnalysis/DTCalibration/histo_t0.root");
  plotter->addFile(0,file_t0);
  TFile *file_t2 = new TFile("/data/c/cerminar/data/DTAnalysis/DTCalibration/histo_t2.root");
  plotter->addFile(1,file_t2);
  TFile *file_t4 = new TFile("/data/c/cerminar/data/DTAnalysis/DTCalibration/histo_t4.root");
  plotter->addFile(2,file_t4);


}


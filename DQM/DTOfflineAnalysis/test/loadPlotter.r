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
  TFile *file_tm4 = new TFile("test.root");
  plotter->addFile(-2,file_tm4);
//   TFile *file_tm2 = new TFile("/data/c/cerminar/data/DTAnalysis/DTCalibration/histo_t-2_V01.root");
//   plotter->addFile(-1,file_tm2);
//   TFile *file_t0 = new TFile("/data/c/cerminar/data/DTAnalysis/DTCalibration/histo_t0_V01.root");
//   plotter->addFile(0,file_t0);
//   TFile *file_t2 = new TFile("/data/c/cerminar/data/DTAnalysis/DTCalibration/histo_t2_V01.root");
//   plotter->addFile(1,file_t2);
//   TFile *file_t4 = new TFile("/data/c/cerminar/data/DTAnalysis/DTCalibration/histo_t4_V01.root");
//   plotter->addFile(2,file_t4);


}


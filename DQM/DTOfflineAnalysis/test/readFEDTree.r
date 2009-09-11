//
{ 

  gROOT->LoadMacro("macros.C");
  TStyle *style = getStyle("myStyle");
  style->cd();
  int NEVENTS = 50;
  
  

  string inputFile = "/data/c/cerminar/scratch/merge9/FEDSizeAnalysis_merged.root";
  string outputFile = "/tmp/cerminar/FED_histo.root";
  

  FEDNtupleReader *reader = new FEDNtupleReader(inputFile, outputFile);
  reader->addTH1F("FED770","FED770","",1000,0,2000,"hist,logy");
  reader->addTH1F("FED771","FED771","",1000,0,2000,"hist,logy");
  reader->addTH1F("FED772","FED772","",1000,0,2000,"hist,logy");
  reader->addTH1F("FED773","FED773","",1000,0,2000,"hist,logy");
  reader->addTH1F("FED774","FED774","",1000,0,2000,"hist,logy");
  reader->addTH1F("FED775","FED775","",1000,0,2000,"hist,logy");
  reader->addTH1F("FED776","FED776","",1000,0,2000,"hist,logy");
  reader->addTH1F("FED777","FED777","",1000,0,2000,"hist,logy");
  reader->addTH1F("FED778","FED778","",1000,0,2000,"hist,logy");
  reader->addTH1F("FED779","FED779","",1000,0,2000,"hist,logy");
  reader->addTH1F("DT","DT","",1000,0,2000,"hist,logy");
  reader->addTH1F("Ecal","Ecal","",1000,0,2000,"hist,logy");
  reader->addTH1F("RPC","RPC","",1000,0,2000,"hist,logy");
  reader->addTH1F("CSC","CSC","",1000,0,2000,"hist,logy");
  reader->addTH1F("Hcal","Hcal","",1000,0,2000,"hist,logy");
  reader->addTH2F("DTvsEcal","DT", "Ecal","",1000,0,2000,1000,0,2000,"box");
  reader->addTH2F("DTvsHcal","DT", "Hcal","",1000,0,2000,1000,0,2000,"box");
  reader->addTH2F("DTvsRPC","DT", "RPC","",1000,0,2000,1000,0,2000,"box");
  reader->addTH2F("DTvsCSC","DT", "CSC","",1000,0,2000,1000,0,2000,"box");

//   reader->addTH2F("FED770vsRPC","FED770","RPC","",1000,0,2000,1000,0,2000,"box");
//   reader->addTH2F("FED771vsRPC","FED771","RPC","",1000,0,2000,1000,0,2000,"box");
//   reader->addTH2F("FED772vsRPC","FED772","RPC","",1000,0,2000,1000,0,2000,"box");
//   reader->addTH2F("FED773vsRPC","FED773","RPC","",1000,0,2000,1000,0,2000,"box");
//   reader->addTH2F("FED774vsRPC","FED774","RPC","",1000,0,2000,1000,0,2000,"box");
//   reader->addTH2F("FED775vsRPC","FED775","RPC","",1000,0,2000,1000,0,2000,"box");
//   reader->addTH2F("FED776vsRPC","FED776","RPC","",1000,0,2000,1000,0,2000,"box");
//   reader->addTH2F("FED777vsRPC","FED777","RPC","",1000,0,2000,1000,0,2000,"box");
//   reader->addTH2F("FED778vsRPC","FED778","RPC","",1000,0,2000,1000,0,2000,"box");
//   reader->addTH2F("FED779vsRPC","FED779","RPC","",1000,0,2000,1000,0,2000,"box");

//   reader->addTH2F("DTvsSiPixel","DT", "SiPixel","",1000,0,2000,1000,0,2000,"box");
//   reader->addTH2F("DTvsSiStrip","DT", "SiStrip","",1000,0,2000,1000,0,2000,"box");
//   reader->addTH2F("DTvsLS","LS", "DT","",800,0,800,1000,0,2000,"box");
//   reader->addTH2F("RPCvsLS","LS", "RPC","",800,0,800,1000,0,2000,"box");


//   // 
  reader->runQueries(-1,"");

//   reader->addTH2F("DTvsEvent","event", "DT","",1000,10990000,11115000,1000,0,2000,"box");
//   reader->addTH2F("RPCvsEvent","event", "RPC","",1000,10990000,11115000,1000,0,2000,"box");
  
//   reader->runQueries(-1,"LS == 102");

//   reader->analyse(NEVENTS);
}

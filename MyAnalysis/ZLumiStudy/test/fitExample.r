
using namespace RooFit;

void fitExample() {
 
  
  TFile *file = new TFile("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB6/ZLumiStudy_sorted.root","r");
  TTree *tree = (TTree *) file->Get("candTree");

  tree->Print();
  

  vector<float> *zMasses;

  TBranch        *b_ZMass;   //!
  TBranch        *b_iBC;   //!


  int ibc = 0;
  

  tree->SetBranchAddress("ZMass", &zMasses, &b_ZMass);
  tree->SetBranchAddress("iBC", &ibc, &b_iBC);


  RooRealVar  mass("mass","mass",0,200);
  RooDataSet data("data","data",RooArgSet(mass));


  for(int entry = 0; entry != 1000; ++entry) {
    tree->GetEntry(entry);


    cout << "Entry" << entry << endl;

    if(zMasses->size() != 0 && ibc != -1) {
      cout << ibc << endl;
      cout << "M: " << (*zMasses)[ibc] << endl;
      
      mass = (*zMasses)[ibc];
      data.add(RooArgSet(mass));
	

    }
  }
  data.Print("v");

  RooWorkspace w("w","w");
  w.import(data);

  /*w.factory("Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])");
  w.factory("Exponential::background(mass, lp[0,-5,5])");
  w.factory("expr::nSignal('fSigAll*numTot', fSigAll[.9,0,1],numTot[1,0,1e10])");
  w.factory("expr::nBkg('(1-fSigAll)*numTot', fSigAll,numTot)");
  w.factory("SUM::pdfSigPlusBackg(nSignal*signal, nBkg*background)"); */

  w.factory("Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])");
  w.factory("Voigtian::signal2(mass, mean2[90,80,100], width, sigma2[4,2,10])");
  w.factory("SUM::signal(vFrac[0.8,0,1]*signal1, signal2)");
  w.factory("Exponential::background(mass, lp[-0.1,-1,0.1])");

  w.factory("expr::nSignal('fSigAll*numTot', fSigAll[.9,0,1],numTot[1,0,1e10])");
  w.factory("expr::nBkg('(1-fSigAll)*numTot', fSigAll,numTot)");

  w.factory("SUM::pdfSigPlusBackg(nSignal*signal, nBkg*background)");

  w.pdf("pdfSigPlusBackg")->Print();

	    
//w.factory("Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])");

  w.Print();
  
  w.pdf("pdfSigPlusBackg")->fitTo(data);

  

  RooPlot* massframe = mass.frame(Bins(100),Title("Mass")) ;
  data.plotOn(massframe);
//   gauss.plotOn(massframe);
  w.pdf("pdfSigPlusBackg")->plotOn(massframe);
  
  massframe->Draw();


}

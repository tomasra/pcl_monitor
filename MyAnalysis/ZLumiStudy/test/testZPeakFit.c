template <typename A, typename B>
static A lexical_cast(const B& b)
{
  std::stringstream sstr;
  sstr << b;
  A a;
  sstr >> a;
  return a;
}



void testZPeakFit() {
	gSystem->AddIncludePath("-I$ROOFITSYS/include");
	
	gSystem->Load("libRooFit");
	gSystem->Load("libRooFitCore");
	gROOT->LoadMacro("$CMSSW_BASE/src/MyAnalysis/ZLumiStudy/test/macros/ZPeakFit.C+g");

	TFile *file = new TFile("/data1/ZLumiStudy/PROD120716_v0/DoubleMuB6/ZLumiStudy_sorted.root","r");
	TTree *tree = (TTree *) file->Get("candTree");

	//tree->Print();

	vector<float> *zMasses;

	TBranch        *b_ZMass;   //!
	TBranch        *b_iBC;   //!

	int ibc = 0;

	tree->SetBranchAddress("ZMass", &zMasses, &b_ZMass);
	tree->SetBranchAddress("iBC", &ibc, &b_iBC);


	TH1F* hist = new TH1F("Zmass", "; ZMass [GeV]; Events", 100, 0, 200);
	hist->Sumw2();

	for (int entry = 0; entry < 1000; entry++) {
		tree->GetEntry(entry);

		if(zMasses->size() != 0 && ibc != -1) {
			float mass = (*zMasses)[ibc];
			hist->Fill(mass);
		}

	}

	TFile* file = new TFile("testFit.root", "RECREATE");

	ZPeakFit fit(hist, "t");

	fit.fitVExpo("test");
	fit.fit2VExpo("test2");
	fit.fit2VExpoMin70("test3");


	frame = fit.plot();

	fit.save(frame);

	file->Close();


}

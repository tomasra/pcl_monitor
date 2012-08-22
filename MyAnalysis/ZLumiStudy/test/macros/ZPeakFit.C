#include "ZPeakFit.h"

using namespace RooFit;


// Constructor
ZPeakFit::ZPeakFit(TH1* h)
: mass("mass", "mass", 0, 200) , data("data", "data", mass, h), w("w","w")
{ 
	
}

// TODO: Namen uebergeben
RooPlot* ZPeakFit::fitVExpo() {
	w.import(data);

	w.factory("Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])");
	w.factory("Exponential::background(mass, lp[0,-5,5])");

	return fit();
}

RooPlot* ZPeakFit::fit2VExpo() {
	w.import(data);

	w.factory("Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])");
	w.factory("Voigtian::signal2(mass, mean2[90,80,100], width, sigma2[4,2,10])");
	w.factory("SUM::signal(vFrac[0.8,0,1]*signal1, signal2)");
	w.factory("Exponential::background(mass, lp[-0.1,-1,0.1])");
	
	return fit();
}

RooPlot* ZPeakFit::fit2VExpoMin70() {
	w.import(data);

	w.factory("Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])");
	w.factory("Voigtian::signal2(mass, mean2[90,80,100], width, sigma2[4,3,10])");
	w.factory("SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)");
	w.factory("Exponential::background(mass, lp[-0.1,-1,0.1])");
	
	return fit();
}

RooPlot* ZPeakFit::fit() {
	w.factory("expr::nSignal('fSigAll*numTot', fSigAll[.9,0,1],numTot[1,0,1e10])");
	w.factory("expr::nBkg('(1-fSigAll)*numTot', fSigAll,numTot)");
	w.factory("SUM::pdfSigPlusBackg(nSignal*signal, nBkg*background)");

	w.pdf("pdfSigPlusBackg")->Print();

	w.Print();
  
	result = w.pdf("pdfSigPlusBackg")->fitTo(data, Save());
	//w.import(result);

	RooPlot* massframe = mass.frame(Bins(100),Title("Mass"));
	massframe->SetName("test");
	data.plotOn(massframe, DataError(RooAbsData::SumW2));
	w.pdf("pdfSigPlusBackg")->plotOn(massframe);

	return massframe;
}


void ZPeakFit::getResult() {
	result->Print();
	long fitnll = result->minNll();
	cout << "nll " << fitnll << endl;

}


void ZPeakFit::save(RooPlot* frame) {
	frame->Write();
	result->Write();
}


#ifndef ZPeakFit_H
#define ZPeakFit_H

#include "RooGlobalFunc.h"

#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooCategory.h"
#include "RooArgList.h"
#include "RooDataHist.h"
#include "RooFormulaVar.h"
#include "RooHistPdf.h"
#include "RooGenericPdf.h"
#include "RooAddPdf.h"
#include "RooSimultaneous.h"
#include "RooGaussian.h"
#include "RooNLLVar.h"
#include "RooConstVar.h"
#include "RooMinuit.h"
#include "RooFitResult.h"
#include "RooExponential.h"
#include "RooFFTConvPdf.h"
#include "RooWorkspace.h"
#include "RooPlot.h"
#include "TCanvas.h"

class ZPeakFit {
public:
	ZPeakFit(TH1* h, std::string title);


	void fitVExpo(std::string title);
	void fit2VExpo(std::string title);
	void fit2VExpoMin70(std::string title);
	
	RooFitResult* getResult(std::string fit);
	RooPlot* plot();

	void save(RooPlot* frame);

private:
	RooRealVar mass;
	RooDataHist data;
	RooFitResult* result_VExpo;
	RooFitResult* result_2VExpo;
	RooFitResult* result_2VExpoMin70;
	RooWorkspace w;
	RooPlot* massframe;

	RooAbsPdf* pdf_VExpo;
	RooAbsPdf* pdf_2VExpo;
	RooAbsPdf* pdf_2VExpoMin70;

	bool fit_VExpo;
	bool fit_2VExpo;
	bool fit_2VExpoMin70;

};
#endif

#ifndef DTHistoPlotter_H
#define DTHistoPlotter_H

/** \class DTHistoPlotter
 *  Utility class to plot TimeBoxes produced with DTTTrigCalibration.
 *  The time box rising edge can be fitted using exactly the same code that is
 *  used by the calibration application.
 *
 *  $Date: 2008/12/03 10:41:16 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include "TString.h"
#include "DTDetId.h"

#include <map>


class TFile;
class TCanvas;
class TH1F;
class TH2F;
class TProfile;
class HRes1DHits;
class HSegment;


class DTHistoPlotter {
public:
  /// Constructor
  DTHistoPlotter();


  /// Destructor
  virtual ~DTHistoPlotter();

  void addFile(int index, TFile *file);


  // Operations
  TH1F *plotRes(const int fileN,
		const TString& set,
		int wheel, int station, int sector, int sl,
		const TString& drawOptions = "");
  
  TH1F * plotNHitsSegm(const int fileN,
			const TString& set,			
			int wheel, int station, int sector,
			const TString& drawOptions = "");
  


  TH1F * plotChi24DSegm(const int fileN,
			const TString& set,			
			int wheel, int station, int sector,
			const TString& drawOptions = "");

  TH1F * plotSegmAngleSLTheta(const int fileN,
			      const TString& set,			      
			      int wheel, int station, int sector,
			      const TString& drawOptions = "");
  
  TH1F * plotSegmAngleSLPhi(const int fileN,
			    const TString& set,
			    int wheel, int station, int sector,
			    const TString& drawOptions = "");

  TH2F * plotNHitsPhiVsPhi(const int fileN,
			   const TString& set,
			   int wheel, int station, int sector,
			   const TString& drawOptions = "");
  
  TH2F * plotNHitsThetaVsPhi(const int fileN,
			     const TString& set,
			     int wheel, int station, int sector,
			     const TString& drawOptions = "");


  TH1F * plotProjSegm(const int fileN,
		      const TString& set,
		      int wheel, int station, int sector,
		      const TString& drawOptions = "");

  TH1F * plotNHitsTheta(const int fileN,
			const TString& set,
			int wheel, int station, int sector,
			const TString& drawOptions = "");

  TH1F * plotT0SegPhi(const int fileN,
		      const TString& set,
		      int wheel, int station, int sector,
		      const TString& drawOptions = "");

  TH1F * plotSeg1D(const TString& hName,
		   const int fileN,
		   const TString& set,
		   int wheel, int station, int sector,
		   const TString& drawOptions = "");

  TH2F * plotSeg2D(const TString& hName,
		   const int fileN,
		   const TString& set,
		   int wheel, int station, int sector,
		   const TString& drawOptions = "");


  TH1F * plotRes1D(const TString& hName,
		   const int fileN,
		   const TString& set,
		   int wheel, int station, int sector, int sl,
		   const TString& drawOptions = "");

  TH2F * plotRes2D(const TString& hName,
		   const int fileN,
		   const TString& set,
		   int wheel, int station, int sector, int sl,
		   const TString& drawOptions = "");

//   TH2F * plotResVsDistToWire(int wheel, int station, int sector, int sl,
// 			     const TString& drawOptions = "");

//   TProfile * plotResVsSLY(int wheel, int station, int sector, int sl,
// 			  const TString& drawOptions = "");

//   TProfile * plotResVsSLX(int wheel, int station, int sector, int sl,
// 			  const TString& drawOptions = "");

//   TH1F * plotN4DSegm(int wheel, int station, int sector,
// 		     const TString& drawOptions = "");
  
  
//   TH1F * plotImpAngle(int wheel, int station, int sector,
// 		      const TString& drawOptions = "");
  
  
//   TH2F * plotPosInChSegm4D(int wheel, int station, int sector,
// 			   const TString& drawOptions = "");
  
//   TH1F * plotPosXInChSegm4D(int wheel, int station, int sector,
// 			   const TString& drawOptions = "");


//   TH1F * plotPosYInChSegm4D(int wheel, int station, int sector,
// 			    const TString& drawOptions = "");
  
  /// Print all canvases in a pdf file.
  void printPDF();

  void fitAllInSet(const TString& set, const TString& options = "");

  double computeHistoMedian(TH1F * histo);



protected:

private:
  TCanvas *drawHisto(int fileIndex, TH1F *histo, const TString& drawOptions = "");
  TCanvas *drawHisto(int fileIndex, TH2F *histo, const TString& drawOptions = "");

  HRes1DHits * getHistoRes(int fileN, const TString& set, const DTDetId& detId);
  HSegment * getHistoSeg(int fileN, const TString& set, const DTDetId& detId);

  void fitAndDraw(int fileIndex, TH1F *histo);




  
//   TString getHistoNameSuffix(int wheel, int station, int sector); // FIXME: remove
//   TString getHistoNameSuffix(int wheel, int station, int sector, int sl);
//   TString getHistoNameSuffix(int wheel, int station, int sector, int sl, int layer);
//   TString getHistoNameSuffix(int wheel, int station, int sector, int sl, int layer, int wire);

//   TString getDirName(int wheel, int station, int sector);


//   TH1F* plotHisto(const TString& histoName, const TString& drawOptions = "");
//   TH2F* plotHisto2D(const TString& histoName, const TString& drawOptions = "");

  TCanvas * newCanvas(TString name="",
		      TString title="",
		      int xdiv=0,
		      int ydiv=0,
		      int form = 1,
		      int w=-1);

  TCanvas * newCanvas(TString name, int xdiv, int ydiv, int form, int w);
  TCanvas * newCanvas(int xdiv, int ydiv, int form = 1);
  TCanvas * newCanvas(int form = 1);
  TCanvas * newCanvas(TString name, int form, int w=-1);


  std::map<int, std::map<TString, std::map<DTDetId, HRes1DHits*> > > histosRes;
  std::map<int, std::map<TString, std::map<DTDetId, HSegment*> > > histosSeg;

  std::map<int, TFile*> files;
  

};
#endif

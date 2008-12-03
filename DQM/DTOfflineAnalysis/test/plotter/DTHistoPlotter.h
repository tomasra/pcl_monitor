#ifndef DTHistoPlotter_H
#define DTHistoPlotter_H

/** \class DTHistoPlotter
 *  Utility class to plot TimeBoxes produced with DTTTrigCalibration.
 *  The time box rising edge can be fitted using exactly the same code that is
 *  used by the calibration application.
 *
 *  $Date: 2006/07/12 13:10:35 $
 *  $Revision: 1.2 $
 *  \author G. Cerminara - INFN Torino
 */

#include "TString.h"


class TFile;
class TCanvas;
class TH1F;
class TH2F;
class TProfile;

class DTHistoPlotter {
public:
  /// Constructor
  DTHistoPlotter(TFile *file);


  /// Destructor
  virtual ~DTHistoPlotter();

  // Operations
  TH1F *plotRes(int wheel, int station, int sector, int sl,
		const TString& drawOptions = "");
  TH2F * plotResVsDistToWire(int wheel, int station, int sector, int sl,
			     const TString& drawOptions = "");

  TProfile * plotResVsSLY(int wheel, int station, int sector, int sl,
			  const TString& drawOptions = "");

  TProfile * plotResVsSLX(int wheel, int station, int sector, int sl,
			  const TString& drawOptions = "");

  TH1F * plotN4DSegm(int wheel, int station, int sector,
		     const TString& drawOptions = "");
  
  TH1F * plotChi24DSegm(int wheel, int station, int sector,
			const TString& drawOptions = "");
  
  TH1F * plotImpAngle(int wheel, int station, int sector,
		      const TString& drawOptions = "");
  
  TH1F * plotSegmAngleSLTheta(int wheel, int station, int sector,
			      const TString& drawOptions = "");
  
  TH1F * plotSegmAngleSLPhi(int wheel, int station, int sector,
			    const TString& drawOptions = "");
  
  TH2F * plotPosInChSegm4D(int wheel, int station, int sector,
			   const TString& drawOptions = "");
  
  TH1F * plotPosXInChSegm4D(int wheel, int station, int sector,
			   const TString& drawOptions = "");


  TH1F * plotPosYInChSegm4D(int wheel, int station, int sector,
			    const TString& drawOptions = "");
  
  /// Print all canvases in a pdf file.
  void printPDF();

  
protected:

private:
  // 0 for old files with TH3F for the segment positions
  // 1 for new files with the TProfile
  int version;


  TString getHistoNameSuffix(int wheel, int station, int sector);
  TString getHistoNameSuffix(int wheel, int station, int sector, int sl);
  TString getHistoNameSuffix(int wheel, int station, int sector, int sl, int layer);
  TString getHistoNameSuffix(int wheel, int station, int sector, int sl, int layer, int wire);

  TString getDirName(int wheel, int station, int sector);


  TH1F* plotHisto(const TString& histoName, const TString& drawOptions = "");
  TH2F* plotHisto2D(const TString& histoName, const TString& drawOptions = "");

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

  TFile *theFile;
};
#endif

#ifndef HistoStationOccupancy_H
#define HistoStationOccupancy_H

/** \class HistoStationOccupancy
 *  No description available.
 *
 *  $Date: 2008/10/21 10:29:45 $
 *  $Revision: 1.1 $
 *  \author G. Cerminara - INFN Torino
 */

#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"
#include <string>


class HistoStationOccupancy {
public:
  /// Constructor
  HistoStationOccupancy(std::string name, int binx, double xmin, double xmax) : theName(name) {
    hOccup = new TH1F(std::string("hOcc_"+name).c_str(),std::string("Occupancy "+name).c_str(),
		      binx,xmin,xmax);
    hOccupVsSect = new TH2F(std::string("hOccupVsSect_"+name).c_str(),
			    std::string("Occupancy vs sector"+name).c_str(),
			    12,1,13,
			    binx,xmin,xmax);


  }

  HistoStationOccupancy(std::string name, TFile* file) : theName(name) {
    hOccup = (TH1F*)file->Get(std::string("hOcc_"+name).c_str());
    hOccupVsSect = (TH2F*)file->Get(std::string("hOccupVsSect_"+name).c_str());
  }

  /// Destructor
  ~HistoStationOccupancy() {}

  // Operations
  void fill(float numberObject,float sector) {
    hOccup->Fill(numberObject);
    hOccupVsSect->Fill(sector, numberObject);
  }

  void write() {
    hOccup->Write();
    hOccupVsSect->Write();
  }

  TH1F *hOccup;
  TH2F * hOccupVsSect;

private:

  TString theName;
};

#endif


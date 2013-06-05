
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2010/05/13 09:34:58 $
 *  $Revision: 1.3 $
 *  \author G. Cerminara - INFN Torino
 */

#include "Utils.h"

#include "DTDetId.h"
#include "TCanvas.h"

#include <sstream>

using namespace std;

Utils::Utils(){}

Utils::~Utils(){}

TString Utils::getHistoNameFromDetId(const DTDetId& detId) {
  stringstream wheelStr; 
//   if(detId.wheel == 0) wheelStr << "all";
//   else wheelStr << detId.wheel;
  wheelStr << detId.wheel;

  stringstream stationStr; 
  if(detId.station == 0) stationStr << "all";
  else stationStr << detId.station;

  stringstream sectorStr; 
  if(detId.sector == 0) sectorStr << "all";
  else sectorStr << detId.sector;

  stringstream slStr; 
  if(detId.sl == 0) slStr << "all";
  else slStr << detId.sl;

  stringstream layerStr; 
  if(detId.layer == 0) layerStr << "all";
  else layerStr << detId.layer;

  string namestr = "Wh" + wheelStr.str() +
    "_St" + stationStr.str() + 
    "_Se" + sectorStr.str();
    
  if(detId.sl != 0) {
    namestr = namestr + "_SL" + slStr.str();
  }
  if(detId.layer != 0) {
    namestr = namestr + "_L" + layerStr.str();
  }

  return TString(namestr.c_str());
}


TString Utils::getHistoNameFromDetIdAndSet(const DTDetId& detId, const TString& set) {
  return Utils::getHistoNameFromDetId(detId) + "_" + set;
}


TString Utils::getDTValidationHistoNameFromDetId(const DTDetId& detId, TString step) {
  TString result=step;
  if(detId.sl == 2) {
    result+="RZ_W";
  } else {
    result+="RPhi_W";
  }
  //  result+=long(abs(detId.wheel));
  result=result+long(abs(detId.wheel))+"_St"+long(detId.station);
  return result;
}



TCanvas * Utils::newCanvas(TString name, TString title,
			   int xdiv, int ydiv, int form, int w) {
  static int i = 1;
  if (name == "") {
    name = TString("Canvas "+i);
    i++;
  }
  TCanvas *c = 0;
  if (title == "") title = name;
  if (w<0) {
    c = new TCanvas(name,title, form);
  } else {
    c = new TCanvas(name,title,form,w);
  }
  if (xdiv*ydiv!=0) c->Divide(xdiv,ydiv);
  c->cd(1);
  return c;
}

TCanvas * Utils::newCanvas(TString name, int xdiv, int ydiv, int form, int w) {
  return newCanvas(name, name,xdiv,ydiv,form,w);
}

TCanvas * Utils::newCanvas(int xdiv, int ydiv, int form) {
  return newCanvas("","",xdiv,ydiv,form);
}

TCanvas * Utils::newCanvas(int form) {
  return newCanvas(0,0,form);
}

TCanvas * Utils::newCanvas(TString name, int form, int w) {
  return newCanvas(name, name, 0,0,form,w);
}
